import logging
import os
from dataclasses import dataclass
from typing import List, Optional, Dict
from pathlib import Path

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
        self._read_only = self._config.read_only
        self.upload_root = os.getenv("UPLOAD_ROOT", "./uploads")

    @property
    def read_only(self) -> bool:
        """Whether the client is in read-only mode."""
        return self._read_only
    
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

    async def upload_file(self, upload_file: str, filesystem: str, destination: str) -> bool:
        """Upload a file to ADLS2.
        
        Args:
            upload_file: Path to the file to upload (relative to UPLOAD_ROOT)
            filesystem: Name of the filesystem
            destination: Destination path in ADLS2
            
        Returns:
            bool: True if file was uploaded successfully, False otherwise
            
        Raises:
            Exception: If there is an error uploading the file
        """
        try:
            # Construct full source path
            source_path = Path(self.upload_root) / upload_file
            
            # Verify file exists and is within upload_root
            if not source_path.exists():
                logger.error(f"Source file does not exist: {source_path}")
                return False
                
            if not str(source_path.absolute()).startswith(str(Path(self.upload_root).absolute())):
                logger.error(f"Source file must be within UPLOAD_ROOT: {self.upload_root}")
                return False

            # Get file system client and create file client
            file_system_client = self.client.get_file_system_client(filesystem)
            file_client = file_system_client.get_file_client(destination)

            # Upload the file
            with open(source_path, "rb") as file:
                file_client.upload_data(file.read(), overwrite=True)

            return True
        except Exception as e:
            logger.error(f"Error uploading file {upload_file} to {destination}: {e}")
            return False

    async def download_file(self, filesystem: str, source: str, download_path: str) -> bool:
        """Download a file from ADLS2.
        
        Args:
            filesystem: Name of the filesystem
            source: Source path in ADLS2
            download_path: Path where to save the file (relative to UPLOAD_ROOT)
            
        Returns:
            bool: True if file was downloaded successfully, False otherwise
            
        Raises:
            Exception: If there is an error downloading the file
        """
        try:
            # Construct full destination path
            dest_path = Path(self.upload_root) / download_path
            
            # Create parent directories if they don't exist
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Verify destination path is within upload_root
            if not str(dest_path.absolute()).startswith(str(Path(self.upload_root).absolute())):
                logger.error(f"Destination path must be within UPLOAD_ROOT: {self.upload_root}")
                return False

            # Get file system client and file client
            file_system_client = self.client.get_file_system_client(filesystem)
            file_client = file_system_client.get_file_client(source)

            # Download the file
            download = file_client.download_file()
            with open(dest_path, "wb") as file:
                file.write(download.readall())

            return True
        except Exception as e:
            logger.error(f"Error downloading file {source} to {download_path}: {e}")
            return False

    async def file_exists(self, filesystem: str, file_path: str) -> bool:
        """Check if a file exists in the specified filesystem.
        
        Args:
            filesystem: Name of the filesystem
            file_path: Path to the file relative to filesystem root
            
        Returns:
            bool: True if file exists, False otherwise
        """
        try:
            file_system_client = self.client.get_file_system_client(filesystem)
            file_client = file_system_client.get_file_client(file_path)
            
            # Try to get file properties to check existence
            file_client.get_file_properties()
            return True
        except Exception as e:
            logger.debug(f"File {file_path} does not exist in filesystem {filesystem}: {e}")
            return False

    async def rename_file(self, filesystem: str, source_path: str, destination_path: str) -> bool:
        """Rename/move a file within the specified filesystem.
        
        Args:
            filesystem: Name of the filesystem
            source_path: Current path of the file relative to filesystem root
            destination_path: New path for the file relative to filesystem root
            
        Returns:
            bool: True if file was renamed successfully, False otherwise
        """
        try:
            file_system_client = self.client.get_file_system_client(filesystem)
            file_client = file_system_client.get_file_client(source_path)
            
            # Construct new name with filesystem prefix as required by Azure SDK
            new_name = f"{file_system_client.file_system_name}/{destination_path}"
            
            # Rename the file
            file_client.rename_file(new_name)
            return True
        except Exception as e:
            logger.error(f"Error renaming file {source_path} to {destination_path}: {e}")
            return False

    async def get_file_properties(self, filesystem: str, file_path: str) -> Optional[Dict[str, str]]:
        """Get properties of a file in the specified filesystem.
        
        Args:
            filesystem: Name of the filesystem
            file_path: Path to the file relative to filesystem root
            
        Returns:
            Dict containing file properties or None if file doesn't exist or error occurs
            Properties include:
            - name: File name
            - size: File size in bytes
            - creation_time: When the file was created
            - last_modified: When the file was last modified
            - content_type: MIME type of the file
            - etag: Entity tag for the file
        """
        try:
            file_system_client = self.client.get_file_system_client(filesystem)
            file_client = file_system_client.get_file_client(file_path)
            
            properties = file_client.get_file_properties()
            
            return {
                "name": file_path,
                "size": str(properties.size),
                "creation_time": properties.creation_time.isoformat() if properties.creation_time else "",
                "last_modified": properties.last_modified.isoformat() if properties.last_modified else "",
                "content_type": properties.content_settings.content_type if properties.content_settings else "",
                "etag": properties.etag if properties.etag else ""
            }
        except Exception as e:
            logger.error(f"Error getting properties for file {file_path}: {e}")
            return None
