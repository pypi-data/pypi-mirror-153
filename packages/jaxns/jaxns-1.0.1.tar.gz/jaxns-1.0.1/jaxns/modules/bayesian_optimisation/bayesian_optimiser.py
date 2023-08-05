# for Gaussian processes this is important
from typing import List, Tuple

from jaxns import NestedSampler, PriorChain, UniformPrior, HalfLaplacePrior, resample, GlobalOptimiser
from jaxns.modules.gaussian_process.kernels import RBF
from jaxns.modules.bayesian_optimisation.utils import latin_hypercube
from jaxns.internals.maps import prepare_func_args
from jax.scipy.linalg import solve_triangular
from jax.scipy.special import ndtr
from jax import random, vmap
from jax import numpy as jnp, jit
from functools import partial


def log_normal(x, mean, cov):
    L = jnp.linalg.cholesky(cov)
    # U, S, Vh = jnp.linalg.svd(cov)
    log_det = jnp.sum(jnp.log(jnp.diag(L)))  # jnp.sum(jnp.log(S))#
    dx = x - mean
    dx = solve_triangular(L, dx, lower=True)
    # U S Vh V 1/S Uh
    # pinv = (Vh.T.conj() * jnp.where(S!=0., jnp.reciprocal(S), 0.)) @ U.T.conj()
    maha = dx @ dx  # dx @ pinv @ dx#solve_triangular(L, dx, lower=True)
    log_likelihood = -0.5 * x.size * jnp.log(2. * jnp.pi) \
                     - log_det \
                     - 0.5 * maha
    return log_likelihood


def aquisition(U_star, U, Y, kernel, sigma, lengthscale, uncert):
    def f(x):
        return x * ndtr(x) + jnp.exp(-0.5 * x ** 2) / jnp.sqrt(2. * jnp.pi)

    Kxx = kernel(U, U, lengthscale, sigma)
    Kxsx = kernel(U_star, U, lengthscale, sigma)
    data_cov = jnp.square(uncert) * jnp.eye(U.shape[0])
    h = jnp.linalg.solve(Kxx + data_cov, Y)
    post_mu_xx = Kxx @ h
    post_mu_xs = Kxsx @ h

    # Kxsxs[i,j] - Kxsx[i,m] @ Kxx^-1[m, n] @ Kxsx[j,n]
    post_var_xs = sigma ** 2 - Kxsx[0, :] @ jnp.linalg.solve(Kxx + data_cov, Kxsx[0, :])

    return jnp.sqrt(post_var_xs) * f(post_mu_xs - jnp.max(post_mu_xx))


def marginalised_aquisition(U_star, U, Y, kernel, samples):
    @prepare_func_args
    def _aquisition(sigma, lengthscale, uncert):
        return aquisition(U_star=U_star[None,:], U=U, Y=Y, kernel=kernel, sigma=sigma, lengthscale=lengthscale, uncert=uncert)

    return jnp.mean(vmap(_aquisition)(**samples))


def posterior_solve(key, U, Y, kernel):
    with PriorChain() as prior_chain:
        UniformPrior('lengthscale', jnp.zeros(U.shape[1]), jnp.ones(U.shape[1]))
        HalfLaplacePrior('uncert', 0.1)
        HalfLaplacePrior('sigma', 1.)

    def log_likelihood(sigma, lengthscale, uncert):
        """
        P(Y|sigma, half_width) = N[Y, f, K]
        Args:
            sigma:
            l:

        Returns:

        """
        data_cov = jnp.square(uncert) * jnp.eye(U.shape[0])
        mu = jnp.zeros_like(Y)
        K = kernel(U, U, lengthscale, sigma)
        return log_normal(Y, mu, K + data_cov)

    ns = NestedSampler(log_likelihood, prior_chain, dynamic=False)
    results = ns(key=key, G=0., termination_evidence_uncert=0.05)
    return results


