"""Main entry point for the League MCP Server."""

import logging
from mcp.server.fastmcp import FastMCP

# Import all tool registration functions
from primitives.tools.account_tools import register_account_tools
from primitives.tools.summoner_tools import register_summoner_tools
from primitives.tools.spectator_tools import register_spectator_tools
from primitives.tools.champion_tools import register_champion_tools
from primitives.tools.clash_tools import register_clash_tools
from primitives.tools.league_tools import register_league_tools
from primitives.tools.status_tools import register_status_tools

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("league")

def main():
    """Initialize and run the MCP server."""
    logger.info("Starting League MCP Server...")
    
    # Register all tools
    logger.info("Registering Account API tools...")
    register_account_tools(mcp)
    
    logger.info("Registering Summoner API tools...")
    register_summoner_tools(mcp)
    
    logger.info("Registering Spectator API tools...")
    register_spectator_tools(mcp)
    
    logger.info("Registering Champion API tools...")
    register_champion_tools(mcp)
    
    logger.info("Registering Clash API tools...")
    register_clash_tools(mcp)
    
    logger.info("Registering League API tools...")
    register_league_tools(mcp)
    
    logger.info("Registering Status API tools...")
    register_status_tools(mcp)
    
    logger.info("All tools registered successfully!")
    
    # Run the server
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main() 