import logging
import os
from dataclasses import dataclass
from typing import List, Optional

from azure.identity import DefaultAzureCredential
from azure.storage.filedatalake import DataLakeServiceClient
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

@dataclass
class ADLS2Config:
    """Configuration for Azure Data Lake Storage Gen2 client."""
    storage_account_name: str
    read_only: bool = True
    storage_account_key: Optional[str] = None

    @classmethod
    def from_env(cls) -> "ADLS2Client":
        """Create a client from environment variables."""
        load_dotenv()

        storage_account_name = os.environ.get("AZURE_STORAGE_ACCOUNT_NAME")
        if not storage_account_name:
            raise ValueError("AZURE_STORAGE_ACCOUNT_NAME is not set")
        
        return cls(
            storage_account_name=storage_account_name,
            storage_account_key=os.environ.get("AZURE_STORAGE_ACCOUNT_KEY"),
            read_only=os.environ.get("READ_ONLY_MODE", "true").lower() == "true"
        )

class ADLS2Client:
    """Azure Data Lake Storage Gen2 client wrapper"""

    def __init__(self, config: Optional[ADLS2Config] = None):
        """ Initialize the ADLS2 client.

        Args:
            config: ADLS2Config instance. If None, loads from environment
        """
        self._config = config or ADLS2Config.from_env()

        # Initialize the client
        self.client = self._create_client()

    @property
    def read_only(self) -> bool:
        """Whether the client is in read-only mode."""
        return self._config.read_only
    
    @property
    def config(self) -> ADLS2Config:
        """The configuration for the client."""
        return self._config
    
    def _create_client(self) -> DataLakeServiceClient:
        """Create the DataLakeServiceClient."""
        account_url = f"https://{self._config.storage_account_name}.dfs.core.windows.net"
        credential = DefaultAzureCredential()
        return DataLakeServiceClient(account_url=account_url, credential=credential)
    
    async def create_container(self, container: str) -> bool:
        """Create a new container (filesystem) in the storage account.
        
        Args:
            container: Name of the container to create
            
        Returns:
            bool: True if container was created successfully, False otherwise
            
        Raises:
            Exception: If there is an error creating the container
        """
        try:
            _ = self.client.create_file_system(file_system=container)
            return True
        except Exception as e:
            logger.error(f"Error creating container {container}: {e}")
            return False
        
    async def list_filesystems(self) -> List[str]:
        """List all filesystems in the storage account.
        
        Returns:
            List[str]: List of filesystem names
        """
        try:
            return [container.name for container in self.client.list_file_systems()]
        except Exception as e:
            logger.error(f"Error listing filesystems: {e}")
            return []
    
    async def delete_filesystem(self, name: str) -> bool:
        """Delete a filesystem from the storage account.
        
        Args:
            name: Name of the filesystem to delete
            
        Returns:
            bool: True if filesystem was deleted successfully, False otherwise
            
        Raises:
            Exception: If there is an error deleting the filesystem
        """
        try:
            file_system_client = self.client.get_file_system_client(name)
            file_system_client.delete_file_system()
            return True
        except Exception as e:
            logger.error(f"Error deleting filesystem {name}: {e}")
            return False

    async def create_directory(self, filesystem: str, directory: str) -> bool:
        """Create a new directory in the specified filesystem.
        
        Args:
            filesystem: Name of the filesystem
            directory: Path of the directory to create
            
        Returns:
            bool: True if directory was created successfully, False otherwise
        """
        try:
            file_system_client = self.client.get_file_system_client(filesystem)
            directory_client = file_system_client.create_directory(directory)
            return True
        except Exception as e:
            logger.error(f"Error creating directory {directory}: {e}")
            return False

    async def delete_directory(self, filesystem: str, directory: str) -> bool:
        """Delete a directory from the specified filesystem.
        
        Args:
            filesystem: Name of the filesystem
            directory: Path of the directory to delete
            
        Returns:
            bool: True if directory was deleted successfully, False otherwise
        """
        try:
            file_system_client = self.client.get_file_system_client(filesystem)
            directory_client = file_system_client.get_directory_client(directory)
            directory_client.delete_directory()
            return True
        except Exception as e:
            logger.error(f"Error deleting directory {directory}: {e}")
            return False

    async def rename_directory(self, filesystem: str, source_path: str, destination_path: str) -> bool:
        """Rename/move a directory within the specified filesystem.
        
        Args:
            filesystem: Name of the filesystem
            source_path: Current path of the directory
            destination_path: New path for the directory
            
        Returns:
            bool: True if directory was renamed successfully, False otherwise
        """
        try:
            file_system_client = self.client.get_file_system_client(filesystem)
            directory_client = file_system_client.get_directory_client(source_path)
            new_name = f"{file_system_client.file_system_name}/{destination_path}"
            directory_client.rename_directory(new_name)
            return True
        except Exception as e:
            logger.error(f"Error renaming directory {source_path} to {destination_path}: {e}")
            return False

    async def directory_get_paths(self, filesystem: str, directory: str = "/", recursive: bool = True) -> List[str]:
        """Get files and directories under the specified path.
        
        Args:
            filesystem: Name of the filesystem
            directory: Path of the directory to list. Defaults to "/".
            recursive: If True, list paths recursively. Defaults to True.
            
        Returns:
            List[str]: List of file and directory under the path
        """
        try:
            file_system_client = self.client.get_file_system_client(filesystem)
            directory_client = file_system_client.get_directory_client(directory)
            
            paths = []
            paths_iter = directory_client.get_paths(recursive=recursive)
            
            for path in paths_iter:
                paths.append(path.name)
                
            return paths
        except Exception as e:
            logger.error(f"Error getting paths for directory {directory}: {e}")
            return []
