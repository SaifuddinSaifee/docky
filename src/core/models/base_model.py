from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseModel(ABC):
    """
    Abstract base class for all data models in the application.
    """

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the model instance to a dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the model.
        """
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BaseModel':
        """
        Create a model instance from a dictionary.

        Args:
            data (Dict[str, Any]): The dictionary containing the model data.

        Returns:
            BaseModel: An instance of the model.
        """
        pass

    def __repr__(self) -> str:
        """
        Return a string representation of the model.

        Returns:
            str: A string representation of the model.
        """
        return f"{self.__class__.__name__}({self.to_dict()})"