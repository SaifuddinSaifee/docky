from typing import Any, Dict
from datetime import datetime
from .base_model import BaseModel

class Volume(BaseModel):
    """
    Model representing a Docker volume.
    """

    def __init__(self, name: str, driver: str, mountpoint: str, created: datetime):
        self.name = name
        self.driver = driver
        self.mountpoint = mountpoint
        self.created = created

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the Volume instance to a dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the Volume.
        """
        return {
            "name": self.name,
            "driver": self.driver,
            "mountpoint": self.mountpoint,
            "created": self.created.isoformat()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Volume':
        """
        Create a Volume instance from a dictionary.

        Args:
            data (Dict[str, Any]): The dictionary containing the Volume data.

        Returns:
            Volume: An instance of the Volume model.
        """
        return cls(
            name=data["name"],
            driver=data["driver"],
            mountpoint=data["mountpoint"],
            created=datetime.fromisoformat(data["created"])
        )