# src/models/image.py

from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Image:
    """
    Represents a Docker image.
    """
    id: str
    repository: str
    tag: str
    created_at: datetime
    created_since: str
    size: str
    virtual_size: str
    shared_size: str
    unique_size: str
    containers: str
    digest: str

    @classmethod
    def from_dict(cls, data: dict) -> 'Image':
        """
        Create an Image instance from a dictionary.

        Args:
            data (dict): Dictionary containing image data.

        Returns:
            Image: A new Image instance.
        """
        return cls(
            id=data['ID'],
            repository=data['Repository'],
            tag=data['Tag'],
            created_at=datetime.strptime(data['CreatedAt'], "%Y-%m-%d %H:%M:%S %z %Z"),
            created_since=data['CreatedSince'],
            size=data['Size'],
            virtual_size=data['VirtualSize'],
            shared_size=data['SharedSize'],
            unique_size=data['UniqueSize'],
            containers=data['Containers'],
            digest=data['Digest']
        )

    def __str__(self) -> str:
        """
        Return a string representation of the Image.

        Returns:
            str: A string representation of the Image.
        """
        return f"Image(id={self.id[:12]}, repository={self.repository}, tag={self.tag})"