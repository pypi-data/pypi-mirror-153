from abc import ABC, abstractmethod


class Engine(ABC):
    """Abstract class for the projection engine."""

    @abstractmethod
    def project():
        """Projects a combination of year, place and age."""

    @abstractmethod
    def project_all():
        """Projects all combinations of year, place and age possible"""
