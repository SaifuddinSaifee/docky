from dataclasses import dataclass
from typing import Optional

@dataclass
class Volume:
    """
    Represents a Docker volume.
    """
    name: str
    driver: str
    mountpoint: str
    labels: str
    scope: str
    availability: str
    group: str
    links: str
    size: str
    status: str

    @classmethod
    def from_dict(cls, data: dict) -> 'Volume':
        """
        Create a Volume instance from a dictionary.

        Args:
            data (dict): Dictionary containing volume data.

        Returns:
            Volume: A new Volume instance.
        """
        return cls(
            name=data['Name'],
            driver=data['Driver'],
            mountpoint=data['Mountpoint'],
            labels=data['Labels'],
            scope=data['Scope'],
            availability=data['Availability'],
            group=data['Group'],
            links=data['Links'],
            size=data['Size'],
            status=data['Status']
        )

    def __str__(self) -> str:
        """
        Return a string representation of the Volume.

        Returns:
            str: A string representation of the Volume.
        """
        return f"Volume(name={self.name}, driver={self.driver}, scope={self.scope})"