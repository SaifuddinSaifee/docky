import subprocess
import json
import logging
from typing import List, Tuple, Optional
from ..models.volume import Volume

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

def get_volumes() -> List[Volume]:
    """
    Get a list of all Docker volumes.

    Returns:
        List[Volume]: A list of Volume objects.
    """
    success, output = run_docker_command(["volume", "ls", "--format", "{{json .}}"])
    if not success:
        logger.error("Failed to get volumes")
        return []

    volumes = []
    for line in output.split('\n'):
        if line:
            try:
                volume_data = json.loads(line)
                volumes.append(Volume.from_dict(volume_data))
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse volume data: {e}")
            except KeyError as e:
                logger.error(f"Missing key in volume data: {e}")
    return volumes

def get_volume_by_name(volume_name: str) -> Optional[Volume]:
    """
    Get a specific volume by its name.

    Args:
        volume_name (str): The name of the volume to retrieve.

    Returns:
        Optional[Volume]: The Volume object if found, None otherwise.
    """
    success, output = run_docker_command(["volume", "inspect", "--format", "{{json .}}", volume_name])
    if not success:
        logger.error(f"Failed to get volume with name {volume_name}")
        return None

    try:
        volume_data = json.loads(output)
        return Volume.from_dict(volume_data[0])  # volume inspect returns a list
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse volume data: {e}")
    except KeyError as e:
        logger.error(f"Missing key in volume data: {e}")
    except IndexError:
        logger.error(f"No volume data returned for name {volume_name}")
    return None

def create_volume(name: str, driver: str = "local", options: Optional[dict] = None) -> bool:
    """
    Create a new Docker volume.

    Args:
        name (str): The name of the volume to create.
        driver (str): The driver to use for the volume (default: "local").
        options (Optional[dict]): Additional options for volume creation.

    Returns:
        bool: True if the volume was successfully created, False otherwise.
    """
    command = ["volume", "create", "--driver", driver]
    if options:
        for key, value in options.items():
            command.extend(["--opt", f"{key}={value}"])
    command.append(name)

    success, output = run_docker_command(command)
    if success:
        logger.info(f"Volume {name} created successfully")
    else:
        logger.error(f"Failed to create volume {name}")
    return success

def remove_volume(volume_name: str, force: bool = False) -> bool:
    """
    Remove a Docker volume.

    Args:
        volume_name (str): The name of the volume to remove.
        force (bool): If True, force the removal of the volume.

    Returns:
        bool: True if the volume was successfully removed, False otherwise.
    """
    command = ["volume", "rm"]
    if force:
        command.append("-f")
    command.append(volume_name)

    success, output = run_docker_command(command)
    if success:
        logger.info(f"Volume {volume_name} removed successfully")
    else:
        logger.error(f"Failed to remove volume {volume_name}")
    return success

def prune_volumes() -> bool:
    """
    Remove all unused volumes.

    Returns:
        bool: True if unused volumes were successfully removed, False otherwise.
    """
    success, output = run_docker_command(["volume", "prune", "-f"])
    if success:
        logger.info("Unused volumes pruned successfully")
    else:
        logger.error("Failed to prune unused volumes")
    return success

def get_volume_usage(volume_name: str) -> Optional[str]:
    """
    Get the disk usage of a specific volume.

    Args:
        volume_name (str): The name of the volume to check.

    Returns:
        Optional[str]: The disk usage of the volume if successful, None otherwise.
    """
    success, output = run_docker_command(["system", "df", "-v", "--format", "{{json .}}", "--filter", f"type=volume"])
    if not success:
        logger.error(f"Failed to get volume usage for {volume_name}")
        return None

    try:
        for line in output.split('\n'):
            data = json.loads(line)
            if data.get('Name') == volume_name:
                return data.get('Size')
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse volume usage data: {e}")
    except KeyError as e:
        logger.error(f"Missing key in volume usage data: {e}")

    logger.error(f"Volume {volume_name} not found in usage data")
    return None

def copy_volume(source_volume: str, destination_volume: str) -> bool:
    """
    Copy the contents of one volume to another.

    Args:
        source_volume (str): The name of the source volume.
        destination_volume (str): The name of the destination volume.

    Returns:
        bool: True if the volume was successfully copied, False otherwise.
    """
    # This operation requires creating a temporary container
    command = [
        "run", "--rm", 
        "-v", f"{source_volume}:/from", 
        "-v", f"{destination_volume}:/to", 
        "alpine", "ash", "-c", "cp -av /from/. /to"
    ]
    
    success, output = run_docker_command(command)
    if success:
        logger.info(f"Volume {source_volume} copied to {destination_volume} successfully")
    else:
        logger.error(f"Failed to copy volume {source_volume} to {destination_volume}")
    return success

# Add more volume-related functions as needed