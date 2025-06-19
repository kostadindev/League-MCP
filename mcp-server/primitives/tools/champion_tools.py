"""Champion API tools for League of Legends."""

import logging
from mcp.server.fastmcp import FastMCP
from services.riot_api_service import make_riot_request, RIOT_API_BASE, LOL_REGIONS
from utils.formatters import format_champion_rotation

logger = logging.getLogger(__name__)


def register_champion_tools(mcp: FastMCP):
    """Register all champion-related tools."""
    
    @mcp.tool()
    async def get_champion_rotation(region: str = "na1") -> str:
        """Get current champion rotation (free-to-play champions).

        Args:
            region: LoL regional server (na1, euw1, eun1, kr, jp1, br1, la1, la2, oc1, tr1, ru)
        """
        logger.info(f"Tool called: get_champion_rotation(region={region})")
        
        if region not in LOL_REGIONS:
            logger.warning(f"Invalid region specified: {region}")
            return f"Error: Invalid region '{region}'. Valid regions: {', '.join(LOL_REGIONS)}"
        
        base_url = RIOT_API_BASE.format(region=region)
        url = f"{base_url}/lol/platform/v3/champion-rotations"
        data = await make_riot_request(url)
        
        if not data:
            logger.warning("No data received from Riot API")
            return "Unable to fetch champion rotation data."
        
        result = format_champion_rotation(data)
        logger.info(f"get_champion_rotation completed successfully")
        return result 