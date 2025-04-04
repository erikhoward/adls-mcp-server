import logging
import os

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

from adls2_mcp_server.client import ADLS2Client
from adls2_mcp_server.tools import register_all_tools

load_dotenv()

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s [%(name)s - %(levelname)s] - %(message)s",
    )
logger = logging.getLogger(__name__)

# Initialize MCP server
mcp = FastMCP("ADLS2MCP")
mcp.client = ADLS2Client() 

# Register all MCP tools
register_all_tools(mcp)

def main():
    """Main entry point for the ADLS2 MCP service."""
    try:
        logger.info("Starting ADLS2 MCP service")
        mcp.run(transport="stdio")
    except Exception as e:
        logger.error(f"Error starting ADLS2 MCP service: {str(e)}")
        raise

if __name__ == "__main__":
    main()