from dataclasses import dataclass
from enum import Enum
from typing import Any, MutableMapping, Union, cast

from .errors import DependencyNotFound, DependencyAlreadyRegistered


class DependencyType(Enum):
    INSTANCE = 1
    FACTORY = 2


@dataclass
class RegistryEntry:
    dependency_type: DependencyType
    dependency_value: Any

    @classmethod
    def factory(cls, factory) -> "RegistryEntry":
        return cls(
            dependency_type=DependencyType.FACTORY,
            dependency_value=factory,
        )

    @classmethod
    def instance(cls, instance) -> "RegistryEntry":
        return cls(
            dependency_type=DependencyType.INSTANCE,
            dependency_value=instance,
        )


class DependenciesRegistry:
    def __init__(self):
        self._dependencies = {}

    def get(self, dependency):
        entry = self._dependencies.get(dependency)
        if entry is None:
            raise DependencyNotFound(dependency)

        if entry.dependency_type == DependencyType.FACTORY:
            return entry.dependency_value()

        return entry.dependency_value

    def register_instance(self, dependency, instance):
        self._ensure_not_registered(dependency)
        entry = RegistryEntry.instance(instance)
        self._dependencies[dependency] = entry

    def register_factory(self, dependency, factory):
        self._ensure_not_registered(dependency)
        entry = RegistryEntry.factory(factory)
        self._dependencies[dependency] = entry

    def _ensure_not_registered(self, dependency):
        if dependency in self._dependencies:
            raise DependencyAlreadyRegistered(dependency)
