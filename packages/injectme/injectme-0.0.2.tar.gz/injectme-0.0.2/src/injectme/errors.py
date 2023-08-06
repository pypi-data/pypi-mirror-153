class InjectmeException(Exception):
    pass


class DependencyNotFound(InjectmeException):
    def __init__(self, dependency):
        super().__init__(f"Dependency {dependency} has not been found in the registry")


class DependencyAlreadyRegistered(InjectmeException):
    def __init__(self, dependency):
        super().__init__(f"Dependency {dependency} already registered")


class InjectionNotSupported(InjectmeException):
    def __init__(self, target):
        super().__init__(f"unsopported injection target {target}")


class InjectionFailure(InjectmeException):
    def __init__(self, cls):
        super().__init__(f"failed to inject deps into {cls}")
