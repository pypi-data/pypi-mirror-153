from .global_registry import get_registry as get_global_registry
from .registry import DependenciesRegistry
from .errors import InjectionFailure, InjectionNotSupported, DependencyNotFound


def inject(target):
    if isinstance(target, DependenciesRegistry):
        registry = target
        return _inject_local_registry(registry)

    if isinstance(target, type):
        cls = target
        return _inject_global_registry(cls)

    raise InjectionNotSupported(target)


def _inject_local_registry(registry: DependenciesRegistry):
    get_registry = lambda: registry
    return _get_cls_decorator(get_registry)


def _inject_global_registry(cls: type):
    cls_decorator = _get_cls_decorator(get_global_registry)
    return cls_decorator(cls)


def _get_cls_decorator(get_registry):
    def inject_inner(cls):
        def __init_deps__(self, cls):
            annotations = cls.__dict__.get("__annotations__", {})
            registry = get_registry()

            try:
                for name, type in annotations.items():
                    dependency = registry.get(type)
                    setattr(self, name, dependency)
            except DependencyNotFound as e:
                raise InjectionFailure(cls) from e

        def injectme_init(self, *args, **kwargs):
            cls.__init_deps__(self, cls)
            cls.__original_init__(self, *args, **kwargs)

        cls.__original_init__ = cls.__init__
        cls.__init_deps__ = __init_deps__
        cls.__init__ = injectme_init

        return cls

    return inject_inner
