import asyncio
from typing import List, Dict, Any, Optional

import docker
from docker.errors import APIError, DockerException
import structlog

logger = structlog.get_logger()

class DockerClient:
    """
    A class to interact with the Docker daemon.
    This class provides methods for basic Docker operations such as
    listing containers, images, volumes, and networks.
    """

    def __init__(self):
        """
        Initialize the Docker client.
        """
        try:
            self.client = docker.from_env()
            logger.info("Docker client initialized successfully")
        except DockerException as e:
            logger.error("Failed to initialize Docker client", error=str(e))
            raise

    async def list_containers(self, all: bool = False) -> List[Dict[str, Any]]:
        """
        List Docker containers.

        Args:
            all (bool): If True, list all containers. If False, list only running containers.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing container information.
        """
        try:
            containers = await asyncio.to_thread(self.client.containers.list, all=all)
            return [self._format_container_info(container) for container in containers]
        except APIError as e:
            logger.error("Failed to list containers", error=str(e))
            raise

    async def list_images(self) -> List[Dict[str, Any]]:
        """
        List Docker images.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing image information.
        """
        try:
            images = await asyncio.to_thread(self.client.images.list)
            return [self._format_image_info(image) for image in images]
        except APIError as e:
            logger.error("Failed to list images", error=str(e))
            raise

    async def list_volumes(self) -> List[Dict[str, Any]]:
        """
        List Docker volumes.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing volume information.
        """
        try:
            volumes = await asyncio.to_thread(self.client.volumes.list)
            return [self._format_volume_info(volume) for volume in volumes]
        except APIError as e:
            logger.error("Failed to list volumes", error=str(e))
            raise

    async def list_networks(self) -> List[Dict[str, Any]]:
        """
        List Docker networks.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing network information.
        """
        try:
            networks = await asyncio.to_thread(self.client.networks.list)
            return [self._format_network_info(network) for network in networks]
        except APIError as e:
            logger.error("Failed to list networks", error=str(e))
            raise

    def _format_container_info(self, container: docker.models.containers.Container) -> Dict[str, Any]:
        """
        Format container information into a dictionary.

        Args:
            container (docker.models.containers.Container): A Docker container object.

        Returns:
            Dict[str, Any]: A dictionary containing formatted container information.
        """
        return {
            "id": container.id,
            "name": container.name,
            "status": container.status,
            "image": container.image.tags[0] if container.image.tags else container.image.id,
            "created": container.attrs['Created'],
            "ports": container.ports,
        }

    def _format_image_info(self, image: docker.models.images.Image) -> Dict[str, Any]:
        """
        Format image information into a dictionary.

        Args:
            image (docker.models.images.Image): A Docker image object.

        Returns:
            Dict[str, Any]: A dictionary containing formatted image information.
        """
        return {
            "id": image.id,
            "tags": image.tags,
            "created": image.attrs['Created'],
            "size": image.attrs['Size'],
        }

    def _format_volume_info(self, volume: docker.models.volumes.Volume) -> Dict[str, Any]:
        """
        Format volume information into a dictionary.

        Args:
            volume (docker.models.volumes.Volume): A Docker volume object.

        Returns:
            Dict[str, Any]: A dictionary containing formatted volume information.
        """
        return {
            "name": volume.name,
            "driver": volume.attrs['Driver'],
            "mountpoint": volume.attrs['Mountpoint'],
            "created": volume.attrs['CreatedAt'],
        }

    def _format_network_info(self, network: docker.models.networks.Network) -> Dict[str, Any]:
        """
        Format network information into a dictionary.

        Args:
            network (docker.models.networks.Network): A Docker network object.

        Returns:
            Dict[str, Any]: A dictionary containing formatted network information.
        """
        return {
            "id": network.id,
            "name": network.name,
            "driver": network.attrs['Driver'],
            "scope": network.attrs['Scope'],
            "created": network.attrs['Created'],
        }

# Example usage
async def main():
    docker_client = DockerClient()
    containers = await docker_client.list_containers(all=True)
    print("Containers:", containers)

    images = await docker_client.list_images()
    print("Images:", images)

    volumes = await docker_client.list_volumes()
    print("Volumes:", volumes)

    networks = await docker_client.list_networks()
    print("Networks:", networks)

if __name__ == "__main__":
    asyncio.run(main())