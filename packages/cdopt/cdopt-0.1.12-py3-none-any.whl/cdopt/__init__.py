__all__ = ["core", "manifold", "manifold_np", "manifold_torch"]
__author__ = 'Nachuan Xiao, Xiaoyin Hu, Xin Liu, and Kim-Chuan Toh'

from . import manifold_np,  manifold
from .core import problem, backbone_autograd, backbone_torch

try:
    import torch
    from . import manifold_torch
    from . import utils_torch
except ImportError:
    print('No torch package installed')


try:
    import jax 
    from .core  import backbone_jax
except ImportError:
    print('No JAX package installed')
