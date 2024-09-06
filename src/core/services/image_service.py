import subprocess
import json
import logging
from typing import List, Tuple, Optional
from ..models.image import Image

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

def get_images() -> List[Image]:
    """
    Get a list of all Docker images.

    Returns:
        List[Image]: A list of Image objects.
    """
    success, output = run_docker_command(["images", "--format", "{{json .}}"])
    if not success:
        logger.error("Failed to get images")
        return []

    images = []
    for line in output.split('\n'):
        if line:
            try:
                image_data = json.loads(line)
                images.append(Image.from_dict(image_data))
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse image data: {e}")
            except KeyError as e:
                logger.error(f"Missing key in image data: {e}")
    return images

def get_image_by_id(image_id: str) -> Optional[Image]:
    """
    Get a specific image by its ID.

    Args:
        image_id (str): The ID of the image to retrieve.

    Returns:
        Optional[Image]: The Image object if found, None otherwise.
    """
    success, output = run_docker_command(["inspect", "--format", "{{json .}}", image_id])
    if not success:
        logger.error(f"Failed to get image with ID {image_id}")
        return None

    try:
        image_data = json.loads(output)
        return Image.from_dict(image_data)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse image data: {e}")
    except KeyError as e:
        logger.error(f"Missing key in image data: {e}")
    return None

def pull_image(image_name: str) -> bool:
    """
    Pull a Docker image from a registry.

    Args:
        image_name (str): The name of the image to pull.

    Returns:
        bool: True if the image was successfully pulled, False otherwise.
    """
    success, output = run_docker_command(["pull", image_name])
    if success:
        logger.info(f"Image {image_name} pulled successfully")
    else:
        logger.error(f"Failed to pull image {image_name}")
    return success

def remove_image(image_id: str, force: bool = False) -> bool:
    """
    Remove a Docker image.

    Args:
        image_id (str): The ID of the image to remove.
        force (bool): If True, force the removal of the image.

    Returns:
        bool: True if the image was successfully removed, False otherwise.
    """
    command = ["rmi", image_id]
    if force:
        command.insert(1, "-f")
    
    success, output = run_docker_command(command)
    if success:
        logger.info(f"Image {image_id} removed successfully")
    else:
        logger.error(f"Failed to remove image {image_id}")
    return success

def tag_image(image_id: str, new_tag: str) -> bool:
    """
    Tag a Docker image.

    Args:
        image_id (str): The ID of the image to tag.
        new_tag (str): The new tag to apply to the image.

    Returns:
        bool: True if the image was successfully tagged, False otherwise.
    """
    success, output = run_docker_command(["tag", image_id, new_tag])
    if success:
        logger.info(f"Image {image_id} tagged as {new_tag} successfully")
    else:
        logger.error(f"Failed to tag image {image_id} as {new_tag}")
    return success

def push_image(image_name: str) -> bool:
    """
    Push a Docker image to a registry.

    Args:
        image_name (str): The name of the image to push.

    Returns:
        bool: True if the image was successfully pushed, False otherwise.
    """
    success, output = run_docker_command(["push", image_name])
    if success:
        logger.info(f"Image {image_name} pushed successfully")
    else:
        logger.error(f"Failed to push image {image_name}")
    return success

# Add more image-related functions as needed