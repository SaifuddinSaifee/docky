# src/models/container.py

from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class Container:
    """
    Represents a Docker container.
    """
    id: str
    name: str
    image: str
    status: str
    state: str
    created: datetime
    ports: str
    command: str
    labels: str
    networks: str
    mounts: str
    size: str
    created_at: str
    running_for: str

    @classmethod
    def from_dict(cls, data: dict) -> 'Container':
        """
        Create a Container instance from a dictionary.

        Args:
            data (dict): Dictionary containing container data.

        Returns:
            Container: A new Container instance.
        """
        return cls(
            id=data['ID'],
            name=data['Names'],
            image=data['Image'],
            status=data['Status'],
            state=data['State'],
            created=datetime.strptime(data['CreatedAt'], "%Y-%m-%d %H:%M:%S %z %Z"),
            ports=data['Ports'],
            command=data['Command'],
            labels=data['Labels'],
            networks=data['Networks'],
            mounts=data['Mounts'],
            size=data['Size'],
            created_at=data['CreatedAt'],
            running_for=data['RunningFor']
        )

    def __str__(self) -> str:
        """
        Return a string representation of the Container.

        Returns:
            str: A string representation of the Container.
        """
        return f"Container(id={self.id[:12]}, name={self.name}, status={self.status})"