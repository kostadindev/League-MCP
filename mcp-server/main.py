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
from primitives.tools.match_tools import register_match_tools
from primitives.tools.challenges_tools import register_challenges_tools
from primitives.tools.tournament_tools import register_tournament_tools
from primitives.resources.data_dragon_resources import register_data_dragon_resources
from primitives.resources.game_constants_resources import register_game_constants_resources
from primitives.prompts.common_workflows import register_workflow_prompts

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
    
    logger.info("Registering Match API tools...")
    register_match_tools(mcp)
    
    logger.info("Registering Challenges API tools...")
    register_challenges_tools(mcp)
    
    logger.info("Registering Tournament API tools...")
    register_tournament_tools(mcp)
    
    logger.info("Registering Data Dragon resources...")
    register_data_dragon_resources(mcp)
    
    logger.info("Registering Game Constants resources...")
    register_game_constants_resources(mcp)
    
    logger.info("Registering workflow prompts...")
    register_workflow_prompts(mcp)
    
    logger.info("All tools, resources, and prompts registered successfully!")
    
    # Run the server
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main() 