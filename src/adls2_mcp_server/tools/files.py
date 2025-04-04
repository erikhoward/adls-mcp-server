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
