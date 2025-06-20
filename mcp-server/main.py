"""
Main entry point for the League MCP Server.

This server provides access to League of Legends game data through the Riot Games API
via the Model Context Protocol (MCP). It supports multiple transport types for 
different integration scenarios.

Usage:
    python main.py [--transport {stdio,sse}]

Transport Types:
    - stdio: Standard input/output transport (default)
      Used for direct integration with MCP clients like Claude Desktop
    - sse: Server-Sent Events transport 
      Used for web-based integrations and HTTP connections

Examples:
    python main.py                    # Uses stdio transport (default)
    python main.py --transport stdio  # Explicitly use stdio transport
    python main.py --transport sse    # Use SSE transport for web integration
"""

import argparse
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
    """
    Initialize and run the MCP server.
    
    Parses command line arguments to determine transport type, registers all
    League of Legends API tools, resources, and workflow prompts, then starts
    the server with the specified transport.
    """
    # Parse command line arguments for transport selection
    parser = argparse.ArgumentParser(
        description='League MCP Server - Provides League of Legends data via MCP',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Transport Types:
  stdio    Standard input/output (for Claude Desktop integration)
  sse      Server-Sent Events (for web-based integrations)
        """
    )
    parser.add_argument(
        '--transport', 
        choices=['stdio', 'sse'], 
        default='stdio',
        help='Transport type to use (default: stdio)'
    )
    args = parser.parse_args()
    
    logger.info(f"Starting League MCP Server with {args.transport} transport...")
    
    # Register all tools    
    register_account_tools(mcp)
    
    register_summoner_tools(mcp)
    
    register_spectator_tools(mcp)
    
    register_champion_tools(mcp)
    
    register_clash_tools(mcp)
    
    register_league_tools(mcp)
    
    register_status_tools(mcp)
    
    register_match_tools(mcp)
    
    register_challenges_tools(mcp)
    
    register_tournament_tools(mcp)
    
    register_data_dragon_resources(mcp)
    register_game_constants_resources(mcp)
    
    register_workflow_prompts(mcp)
    
    logger.info("All tools, resources, and prompts registered successfully!")
    
    # Run the server with the specified transport type
    logger.info(f"Server starting on {args.transport} transport...")
    mcp.run(transport=args.transport)

if __name__ == "__main__":
    main() 