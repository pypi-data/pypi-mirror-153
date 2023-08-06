from .registry import DependenciesRegistry

__INJECTME_REGISTRY = None


def _reset_registry():
    global __INJECTME_REGISTRY
    __INJECTME_REGISTRY = None


def _get_current_global_registry():
    return __INJECTME_REGISTRY


def set_registry(registry):
    global __INJECTME_REGISTRY
    __INJECTME_REGISTRY = registry


def get_registry():
    global __INJECTME_REGISTRY
    if __INJECTME_REGISTRY is None:
        __INJECTME_REGISTRY = DependenciesRegistry()

    return __INJECTME_REGISTRY


def register(dependency, instance):
    registry = get_registry()
    registry.register_instance(dependency, instance)


def register_factory(dependency, factory):
    registry = get_registry()
    registry.register_factory(dependency, factory)
