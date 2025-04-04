import json
import logging
from dataclasses import dataclass
from typing import Dict

logger = logging.getLogger(__name__)

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
            return json.dumps(response.__dict__)

        try:
            success = await mcp.client.upload_file(upload_file, filesystem, destination)
            response = FileResponse(
                source=upload_file,
                destination=destination,
                success=success,
                error="" if success else "Failed to upload file"
            )
            return json.dumps(response.__dict__)
        except Exception as e:
            logger.error(f"Error uploading file {upload_file} to {destination}: {e}")
            response = FileResponse(
                source=upload_file,
                destination=destination,
                success=False,
                error=str(e)
            )
            return json.dumps(response.__dict__)

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
            return json.dumps(response.__dict__)
        except Exception as e:
            logger.error(f"Error downloading file {source} to {download_path}: {e}")
            response = FileDownloadResponse(
                source=source,
                destination=download_path,
                success=False,
                error=str(e)
            )
            return json.dumps(response.__dict__)

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
            return json.dumps(response.__dict__)
        except Exception as e:
            logger.error(f"Error checking file existence {file_path}: {e}")
            response = FileExistsResponse(
                path=file_path,
                exists=False,
                error=str(e)
            )
            return json.dumps(response.__dict__)

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
            return json.dumps(response.__dict__)

        try:
            success = await mcp.client.rename_file(filesystem, source_path, destination_path)
            response = FileRenameResponse(
                source=source_path,
                destination=destination_path,
                success=success,
                error="" if success else "Failed to rename file"
            )
            return json.dumps(response.__dict__)
        except Exception as e:
            logger.error(f"Error renaming file {source_path} to {destination_path}: {e}")
            response = FileRenameResponse(
                source=source_path,
                destination=destination_path,
                success=False,
                error=str(e)
            )
            return json.dumps(response.__dict__)
