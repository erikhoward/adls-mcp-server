import json
import logging
from dataclasses import dataclass, field, asdict
from typing import Dict, List

logger = logging.getLogger(__name__)

@dataclass
class DirectoryResponse:
    path: str
    success: bool
    error: str = ""

@dataclass
class DirectoryExistsResponse:
    path: str
    exists: bool
    error: str = ""

@dataclass
class DirectoryPathsResponse:
    path: str
    paths: List[str] = field(default_factory=list)
    error: str = ""

def register_directory_tools(mcp):
    """Register directory-related MCP tools."""

    @mcp.tool(
        name="create_directory",
        description="Create a new directory in the specified filesystem"
    )
    async def create_directory(filesystem: str, path: str) -> Dict[str, str]:
        """Create a new directory in the specified filesystem.
        
        Args:
            filesystem: Name of the filesystem
            path: Path of the directory to create
            
        Returns:
            Dict containing the result of the operation
        """
        if mcp.client.read_only:
            response = DirectoryResponse(
                path=path,
                success=False,
                error="Cannot create directory in read-only mode"
            )
            return asdict(response)

        try:
            success = await mcp.client.create_directory(filesystem, path)
            response = DirectoryResponse(
                path=path,
                success=success,
                error="" if success else "Failed to create directory"
            )
            return asdict(response)
        except Exception as e:
            logger.error(f"Error creating directory {path}: {e}")
            response = DirectoryResponse(
                path=path,
                success=False,
                error=str(e)
            )
            return asdict(response)

    @mcp.tool(
        name="delete_directory",
        description="Delete a directory from the specified filesystem"
    )
    async def delete_directory(filesystem: str, path: str) -> Dict[str, str]:
        """Delete a directory from the specified filesystem.
        
        Args:
            filesystem: Name of the filesystem
            path: Path of the directory to delete
            
        Returns:
            Dict containing the result of the operation
        """
        if mcp.client.read_only:
            response = DirectoryResponse(
                path=path,
                success=False,
                error="Cannot delete directory in read-only mode"
            )
            return asdict(response)

        try:
            success = await mcp.client.delete_directory(filesystem, path)
            response = DirectoryResponse(
                path=path,
                success=success,
                error="" if success else "Failed to delete directory"
            )
            return asdict(response)
        except Exception as e:
            logger.error(f"Error deleting directory {path}: {e}")
            response = DirectoryResponse(
                path=path,
                success=False,
                error=str(e)
            )
            return asdict(response)

    @mcp.tool(
        name="rename_directory",
        description="Rename/move a directory within the specified filesystem"
    )
    async def rename_directory(filesystem: str, source_path: str, destination_path: str) -> Dict[str, str]:
        """Rename/move a directory within the specified filesystem.
        
        Args:
            filesystem: Name of the filesystem
            source_path: Current path of the directory
            destination_path: New path for the directory
            
        Returns:
            Dict containing the result of the operation
        """
        if mcp.client.read_only:
            response = DirectoryResponse(
                path=source_path,
                success=False,
                error="Cannot rename directory in read-only mode"
            )
            return asdict(response)

        try:
            success = await mcp.client.rename_directory(filesystem, source_path, destination_path)
            response = DirectoryResponse(
                path=destination_path,
                success=success,
                error="" if success else "Failed to rename directory"
            )
            return asdict(response)
        except Exception as e:
            logger.error(f"Error renaming directory {source_path} to {destination_path}: {e}")
            response = DirectoryResponse(
                path=source_path,
                success=False,
                error=str(e)
            )
            return asdict(response)

    @mcp.tool(
        name="directory_exists",
        description="Check if a directory exists in the specified filesystem"
    )
    async def directory_exists(filesystem: str, path: str) -> Dict[str, str]:
        """Check if a directory exists in the specified filesystem.
        
        Args:
            filesystem: Name of the filesystem
            path: Path of the directory to check
            
        Returns:
            Dict containing the result of the operation
        """
        try:
            exists = await mcp.client.directory_exists(filesystem, path)
            response = DirectoryExistsResponse(
                path=path,
                exists=exists,
                error=""
            )
            return asdict(response)
        except Exception as e:
            logger.error(f"Error checking directory existence {path}: {e}")
            response = DirectoryExistsResponse(
                path=path,
                exists=False,
                error=str(e)
            )
            return asdict(response)

    @mcp.tool(
        name="directory_get_paths",
        description="Get all paths under the specified directory"
    )
    async def directory_get_paths(filesystem: str, directory_path: str, recursive: bool = True) -> Dict[str, str]:
        """Get all paths under the specified directory.
        
        Args:
            filesystem: Name of the filesystem
            directory_path: Path of the directory to list
            recursive: If True, list paths recursively. Defaults to True.
            
        Returns:
            Dict containing the list of paths and operation status
        """
        try:
            paths = await mcp.client.directory_get_paths(filesystem, directory_path, recursive)
            response = DirectoryPathsResponse(
                path=directory_path,
                paths=paths,
                error=""
            )
            return asdict(response)
        except Exception as e:
            logger.error(f"Error getting paths for directory {directory_path}: {e}")
            response = DirectoryPathsResponse(
                path=directory_path,
                error=str(e)
            )
            return asdict(response)
