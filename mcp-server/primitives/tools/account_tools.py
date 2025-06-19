"""Account API tools for Riot Games."""

import logging
from mcp.server.fastmcp import FastMCP
from services.riot_api_service import make_riot_request, RIOT_API_BASE, LOL_REGIONS
from utils.formatters import format_account

logger = logging.getLogger(__name__)


def register_account_tools(mcp: FastMCP):
    """Register all account-related tools."""
    
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