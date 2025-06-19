"""Summoner API tools for League of Legends."""

import logging
from mcp.server.fastmcp import FastMCP
from services.riot_api_service import make_riot_request, RIOT_API_BASE, LOL_REGIONS
from utils.formatters import format_summoner

logger = logging.getLogger(__name__)


def register_summoner_tools(mcp: FastMCP):
    """Register all summoner-related tools."""
    
    @mcp.tool()
    async def get_summoner_by_puuid(puuid: str, region: str = "na1") -> str:
        """Get summoner information by PUUID.

        Args:
            puuid: Encrypted PUUID (78 characters) of the summoner
            region: LoL regional server (na1, euw1, eun1, kr, jp1, br1, la1, la2, oc1, tr1, ru)
        """
        logger.info(f"Tool called: get_summoner_by_puuid(puuid={puuid[:8]}..., region={region})")
        
        if region not in LOL_REGIONS:
            logger.warning(f"Invalid region specified: {region}")
            return f"Error: Invalid region '{region}'. Valid regions: {', '.join(LOL_REGIONS)}"
        
        base_url = RIOT_API_BASE.format(region=region)
        url = f"{base_url}/lol/summoner/v4/summoners/by-puuid/{puuid}"
        data = await make_riot_request(url)
        
        if not data:
            logger.warning("No data received from Riot API")
            return "Unable to fetch summoner data."
        
        result = format_summoner(data)
        logger.info(f"get_summoner_by_puuid completed successfully")
        return result

    @mcp.tool()
    async def get_summoner_by_account_id(account_id: str, region: str = "na1") -> str:
        """Get summoner information by encrypted account ID.

        Args:
            account_id: Encrypted account ID (max 56 characters)
            region: LoL regional server (na1, euw1, eun1, kr, jp1, br1, la1, la2, oc1, tr1, ru)
        """
        logger.info(f"Tool called: get_summoner_by_account_id(account_id={account_id[:8]}..., region={region})")
        
        if region not in LOL_REGIONS:
            logger.warning(f"Invalid region specified: {region}")
            return f"Error: Invalid region '{region}'. Valid regions: {', '.join(LOL_REGIONS)}"
        
        base_url = RIOT_API_BASE.format(region=region)
        url = f"{base_url}/lol/summoner/v4/summoners/by-account/{account_id}"
        data = await make_riot_request(url)
        
        if not data:
            logger.warning("No data received from Riot API")
            return "Unable to fetch summoner data."
        
        result = format_summoner(data)
        logger.info(f"get_summoner_by_account_id completed successfully")
        return result

    @mcp.tool()
    async def get_summoner_by_summoner_id(summoner_id: str, region: str = "na1") -> str:
        """Get summoner information by encrypted summoner ID.

        Args:
            summoner_id: Encrypted summoner ID (max 63 characters)
            region: LoL regional server (na1, euw1, eun1, kr, jp1, br1, la1, la2, oc1, tr1, ru)
        """
        logger.info(f"Tool called: get_summoner_by_summoner_id(summoner_id={summoner_id[:8]}..., region={region})")
        
        if region not in LOL_REGIONS:
            logger.warning(f"Invalid region specified: {region}")
            return f"Error: Invalid region '{region}'. Valid regions: {', '.join(LOL_REGIONS)}"
        
        base_url = RIOT_API_BASE.format(region=region)
        url = f"{base_url}/lol/summoner/v4/summoners/{summoner_id}"
        data = await make_riot_request(url)
        
        if not data:
            logger.warning("No data received from Riot API")
            return "Unable to fetch summoner data."
        
        result = format_summoner(data)
        logger.info(f"get_summoner_by_summoner_id completed successfully")
        return result

    @mcp.tool()
    async def get_summoner_by_rso_puuid(rso_puuid: str, region: str = "na1") -> str:
        """Get summoner information by RSO encrypted PUUID (fulfillment endpoint).

        Args:
            rso_puuid: RSO encrypted PUUID 
            region: LoL regional server (na1, euw1, eun1, kr, jp1, br1, la1, la2, oc1, tr1, ru)
        """
        logger.info(f"Tool called: get_summoner_by_rso_puuid(rso_puuid={rso_puuid[:8]}..., region={region})")
        
        if region not in LOL_REGIONS:
            logger.warning(f"Invalid region specified: {region}")
            return f"Error: Invalid region '{region}'. Valid regions: {', '.join(LOL_REGIONS)}"
        
        base_url = RIOT_API_BASE.format(region=region)
        url = f"{base_url}/fulfillment/v1/summoners/by-puuid/{rso_puuid}"
        data = await make_riot_request(url)
        
        if not data:
            logger.warning("No data received from Riot API")
            return "Unable to fetch summoner data."
        
        result = format_summoner(data)
        logger.info(f"get_summoner_by_rso_puuid completed successfully")
        return result 