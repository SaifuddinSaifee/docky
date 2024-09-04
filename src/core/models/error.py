from typing import Any, Dict, Optional
from enum import Enum


class ErrorType(Enum):
    """Enum representing different types of errors in the application."""
    DOCKER_CONNECTION = "docker_connection"
    DOCKER_API = "docker_api"
    INVALID_INPUT = "invalid_input"
    RESOURCE_NOT_FOUND = "resource_not_found"
    PERMISSION_DENIED = "permission_denied"
    UNEXPECTED = "unexpected"


class DockyError(Exception):
    """
    Custom error class for the Docky application.

    This class extends the built-in Exception class to provide more
    structured error information.
    """

    def __init__(self,
                 error_type: ErrorType,
                 message: str,
                 details: Optional[Dict[str, Any]] = None):
        """
        Initialize a new DockyError.

        Args:
            error_type (ErrorType): The type of the error.
            message (str): A human-readable error message.
            details (Optional[Dict[str, Any]]): Additional error details.
        """
        self.error_type = error_type
        self.message = message
        self.details = details or {}
        super().__init__(self.message)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the error to a dictionary representation.

        Returns:
            Dict[str, Any]: A dictionary containing error information.
        """
        return {
            "error_type": self.error_type.value,
            "message": self.message,
            "details": self.details
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DockyError':
        """
        Create a DockyError instance from a dictionary.

        Args:
            data (Dict[str, Any]): The dictionary containing error data.

        Returns:
            DockyError: An instance of DockyError.
        """
        return cls(
            error_type=ErrorType(data["error_type"]),
            message=data["message"],
            details=data.get("details")
        )

    def __str__(self) -> str:
        """
        Return a string representation of the error.

        Returns:
            str: A string representation of the error.
        """
        return f"{self.error_type.value.upper()}: {self.message}"

# Example usage:
# raise DockyError(ErrorType.DOCKER_CONNECTION, "Failed to connect to Docker daemon", {"host": "localhost", "port": 2375})