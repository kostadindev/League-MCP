"""Status API tools for League of Legends."""

import logging
from mcp.server.fastmcp import FastMCP
from services.riot_api_service import make_riot_request, RIOT_API_BASE, LOL_REGIONS
from utils.formatters import format_platform_status

logger = logging.getLogger(__name__)


def register_status_tools(mcp: FastMCP):
    """Register all status-related tools."""
    
    @mcp.tool()
    async def get_platform_status(region: str = "na1") -> str:
        """Get League of Legends status for the given platform.

        Args:
            region: LoL regional server (na1, euw1, eun1, kr, jp1, br1, la1, la2, oc1, tr1, ru)
        """
        logger.info(f"Tool called: get_platform_status(region={region})")
        
        if region not in LOL_REGIONS:
            logger.warning(f"Invalid region specified: {region}")
            return f"Error: Invalid region '{region}'. Valid regions: {', '.join(LOL_REGIONS)}"
        
        base_url = RIOT_API_BASE.format(region=region)
        url = f"{base_url}/lol/status/v4/platform-data"
        data = await make_riot_request(url)
        
        if not data:
            logger.warning("No data received from Riot API")
            return "Unable to fetch platform status data."
        
        result = format_platform_status(data)
        logger.info(f"get_platform_status completed successfully")
        return result 