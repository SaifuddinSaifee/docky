import subprocess
import shutil
from typing import Tuple, List, Optional
import logging
import platform

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DockerEngineManager:
    """
    A class to manage Docker engine operations using subprocess.
    """

    @staticmethod
    def is_docker_installed() -> bool:
        """
        Check if Docker is installed on the system.

        Returns:
            bool: True if Docker is installed, False otherwise.
        """
        return shutil.which('docker') is not None

    @staticmethod
    def is_docker_running() -> bool:
        """
        Check if the Docker engine is currently running.

        Returns:
            bool: True if Docker is running, False otherwise.
        """
        try:
            subprocess.run(["docker", "info"], capture_output=True, check=True)
            return True
        except subprocess.CalledProcessError:
            return False

    @classmethod
    def start_docker_engine(cls) -> bool:
        """
        Attempt to start the Docker engine.

        Returns:
            bool: True if Docker was successfully started, False otherwise.
        """
        if cls.is_docker_running():
            logger.info("Docker is already running.")
            return True

        system = platform.system()
        if system == "Linux":
            return cls._start_docker_linux()
        elif system == "Darwin":  # macOS
            return cls._start_docker_macos()
        elif system == "Windows":
            return cls._start_docker_windows()
        else:
            logger.error(f"Unsupported operating system: {system}")
            return False

    @staticmethod
    def _start_docker_linux() -> bool:
        """
        Start Docker on Linux systems.

        Returns:
            bool: True if Docker was successfully started, False otherwise.
        """
        try:
            subprocess.run(["sudo", "systemctl", "start", "docker"], check=True)
            logger.info("Docker started successfully on Linux.")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to start Docker on Linux: {e}")
            return False

    @staticmethod
    def _start_docker_macos() -> bool:
        """
        Start Docker on macOS systems.

        Returns:
            bool: True if Docker was successfully started, False otherwise.
        """
        try:
            subprocess.run(["open", "-a", "Docker"], check=True)
            logger.info("Docker started successfully on macOS.")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to start Docker on macOS: {e}")
            return False

    @staticmethod
    def _start_docker_windows() -> bool:
        """
        Start Docker on Windows systems.

        Returns:
            bool: True if Docker was successfully started, False otherwise.
        """
        try:
            subprocess.run(["start", "docker"], shell=True, check=True)
            logger.info("Docker started successfully on Windows.")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to start Docker on Windows: {e}")
            return False

    @staticmethod
    def stop_docker_engine() -> bool:
        """
        Attempt to stop the Docker engine.

        Returns:
            bool: True if Docker was successfully stopped, False otherwise.
        """
        try:
            subprocess.run(["docker", "stop"], capture_output=True, check=True)
            logger.info("Docker stopped successfully.")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to stop Docker: {e}")
            return False

    @staticmethod
    def get_docker_version() -> Optional[str]:
        """
        Get the installed Docker version.

        Returns:
            Optional[str]: The Docker version string, or None if it couldn't be retrieved.
        """
        try:
            result = subprocess.run(["docker", "--version"], capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to get Docker version: {e}")
            return None

    @staticmethod
    def run_docker_command(command: List[str]) -> Tuple[bool, str]:
        """
        Execute a Docker command using subprocess.

        Args:
            command (List[str]): The Docker command to execute.

        Returns:
            Tuple[bool, str]: A tuple containing a boolean indicating success and the output string.
        """
        try:
            result = subprocess.run(["docker"] + command, capture_output=True, text=True, check=True)
            return True, result.stdout.strip()
        except subprocess.CalledProcessError as e:
            error_message = f"Error executing Docker command: {e.stderr.strip()}"
            logger.error(error_message)
            return False, error_message

    @classmethod
    def ensure_docker_running(cls) -> bool:
        """
        Ensure that Docker is installed and running, attempting to start it if it's not.

        Returns:
            bool: True if Docker is running after this method, False otherwise.
        """
        if not cls.is_docker_installed():
            logger.error("Docker is not installed on this system.")
            return False

        if not cls.is_docker_running():
            logger.info("Docker is not running. Attempting to start...")
            return cls.start_docker_engine()

        return True

# Example usage
if __name__ == "__main__":
    docker_manager = DockerEngineManager()

    if docker_manager.ensure_docker_running():
        print("Docker is up and running!")
        version = docker_manager.get_docker_version()
        if version:
            print(f"Docker version: {version}")

        # Example of running a custom Docker command
        print("\nRunning 'docker info' command:")
        success, output = docker_manager.run_docker_command(["info"])
        if success:
            print(output)
        else:
            print("Failed to run 'docker info' command.")
    else:
        print("Failed to ensure Docker is running.")