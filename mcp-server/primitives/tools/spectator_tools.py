"""Spectator API tools for League of Legends."""

import logging
from mcp.server.fastmcp import FastMCP
from services.riot_api_service import make_riot_request, RIOT_API_BASE, LOL_REGIONS
from utils.formatters import format_active_game, format_featured_games

logger = logging.getLogger(__name__)


def register_spectator_tools(mcp: FastMCP):
    """Register all spectator-related tools."""
    
    @mcp.tool()
    async def get_active_game(puuid: str, region: str = "na1") -> str:
        """Get current active game information for a summoner by PUUID.

        Args:
            puuid: Encrypted PUUID (78 characters) of the summoner
            region: LoL regional server (na1, euw1, eun1, kr, jp1, br1, la1, la2, oc1, tr1, ru)
        """
        logger.info(f"Tool called: get_active_game(puuid={puuid[:8]}..., region={region})")
        
        if region not in LOL_REGIONS:
            logger.warning(f"Invalid region specified: {region}")
            return f"Error: Invalid region '{region}'. Valid regions: {', '.join(LOL_REGIONS)}"
        
        base_url = RIOT_API_BASE.format(region=region)
        url = f"{base_url}/lol/spectator/v5/active-games/by-summoner/{puuid}"
        data = await make_riot_request(url)
        
        if not data:
            logger.warning("No data received from Riot API")
            return "Unable to fetch active game data."
        
        result = format_active_game(data)
        logger.info(f"get_active_game completed successfully")
        return result

    @mcp.tool()
    async def get_featured_games(region: str = "na1") -> str:
        """Get list of currently featured games.

        Args:
            region: LoL regional server (na1, euw1, eun1, kr, jp1, br1, la1, la2, oc1, tr1, ru)
        """
        logger.info(f"Tool called: get_featured_games(region={region})")
        
        if region not in LOL_REGIONS:
            logger.warning(f"Invalid region specified: {region}")
            return f"Error: Invalid region '{region}'. Valid regions: {', '.join(LOL_REGIONS)}"
        
        base_url = RIOT_API_BASE.format(region=region)
        url = f"{base_url}/lol/spectator/v5/featured-games"
        data = await make_riot_request(url)
        
        if not data:
            logger.warning("No data received from Riot API")
            return "Unable to fetch featured games data."
        
        result = format_featured_games(data)
        logger.info(f"get_featured_games completed successfully")
        return result 