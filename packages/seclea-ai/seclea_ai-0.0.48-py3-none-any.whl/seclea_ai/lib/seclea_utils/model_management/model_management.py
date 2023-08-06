from abc import ABC, abstractmethod
from typing import Any


class ModelManager(ABC):
    @staticmethod
    @abstractmethod
    def encode(model: Any) -> bytes:
        """
        Saves a model at the specified reference.
        :param model: model to save
        :return: Where it was saved.
        """
        pass

    @staticmethod
    @abstractmethod
    def decode(data: bytes) -> Any:
        """
        :param data:
        :return: The model.
        """
        pass

    @staticmethod
    @abstractmethod
    def get_params(model):
        """
        Gets the model parameters for a given model.
        """
        pass