@partial(jit, static_argnames=['top_two'])
def choose_next_U(key, U, Y, top_two: bool = False,
                  *,
                  termination_patience=3,
                  termination_frac_likelihood_improvement=1e-3,
                  termination_likelihood_contour=None,
                  termination_max_num_steps=None,
                  termination_max_num_likelihood_evaluations=None):
    kernel = RBF()
    key1, key2, key3 = random.split(key, 3)

    U_mean = jnp.nanmean(U, axis=0)
    U_scale = jnp.nanstd(U, axis=0) + 1e-6
    U -= U_mean
    U /= U_scale

    Y_mean = jnp.nanmean(Y, axis=0)
    Y_scale = jnp.nanstd(Y, axis=0) + 1e-6
    Y -= Y_mean
    Y /= Y_scale

    results = posterior_solve(key1, U, Y, kernel)

    # search over U-domain space

    samples = resample(key=key2,
                       samples=results.samples, log_weights=results.log_dp_mean,
                       S=100, replace=True)

    with PriorChain() as search_prior_chain:
        # we'll effectively place no prior on the parameters, other than requiring them to be within [-10,10]
        UniformPrior('U_star', jnp.zeros(U.shape[1]), jnp.ones(U.shape[1]))

    go = GlobalOptimiser(loglikelihood=lambda U_star: marginalised_aquisition(
        U_star=U_star, U=U, Y=Y, kernel=kernel, samples=samples), prior_chain=search_prior_chain,
                         samples_per_step=search_prior_chain.U_ndims * 10)

    go_result = go(key=key3,
                   termination_patience=termination_patience,
                   termination_frac_likelihood_improvement=termination_frac_likelihood_improvement,
                   termination_likelihood_contour=termination_likelihood_contour,
                   termination_max_num_steps=termination_max_num_steps,
                   termination_max_num_likelihood_evaluations=termination_max_num_likelihood_evaluations)
    next_U = go_result.sample_L_max['U_star'] * U_scale + U_mean
    return next_U


class BayesianOptimiser(object):
    def __init__(self, prior_chain: PriorChain, U=None, X=None, Y=None, key=None):
        self.prior_chain = prior_chain
        self.prior_chain.build()
        self.U = U or []
        self.X = X or []
        self.Y = Y or []
        assert len(self.Y) == len(self.U) == len(self.X)
        if key is None:
            key = random.PRNGKey(42)
        self.key = key
        self.beta = 0.5

    def __repr__(self):
        return f"BayesianOptimiser(num_measurements={len(self.Y)}, max.obj.={max(self.Y)})"

    def initialise_experiment(self, num_samples) -> Tuple[List[jnp.ndarray], List[jnp.ndarray]]:
        self.key, key = random.split(self.key)
        U_test = list(latin_hypercube(key, num_samples, self.prior_chain.U_ndims, cube_scale=0))
        X_test = list(map(lambda U: self.prior_chain(U), U_test))
        return U_test, X_test

    def add_result(self, U, X, Y):
        self.U.append(U)
        self.X.append(X)
        self.Y.append(Y)

    def choose_next_sample_location(self, termination_patience=2,
                                    termination_frac_likelihood_improvement=1e-2,
                                    termination_likelihood_contour=None,
                                    termination_max_num_steps=None,
                                    termination_max_num_likelihood_evaluations=None):
        self.key, key1, key2 = random.split(self.key, 3)
        # choose_I1 = random.uniform(key1) < self.beta
        U_test = choose_next_U(key=key2,
                                   U=jnp.asarray(self.U),
                                   Y=jnp.asarray(self.Y),
                                   top_two=False,
                                   termination_patience=termination_patience,
                                   termination_frac_likelihood_improvement=termination_frac_likelihood_improvement,
                                   termination_likelihood_contour=termination_likelihood_contour,
                                   termination_max_num_steps=termination_max_num_steps,
                                   termination_max_num_likelihood_evaluations=termination_max_num_likelihood_evaluations
                                   )
        # else:
        #     U_test = choose_next_U(key=key2,
        #                            U=jnp.asarray(self.U),
        #                            Y=jnp.asarray(self.Y),
        #                            top_two=True,
        #                            termination_patience=termination_patience,
        #                            termination_frac_likelihood_improvement=termination_frac_likelihood_improvement,
        #                            termination_likelihood_contour=termination_likelihood_contour,
        #                            termination_max_num_steps=termination_max_num_steps,
        #                            termination_max_num_likelihood_evaluations=termination_max_num_likelihood_evaluations
        #                            )

        X_test = self.prior_chain(U_test)
        return U_test, X_test
