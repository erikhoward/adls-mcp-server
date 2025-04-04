import json
import logging
import os
from dataclasses import dataclass, field
from typing import List

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

@dataclass
class FilesystemData:
    filesystems: List[str] = field(default_factory=list)

def register_filesystem_tools(mcp):
    """Register filesystem related MCP tools."""

    @mcp.resource("adls://filesystems", name="filesystems", description="List all filesystems in the storage account")
    async def list_filesystems() -> List[str]:
        """List all filesystems in the storage account."""
        try:
            fs = await mcp.client.list_filesystems()
            data = FilesystemData(filesystems=fs)
            return json.dumps(data.__dict__)
        except Exception as e:
            logger.error(f"Error listing filesystems: {e}")
            return []
