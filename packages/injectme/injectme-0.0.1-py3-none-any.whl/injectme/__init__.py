from .decorator import inject
from .global_registry import register, register_factory, set_registry, get_registry
from .registry import DependenciesRegistry
from .errors import (
    DependencyNotFound,
    DependencyAlreadyRegistered,
    InjectionNotSupported,
    InjectionFailure,
    InjectmeException,
)


__all__ = [
    "inject",
    "register",
    "register_factory",
    "set_registry",
    "get_registry",
    "DependenciesRegistry",
    "DependencyNotFound",
    "DependencyAlreadyRegistered",
    "InjectionNotSupported",
    "InjectionFailure",
    "InjectmeException",
]

__version__ = "0.0.1"

