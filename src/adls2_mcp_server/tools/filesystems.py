import json
import logging
import os
from dataclasses import dataclass, field, asdict
from typing import List, Dict

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

@dataclass
class FilesystemListResponse:
    success: bool
    filesystems: List[str] = field(default_factory=list)
    error: str = ""

@dataclass
class CreateFilesystemResponse:
    name: str
    success: bool
    error: str = ""

@dataclass
class DeleteFilesystemResponse:
    name: str
    success: bool
    error: str = ""

def register_filesystem_tools(mcp):
    """Register filesystem related MCP tools."""

    @mcp.tool(
        name="list_filesystems",
        description="List all filesystems in the storage account"
    )
    async def list_filesystems() -> Dict[str, str]:
        """List all filesystems in the storage account.
        
        Returns:
            Dict containing the list of filesystems and operation status
        """
        try:
            fs = await mcp.client.list_filesystems()
            response = FilesystemListResponse(
                success=True,
                filesystems=fs,
                error=""
            )
            return asdict(response)
        except Exception as e:
            logger.error(f"Error listing filesystems: {e}")
            response = FilesystemListResponse(
                success=False,
                error=str(e)
            )
            return asdict(response)

    @mcp.tool(
        name="create_filesystem",
        description="Create a new ADLS2 filesystem (container)"
    )
    async def create_filesystem(name: str) -> Dict[str, str]:
        """Create a new filesystem in the storage account.
        
        Args:
            name: Name of the filesystem to create
            
        Returns:
            Dict containing the result of the operation
        """
        if mcp.client.read_only:
            response = CreateFilesystemResponse(
                name=name,
                success=False,
                error="Cannot create filesystem in read-only mode"
            )
            return asdict(response)

        try:
            success = await mcp.client.create_container(name)
            response = CreateFilesystemResponse(
                name=name,
                success=success,
                error="" if success else "Failed to create filesystem"
            )
            return asdict(response)
        except Exception as e:
            logger.error(f"Error creating filesystem {name}: {e}")
            response = CreateFilesystemResponse(
                name=name,
                success=False,
                error=str(e)
            )
            return asdict(response)

    @mcp.tool(
        name="delete_filesystem",
        description="Delete an ADLS2 filesystem"
    )
    async def delete_filesystem(name: str) -> Dict[str, str]:
        """Delete a filesystem from the storage account.
        
        Args:
            name: Name of the filesystem to delete
            
        Returns:
            Dict containing the result of the operation
        """
        if mcp.client.read_only:
            response = DeleteFilesystemResponse(
                name=name,
                success=False,
                error="Cannot delete filesystem in read-only mode"
            )
            return asdict(response)

        try:
            success = await mcp.client.delete_filesystem(name)
            response = DeleteFilesystemResponse(
                name=name,
                success=success,
                error="" if success else "Failed to delete filesystem"
            )
            return asdict(response)
        except Exception as e:
            logger.error(f"Error deleting filesystem {name}: {e}")
            response = DeleteFilesystemResponse(
                name=name,
                success=False,
                error=str(e)
            )
            return asdict(response)
