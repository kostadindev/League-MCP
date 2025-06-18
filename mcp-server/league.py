from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("league")

# Constants
RIOT_API_BASE = "https://{region}.api.riotgames.com"
USER_AGENT = "league-mcp-server/1.0"

# You'll need to set your Riot API key as an environment variable
# Get your key from: https://developer.riotgames.com/
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("RIOT_API_KEY")

async def make_riot_request(url: str) -> dict[str, Any] | None:
    """Make a request to the Riot API with proper error handling."""
    logger.info(f"Making Riot API request to: {url}")
    
    if not API_KEY:
        logger.error("RIOT_API_KEY environment variable not set")
        return {"error": "RIOT_API_KEY environment variable not set"}
    
    headers = {
        "User-Agent": USER_AGENT,
        "X-Riot-Token": API_KEY,
        "Accept": "application/json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            data = response.json()
            logger.info(f"Successfully received response from Riot API")
            logger.debug(f"Response data: {data}")
            return data
        except httpx.HTTPStatusError as e:
            error_msg = f"HTTP {e.response.status_code}: {e.response.text}"
            logger.error(f"Riot API HTTP error: {error_msg}")
            return {"error": error_msg}
        except Exception as e:
            error_msg = f"Request failed: {str(e)}"
            logger.error(f"Riot API request failed: {error_msg}")
            return {"error": error_msg}

def format_account(account_data: dict) -> str:
    """Format account data into a readable string."""
    if "error" in account_data:
        return f"Error: {account_data['error']}"
    
    puuid = account_data.get('puuid', 'N/A')
    game_name = account_data.get('gameName', 'N/A')
    tag_line = account_data.get('tagLine', 'N/A')
    
    return f"""
PUUID: {puuid}
Game Name: {game_name}
Tag Line: {tag_line}
Riot ID: {game_name}#{tag_line}
"""

@mcp.tool()
async def get_account_by_puuid(puuid: str, region: str = "americas") -> str:
    """Get account information by PUUID.

    Args:
        puuid: Encrypted PUUID (78 characters)
        region: Routing region (americas, asia, europe)
    """
    logger.info(f"Tool called: get_account_by_puuid(puuid={puuid[:8]}..., region={region})")
    
    base_url = RIOT_API_BASE.format(region=region)
    url = f"{base_url}/riot/account/v1/accounts/by-puuid/{puuid}"
    data = await make_riot_request(url)
    
    if not data:
        logger.warning("No data received from Riot API")
        return "Unable to fetch account data."
    
    result = format_account(data)
    logger.info(f"get_account_by_puuid completed successfully")
    return result

@mcp.tool()
async def get_account_by_riot_id(game_name: str, tag_line: str, region: str = "americas") -> str:
    """Get account information by Riot ID (gameName#tagLine).

    Args:
        game_name: The game name part of the Riot ID
        tag_line: The tag line part of the Riot ID  
        region: Routing region (americas, asia, europe)
    """
    logger.info(f"Tool called: get_account_by_riot_id(game_name={game_name}, tag_line={tag_line}, region={region})")
    
    base_url = RIOT_API_BASE.format(region=region)
    url = f"{base_url}/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
    data = await make_riot_request(url)
    
    if not data:
        logger.warning("No data received from Riot API")
        return "Unable to fetch account data."
    
    result = format_account(data)
    logger.info(f"get_account_by_riot_id completed successfully")
    return result

@mcp.tool()
async def get_active_shard(game: str, puuid: str, region: str = "americas") -> str:
    """Get active shard for a player.

    Args:
        game: Game identifier (e.g., 'val' for VALORANT, 'lor' for Legends of Runeterra)
        puuid: Encrypted PUUID (78 characters)
        region: Routing region (americas, asia, europe)
    """
    logger.info(f"Tool called: get_active_shard(game={game}, puuid={puuid[:8]}..., region={region})")
    
    base_url = RIOT_API_BASE.format(region=region)
    url = f"{base_url}/riot/account/v1/active-shards/by-game/{game}/by-puuid/{puuid}"
    data = await make_riot_request(url)
    
    if not data:
        logger.warning("No data received from Riot API")
        return "Unable to fetch active shard data."
    
    if "error" in data:
        logger.warning(f"Error in API response: {data['error']}")
        return f"Error: {data['error']}"
    
    result = f"""
Game: {data.get('game', 'N/A')}
Active Shard: {data.get('activeShard', 'N/A')}
PUUID: {data.get('puuid', 'N/A')}
"""
    logger.info(f"get_active_shard completed successfully")
    return result

@mcp.tool()
async def get_active_region(game: str, puuid: str, region: str = "americas") -> str:
    """Get active region for a player (LoL and TFT).

    Args:
        game: Game identifier (e.g., 'lol' for League of Legends, 'tft' for Teamfight Tactics)
        puuid: Encrypted PUUID (78 characters)
        region: Routing region (americas, asia, europe)
    """
    logger.info(f"Tool called: get_active_region(game={game}, puuid={puuid[:8]}..., region={region})")
    
    base_url = RIOT_API_BASE.format(region=region)
    url = f"{base_url}/riot/account/v1/region/by-game/{game}/by-puuid/{puuid}"
    data = await make_riot_request(url)
    
    if not data:
        logger.warning("No data received from Riot API")
        return "Unable to fetch active region data."
    
    if "error" in data:
        logger.warning(f"Error in API response: {data['error']}")
        return f"Error: {data['error']}"
    
    result = f"""
PUUID: {data.get('puuid', 'N/A')}
Game: {data.get('game', 'N/A')}
Active Region: {data.get('region', 'N/A')}
"""
    logger.info(f"get_active_region completed successfully")
    return result

if __name__ == "__main__":
    logger.info("Starting League MCP Server...")
    # Initialize and run the server
    mcp.run(transport='stdio')