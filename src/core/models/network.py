# src/models/network.py

from dataclasses import dataclass
from datetime import datetime
import re

@dataclass
class Network:
    """
    Represents a Docker network.
    """
    id: str
    name: str
    driver: str
    scope: str
    ipv6: str
    internal: str
    labels: str
    created_at: datetime

    @classmethod
    def from_dict(cls, data: dict) -> 'Network':
        """
        Create a Network instance from a dictionary.

        Args:
            data (dict): Dictionary containing network data.

        Returns:
            Network: A new Network instance.
        """
        # Parse the CreatedAt string to remove the nanoseconds
        created_at_str = re.sub(r'(\.\d{6})\d+', r'\1', data['CreatedAt'])
        created_at = datetime.strptime(created_at_str, "%Y-%m-%d %H:%M:%S.%f %z %Z")

        return cls(
            id=data['ID'],
            name=data['Name'],
            driver=data['Driver'],
            scope=data['Scope'],
            ipv6=data['IPv6'],
            internal=data['Internal'],
            labels=data['Labels'],
            created_at=created_at
        )

    def __str__(self) -> str:
        """
        Return a string representation of the Network.

        Returns:
            str: A string representation of the Network.
        """
        return f"Network(id={self.id[:12]}, name={self.name}, driver={self.driver})"