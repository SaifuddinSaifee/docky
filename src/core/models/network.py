from typing import Any, Dict
from datetime import datetime
from .base_model import BaseModel

class Network(BaseModel):
    """
    Model representing a Docker network.
    """

    def __init__(self, id: str, name: str, driver: str, scope: str, created: datetime):
        self.id = id
        self.name = name
        self.driver = driver
        self.scope = scope
        self.created = created

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the Network instance to a dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the Network.
        """
        return {
            "id": self.id,
            "name": self.name,
            "driver": self.driver,
            "scope": self.scope,
            "created": self.created.isoformat()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Network':
        """
        Create a Network instance from a dictionary.

        Args:
            data (Dict[str, Any]): The dictionary containing the Network data.

        Returns:
            Network: An instance of the Network model.
        """
        return cls(
            id=data["id"],
            name=data["name"],
            driver=data["driver"],
            scope=data["scope"],
            created=datetime.fromisoformat(data["created"])
        )