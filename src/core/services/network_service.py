import subprocess
import json
import logging
from typing import List, Tuple, Optional
from models.network import Network

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

def get_networks() -> List[Network]:
    """
    Get a list of all Docker networks.

    Returns:
        List[Network]: A list of Network objects.
    """
    success, output = run_docker_command(["network", "ls", "--format", "{{json .}}"])
    if not success:
        logger.error("Failed to get networks")
        return []

    networks = []
    for line in output.split('\n'):
        if line:
            try:
                network_data = json.loads(line)
                networks.append(Network.from_dict(network_data))
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse network data: {e}")
            except KeyError as e:
                logger.error(f"Missing key in network data: {e}")
    return networks

def get_network_by_id(network_id: str) -> Optional[Network]:
    """
    Get a specific network by its ID.

    Args:
        network_id (str): The ID of the network to retrieve.

    Returns:
        Optional[Network]: The Network object if found, None otherwise.
    """
    success, output = run_docker_command(["network", "inspect", "--format", "{{json .}}", network_id])
    if not success:
        logger.error(f"Failed to get network with ID {network_id}")
        return None

    try:
        network_data = json.loads(output)
        return Network.from_dict(network_data[0])  # network inspect returns a list
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse network data: {e}")
    except KeyError as e:
        logger.error(f"Missing key in network data: {e}")
    except IndexError:
        logger.error(f"No network data returned for ID {network_id}")
    return None

def create_network(name: str, driver: str = "bridge", options: Optional[dict] = None) -> bool:
    """
    Create a new Docker network.

    Args:
        name (str): The name of the network to create.
        driver (str): The driver to use for the network (default: "bridge").
        options (Optional[dict]): Additional options for network creation.

    Returns:
        bool: True if the network was successfully created, False otherwise.
    """
    command = ["network", "create", "--driver", driver]
    if options:
        for key, value in options.items():
            command.extend(["--opt", f"{key}={value}"])
    command.append(name)

    success, output = run_docker_command(command)
    if success:
        logger.info(f"Network {name} created successfully")
    else:
        logger.error(f"Failed to create network {name}")
    return success

def remove_network(network_id: str) -> bool:
    """
    Remove a Docker network.

    Args:
        network_id (str): The ID of the network to remove.

    Returns:
        bool: True if the network was successfully removed, False otherwise.
    """
    success, output = run_docker_command(["network", "rm", network_id])
    if success:
        logger.info(f"Network {network_id} removed successfully")
    else:
        logger.error(f"Failed to remove network {network_id}")
    return success

def connect_container_to_network(container_id: str, network_id: str) -> bool:
    """
    Connect a container to a network.

    Args:
        container_id (str): The ID of the container to connect.
        network_id (str): The ID of the network to connect to.

    Returns:
        bool: True if the container was successfully connected, False otherwise.
    """
    success, output = run_docker_command(["network", "connect", network_id, container_id])
    if success:
        logger.info(f"Container {container_id} connected to network {network_id} successfully")
    else:
        logger.error(f"Failed to connect container {container_id} to network {network_id}")
    return success

def disconnect_container_from_network(container_id: str, network_id: str) -> bool:
    """
    Disconnect a container from a network.

    Args:
        container_id (str): The ID of the container to disconnect.
        network_id (str): The ID of the network to disconnect from.

    Returns:
        bool: True if the container was successfully disconnected, False otherwise.
    """
    success, output = run_docker_command(["network", "disconnect", network_id, container_id])
    if success:
        logger.info(f"Container {container_id} disconnected from network {network_id} successfully")
    else:
        logger.error(f"Failed to disconnect container {container_id} from network {network_id}")
    return success

def prune_networks() -> bool:
    """
    Remove all unused networks.

    Returns:
        bool: True if unused networks were successfully removed, False otherwise.
    """
    success, output = run_docker_command(["network", "prune", "-f"])
    if success:
        logger.info("Unused networks pruned successfully")
    else:
        logger.error("Failed to prune unused networks")
    return success

# Add more network-related functions as needed