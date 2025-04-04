from .filesystems import register_filesystem_tools
from .files import register_file_tools
from .directories import register_directory_tools

def register_all_tools(mcp):
    """Register all MCP tools."""
    register_filesystem_tools(mcp)
    register_file_tools(mcp)
    register_directory_tools(mcp)