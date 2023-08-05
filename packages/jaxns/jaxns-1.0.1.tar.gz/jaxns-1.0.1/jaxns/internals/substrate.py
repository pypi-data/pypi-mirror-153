from enum import Enum, auto
from typing import Union

import numpy as np


class Backend(Enum):
    JAX = auto()
    NUMPY = auto()
    TENSORFLOW = auto()

def get_backend(backend: Union[Backend, str]) -> Backend:
    if isinstance(backend, Backend):
        return backend
    if backend.lower() == 'jax':
        return Backend.JAX
    elif backend.lower() == 'numpy':
        return Backend.NUMPY
    elif backend.lower() == 'tensorflow':
        return Backend.TENSORFLOW
    else:
        raise ValueError(f"Backend {backend} invalid.")

def test_get_backend():
    assert get_backend('jax') == Backend.JAX
    assert get_backend('numpy') == Backend.NUMPY
    assert get_backend('tensorflow') == Backend.TENSORFLOW
    assert get_backend(Backend.JAX) == Backend.JAX
    assert get_backend(Backend.NUMPY) == Backend.NUMPY
    assert get_backend(Backend.TENSORFLOW) == Backend.TENSORFLOW

methods = [
    'asarray',
    'array',
    'int64',
    'int32',
    'float32',
    'float64'
]
class Substrate(object):
    def __init__(self, backend: Union[Backend, str]):
        self.backend = get_backend(backend)
        print(self.backend)
        print(backend)
        if self.backend == Backend.JAX:
            from jax import numpy
            _np = numpy
        elif self.backend == Backend.NUMPY:
            import numpy
            _np = numpy
        elif self.backend == Backend.TENSORFLOW:
            import tensorflow
            _np = tensorflow
        else:
            raise ValueError(f"Backend {self.backend} in valid")
        self._np = _np

    @property
    def np(self):
        return self._np

    def __getattribute__(self, item):
        return


def test_substrate():
    import numpy as tnp

    for backend in ['numpy', 'jax', 'tensorflow']:
        st = Substrate(backend)
        snp = st.np

        def test_unary_op(substrate_func, func, x):
            assert np.allclose(substrate_func(x), func(x))

        _unary_ops = [obj for obj in tnp if isinstance(obj, callable)]
        print(_unary_ops)
        # unary_ops = dict( )


