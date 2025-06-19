"""Match API tools for League of Legends."""

import logging
from mcp.server.fastmcp import FastMCP
from services.riot_api_service import make_riot_request, RIOT_API_BASE, get_routing_region, LOL_REGIONS
from utils.formatters import format_match_ids, format_match_detail, format_match_timeline

logger = logging.getLogger(__name__)


def register_match_tools(mcp: FastMCP):
    """Register all match-related tools."""
    
    @mcp.tool()
    async def get_match_ids_by_puuid(puuid: str, start_time: int = None, end_time: int = None, queue: int = None, 
                                    match_type: str = None, start: int = 0, count: int = 20, region: str = "na1") -> str:
        """Get a list of match IDs by PUUID.

        Args:
            puuid: Encrypted PUUID (78 characters) of the summoner
            start_time: Epoch timestamp in seconds (optional)
            end_time: Epoch timestamp in seconds (optional)
            queue: Filter by specific queue ID (optional)
            match_type: Filter by match type (optional)
            start: Start index (defaults to 0)
            count: Number of match IDs to return (defaults to 20, max 100)
            region: Platform region to determine routing (defaults to "na1")
        """
        logger.info(f"Tool called: get_match_ids_by_puuid(puuid={puuid[:8]}..., region={region})")
        
        if region not in LOL_REGIONS:
            logger.warning(f"Invalid region specified: {region}")
            return f"Error: Invalid region '{region}'. Valid regions: {', '.join(LOL_REGIONS)}"
        
        # Convert platform region to routing region
        routing_region = get_routing_region(region)
        
        base_url = RIOT_API_BASE.format(region=routing_region)
        url = f"{base_url}/lol/match/v5/matches/by-puuid/{puuid}/ids"
        
        # Build query parameters
        params = []
        if start_time:
            params.append(f"startTime={start_time}")
        if end_time:
            params.append(f"endTime={end_time}")
        if queue:
            params.append(f"queue={queue}")
        if match_type:
            params.append(f"type={match_type}")
        if start != 0:
            params.append(f"start={start}")
        if count != 20:
            params.append(f"count={count}")
        
        if params:
            url += "?" + "&".join(params)
        
        data = await make_riot_request(url)
        
        if not data:
            logger.warning("No data received from Riot API")
            return "Unable to fetch match IDs."
        
        result = format_match_ids(data, puuid)
        logger.info(f"get_match_ids_by_puuid completed successfully")
        return result

    @mcp.tool()
    async def get_match_details(match_id: str, region: str = "na1") -> str:
        """Get detailed match information by match ID.

        Args:
            match_id: The match ID
            region: Platform region to determine routing (defaults to "na1")
        """
        logger.info(f"Tool called: get_match_details(match_id={match_id}, region={region})")
        
        if region not in LOL_REGIONS:
            logger.warning(f"Invalid region specified: {region}")
            return f"Error: Invalid region '{region}'. Valid regions: {', '.join(LOL_REGIONS)}"
        
        # Convert platform region to routing region
        routing_region = get_routing_region(region)
        
        base_url = RIOT_API_BASE.format(region=routing_region)
        url = f"{base_url}/lol/match/v5/matches/{match_id}"
        data = await make_riot_request(url)
        
        if not data:
            logger.warning("No data received from Riot API")
            return "Unable to fetch match details."
        
        result = format_match_detail(data)
        logger.info(f"get_match_details completed successfully")
        return result

    @mcp.tool()
    async def get_match_timeline(match_id: str, region: str = "na1") -> str:
        """Get match timeline by match ID.

        Args:
            match_id: The match ID
            region: Platform region to determine routing (defaults to "na1")
        """
        logger.info(f"Tool called: get_match_timeline(match_id={match_id}, region={region})")
        
        if region not in LOL_REGIONS:
            logger.warning(f"Invalid region specified: {region}")
            return f"Error: Invalid region '{region}'. Valid regions: {', '.join(LOL_REGIONS)}"
        
        # Convert platform region to routing region
        routing_region = get_routing_region(region)
        
        base_url = RIOT_API_BASE.format(region=routing_region)
        url = f"{base_url}/lol/match/v5/matches/{match_id}/timeline"
        data = await make_riot_request(url)
        
        if not data:
            logger.warning("No data received from Riot API")
            return "Unable to fetch match timeline."
        
        result = format_match_timeline(data)
        logger.info(f"get_match_timeline completed successfully")
        return result 