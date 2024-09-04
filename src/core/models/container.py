from typing import Any, Dict, List
from datetime import datetime
from .base_model import BaseModel

class Container(BaseModel):
    """
    Model representing a Docker container.
    """

    def __init__(self, id: str, name: str, image: str, status: str,
                 created: datetime, ports: Dict[str, List[Dict[str, str]]]):
        self.id = id
        self.name = name
        self.image = image
        self.status = status
        self.created = created
        self.ports = ports

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the Container instance to a dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the Container.
        """
        return {
            "id": self.id,
            "name": self.name,
            "image": self.image,
            "status": self.status,
            "created": self.created.isoformat(),
            "ports": self.ports
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Container':
        """
        Create a Container instance from a dictionary.

        Args:
            data (Dict[str, Any]): The dictionary containing the Container data.

        Returns:
            Container: An instance of the Container model.
        """
        return cls(
            id=data["id"],
            name=data["name"],
            image=data["image"],
            status=data["status"],
            created=datetime.fromisoformat(data["created"]),
            ports=data["ports"]
        )