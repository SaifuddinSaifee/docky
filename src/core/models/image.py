from typing import Any, Dict, List
from datetime import datetime
from .base_model import BaseModel

class Image(BaseModel):
    """
    Model representing a Docker image.
    """

    def __init__(self, id: str, tags: List[str], created: datetime, size: int):
        self.id = id
        self.tags = tags
        self.created = created
        self.size = size

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the Image instance to a dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the Image.
        """
        return {
            "id": self.id,
            "tags": self.tags,
            "created": self.created.isoformat(),
            "size": self.size
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Image':
        """
        Create an Image instance from a dictionary.

        Args:
            data (Dict[str, Any]): The dictionary containing the Image data.

        Returns:
            Image: An instance of the Image model.
        """
        return cls(
            id=data["id"],
            tags=data["tags"],
            created=datetime.fromisoformat(data["created"]),
            size=data["size"]
        )