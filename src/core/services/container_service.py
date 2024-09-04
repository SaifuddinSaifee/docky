import subprocess
import json
import logging
from typing import List, Tuple, Optional
from src.core.models.container import Container

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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

def get_containers() -> List[Container]:
    """
    Get a list of all Docker containers.

    Returns:
        List[Container]: A list of Container objects.
    """
    success, output = run_docker_command(["ps", "-a", "--format", "{{json .}}"])
    if not success:
        logger.error("Failed to get containers")
        return []

    containers = []
    for line in output.split('\n'):
        if line:
            try:
                container_data = json.loads(line)
                containers.append(Container.from_dict(container_data))
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse container data: {e}")
            except KeyError as e:
                logger.error(f"Missing key in container data: {e}")
    return containers

def get_container_by_id(container_id: str) -> Optional[Container]:
    """
    Get a specific container by its ID.

    Args:
        container_id (str): The ID of the container to retrieve.

    Returns:
        Optional[Container]: The Container object if found, None otherwise.
    """
    success, output = run_docker_command(["inspect", "--format", "{{json .}}", container_id])
    if not success:
        logger.error(f"Failed to get container with ID {container_id}")
        return None

    try:
        container_data = json.loads(output)
        return Container.from_dict(container_data)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse container data: {e}")
    except KeyError as e:
        logger.error(f"Missing key in container data: {e}")
    return None

def start_container(container_id: str) -> bool:
    """
    Start a Docker container.

    Args:
        container_id (str): The ID of the container to start.

    Returns:
        bool: True if the container was successfully started, False otherwise.
    """
    success, output = run_docker_command(["start", container_id])
    if success:
        logger.info(f"Container {container_id} started successfully")
    else:
        logger.error(f"Failed to start container {container_id}")
    return success

def stop_container(container_id: str) -> bool:
    """
    Stop a Docker container.

    Args:
        container_id (str): The ID of the container to stop.

    Returns:
        bool: True if the container was successfully stopped, False otherwise.
    """
    success, output = run_docker_command(["stop", container_id])
    if success:
        logger.info(f"Container {container_id} stopped successfully")
    else:
        logger.error(f"Failed to stop container {container_id}")
    return success

def remove_container(container_id: str, force: bool = False) -> bool:
    """
    Remove a Docker container.

    Args:
        container_id (str): The ID of the container to remove.
        force (bool): If True, force the removal of the container.

    Returns:
        bool: True if the container was successfully removed, False otherwise.
    """
    command = ["rm", container_id]
    if force:
        command.insert(1, "-f")
    
    success, output = run_docker_command(command)
    if success:
        logger.info(f"Container {container_id} removed successfully")
    else:
        logger.error(f"Failed to remove container {container_id}")
    return success

def get_container_logs(container_id: str, tail: Optional[int] = None) -> Optional[str]:
    """
    Get the logs of a Docker container.

    Args:
        container_id (str): The ID of the container to get logs from.
        tail (Optional[int]): If provided, only return this number of lines from the end of the logs.

    Returns:
        Optional[str]: The container logs if successful, None otherwise.
    """
    command = ["logs", container_id]
    if tail is not None:
        command.extend(["--tail", str(tail)])
    
    success, output = run_docker_command(command)
    if success:
        return output
    else:
        logger.error(f"Failed to get logs for container {container_id}")
        return None

# Add more container-related functions as needed