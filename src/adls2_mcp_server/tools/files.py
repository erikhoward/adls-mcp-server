import json
import logging
from dataclasses import dataclass, asdict
from typing import Dict, Union

logger = logging.getLogger(__name__)


# Data class used to prevent the init inbuilt function and less boilerplate 
@dataclass
class FileResponse:
    source: str
    destination: str
    success: bool
    error: str = ""

@dataclass
class FileDownloadResponse:
    source: str
    destination: str
    success: bool
    error: str = ""

@dataclass
class FileExistsResponse:
    path: str
    exists: bool
    error: str = ""

@dataclass
class FileRenameResponse:
    source: str
    destination: str
    success: bool
    error: str = ""

@dataclass
class FilePropertiesResponse:
    path: str
    properties: Dict[str, str]
    success: bool
    error: str = ""

@dataclass
class FileMetadataResponse:
    path: str
    metadata: Dict[str, str]
    success: bool
    error: str = ""

@dataclass
class SetFileMetadataResponse:
    path: str
    success: bool
    error: str = ""

def register_file_tools(mcp):
    """Register file-related MCP tools."""

    @mcp.tool(
        name="upload_file",
        description="Upload a file to ADLS2"
    )
    async def upload_file(upload_file: str, filesystem: str, destination: str) -> Dict[str, str]:
        """Upload a file to ADLS2.
        
        Args:
            upload_file: Path to the file to upload (relative to UPLOAD_ROOT)
            filesystem: Name of the filesystem
            destination: Destination path in ADLS2
            
        Returns:
            Dict containing the result of the operation
        """
        if mcp.client.read_only:
            response = FileResponse(
                source=upload_file,
                destination=destination,
                success=False,
                error="Cannot upload file in read-only mode"
            )
            # TODO: add comment remove the json.dumps because we are returning a dict but no need for json because mcp serializes itself to json
            return asdict(response)

        try:
            success = await mcp.client.upload_file(upload_file, filesystem, destination)
            response = FileResponse(
                source=upload_file,
                destination=destination,
                success=success,
                error="" if success else "Failed to upload file"
            )
            return asdict(response)
        except Exception as e:
            logger.error(f"Error uploading file {upload_file} to {destination}: {e}")
            response = FileResponse(
                source=upload_file,
                destination=destination,
                success=False,
                error=str(e)
            )
            return asdict(response)

    @mcp.tool(
        name="download_file",
        description="Download a file from ADLS2"
    )
    async def download_file(filesystem: str, source: str, download_path: str) -> Dict[str, str]:
        """Download a file from ADLS2.
        
        Args:
            filesystem: Name of the filesystem
            source: Source path in ADLS2
            download_path: Path where to save the file (relative to UPLOAD_ROOT)
            
        Returns:
            Dict containing the result of the operation
        """
        try:
            success = await mcp.client.download_file(filesystem, source, download_path)
            response = FileDownloadResponse(
                source=source,
                destination=download_path,
                success=success,
                error="" if success else "Failed to download file"
            )
            return asdict(response)
        except Exception as e:
            logger.error(f"Error downloading file {source} to {download_path}: {e}")
            response = FileDownloadResponse(
                source=source,
                destination=download_path,
                success=False,
                error=str(e)
            )
            return asdict(response)

    @mcp.tool(
        name="file_exists",
        description="Check if a file exists in the specified filesystem"
    )
    async def file_exists(filesystem: str, file_path: str) -> Dict[str, str]:
        """Check if a file exists in the specified filesystem.
        
        Args:
            filesystem: Name of the filesystem
            file_path: Path to the file relative to filesystem root
            
        Returns:
            Dict containing the result of the operation
        """
        try:
            exists = await mcp.client.file_exists(filesystem, file_path)
            response = FileExistsResponse(
                path=file_path,
                exists=exists,
                error=""
            )
            return asdict(response)
        except Exception as e:
            logger.error(f"Error checking file existence {file_path}: {e}")
            response = FileExistsResponse(
                path=file_path,
                exists=False,
                error=str(e)
            )
            return asdict(response)

    @mcp.tool(
        name="rename_file",
        description="Rename/move a file within the specified filesystem"
    )
    async def rename_file(filesystem: str, source_path: str, destination_path: str) -> Dict[str, str]:
        """Rename/move a file within the specified filesystem.
        
        Args:
            filesystem: Name of the filesystem
            source_path: Current path of the file relative to filesystem root
            destination_path: New path for the file relative to filesystem root
            
        Returns:
            Dict containing the result of the operation
        """
        if mcp.client.read_only:
            response = FileRenameResponse(
                source=source_path,
                destination=destination_path,
                success=False,
                error="Cannot rename file in read-only mode"
            )
            return asdict(response)

        try:
            success = await mcp.client.rename_file(filesystem, source_path, destination_path)
            response = FileRenameResponse(
                source=source_path,
                destination=destination_path,
                success=success,
                error="" if success else "Failed to rename file"
            )
            return asdict(response)
        except Exception as e:
            logger.error(f"Error renaming file {source_path} to {destination_path}: {e}")
            response = FileRenameResponse(
                source=source_path,
                destination=destination_path,
                success=False,
                error=str(e)
            )
            return asdict(response)

    @mcp.tool(
        name="get_file_properties",
        description="Get properties of a file in the specified filesystem"
    )
    async def get_file_properties(filesystem: str, file_path: str) -> Dict[str, str]:
        """Get properties of a file in the specified filesystem.
        
        Args:
            filesystem: Name of the filesystem
            file_path: Path to the file relative to filesystem root
            
        Returns:
            Dict containing the file properties and operation status
        """
        try:
            properties = await mcp.client.get_file_properties(filesystem, file_path)
            if properties is not None:
                response = FilePropertiesResponse(
                    path=file_path,
                    properties=properties,
                    success=True,
                    error=""
                )
            else:
                response = FilePropertiesResponse(
                    path=file_path,
                    properties={},
                    success=False,
                    error="Failed to get file properties"
                )
            return asdict(response)
        except Exception as e:
            logger.error(f"Error getting properties for file {file_path}: {e}")
            response = FilePropertiesResponse(
                path=file_path,
                properties={},
                success=False,
                error=str(e)
            )
            return asdict(response)

    @mcp.tool(
        name="get_file_metadata",
        description="Get metadata of a file in the specified filesystem"
    )
    async def get_file_metadata(filesystem: str, file_path: str) -> Dict[str, str]:
        """Get metadata of a file in the specified filesystem.
        
        Args:
            filesystem: Name of the filesystem
            file_path: Path to the file relative to filesystem root
            
        Returns:
            Dict containing the file metadata and operation status
        """
        try:
            metadata = await mcp.client.get_file_metadata(filesystem, file_path)
            if metadata is not None:
                response = FileMetadataResponse(
                    path=file_path,
                    metadata=metadata,
                    success=True,
                    error=""
                )
            else:
                response = FileMetadataResponse(
                    path=file_path,
                    metadata={},
                    success=False,
                    error="Failed to get file metadata"
                )
            return asdict(response)
        except Exception as e:
            logger.error(f"Error getting metadata for file {file_path}: {e}")
            response = FileMetadataResponse(
                path=file_path,
                metadata={},
                success=False,
                error=str(e)
            )
            return asdict(response)

    @mcp.tool(
        name="set_file_metadata",
        description="Set a single metadata key-value pair for a file"
    )
    async def set_file_metadata(filesystem: str, file_path: str, key: str, value: str) -> Dict[str, str]:
        """Set a single metadata key-value pair for a file.
        
        Args:
            filesystem: Name of the filesystem
            file_path: Path to the file relative to filesystem root
            key: Metadata key
            value: Metadata value
            
        Returns:
            Dict containing the operation status
        """
        if mcp.client.read_only:
            response = SetFileMetadataResponse(
                path=file_path,
                success=False,
                error="Cannot set metadata in read-only mode"
            )
            return asdict(response)

        try:
            success = await mcp.client.set_file_metadata(filesystem, file_path, key, value)
            response = SetFileMetadataResponse(
                path=file_path,
                success=success,
                error="" if success else "Failed to set file metadata"
            )
            return asdict(response)
        except Exception as e:
            logger.error(f"Error setting metadata for file {file_path}: {e}")
            response = SetFileMetadataResponse(
                path=file_path,
                success=False,
                error=str(e)
            )
            return asdict(response)

    @mcp.tool(
        name="set_file_metadata_json",
        description="Set multiple metadata key-value pairs for a file using JSON"
    )
    async def set_file_metadata_json(filesystem: str, file_path: str, metadata_json: Union[str, Dict[str, str]]) -> Dict[str, str]:
        """Set multiple metadata key-value pairs for a file using JSON.
        
        Args:
            filesystem: Name of the filesystem
            file_path: Path to the file relative to filesystem root
            metadata_json: JSON string or dictionary containing metadata key-value pairs
            
        Returns:
            Dict containing the operation status
        """
        if mcp.client.read_only:
            response = SetFileMetadataResponse(
                path=file_path,
                success=False,
                error="Cannot set metadata in read-only mode"
            )
            return asdict(response)

        try:
            # Convert metadata_json to string if it's a dictionary
            if isinstance(metadata_json, dict):
                metadata_json = json.dumps(metadata_json)
            
            success = await mcp.client.set_file_metadata_json(filesystem, file_path, metadata_json)
            response = SetFileMetadataResponse(
                path=file_path,
                success=success,
                error="" if success else "Failed to set file metadata"
            )
            return asdict(response)
        except Exception as e:
            logger.error(f"Error setting metadata for file {file_path}: {e}")
            response = SetFileMetadataResponse(
                path=file_path,
                success=False,
                error=str(e)
            )
            return asdict(response)
