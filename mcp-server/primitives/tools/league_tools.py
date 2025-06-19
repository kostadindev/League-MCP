"""League API tools for League of Legends."""

import logging
from mcp.server.fastmcp import FastMCP
from services.riot_api_service import make_riot_request, RIOT_API_BASE, LOL_REGIONS
from utils.formatters import format_league_list, format_league_entries

logger = logging.getLogger(__name__)


def register_league_tools(mcp: FastMCP):
    """Register all league-related tools."""
    
    @mcp.tool()
    async def get_challenger_league(queue: str, region: str = "na1") -> str:
        """Get the challenger league for a given queue.

        Args:
            queue: Queue type (e.g., RANKED_SOLO_5x5, RANKED_FLEX_SR)
            region: LoL regional server (na1, euw1, eun1, kr, jp1, br1, la1, la2, oc1, tr1, ru)
        """
        logger.info(f"Tool called: get_challenger_league(queue={queue}, region={region})")
        
        if region not in LOL_REGIONS:
            logger.warning(f"Invalid region specified: {region}")
            return f"Error: Invalid region '{region}'. Valid regions: {', '.join(LOL_REGIONS)}"
        
        base_url = RIOT_API_BASE.format(region=region)
        url = f"{base_url}/lol/league/v4/challengerleagues/by-queue/{queue}"
        data = await make_riot_request(url)
        
        if not data:
            logger.warning("No data received from Riot API")
            return "Unable to fetch challenger league data."
        
        result = format_league_list(data)
        logger.info(f"get_challenger_league completed successfully")
        return result

    @mcp.tool()
    async def get_grandmaster_league(queue: str, region: str = "na1") -> str:
        """Get the grandmaster league for a given queue.

        Args:
            queue: Queue type (e.g., RANKED_SOLO_5x5, RANKED_FLEX_SR)
            region: LoL regional server (na1, euw1, eun1, kr, jp1, br1, la1, la2, oc1, tr1, ru)
        """
        logger.info(f"Tool called: get_grandmaster_league(queue={queue}, region={region})")
        
        if region not in LOL_REGIONS:
            logger.warning(f"Invalid region specified: {region}")
            return f"Error: Invalid region '{region}'. Valid regions: {', '.join(LOL_REGIONS)}"
        
        base_url = RIOT_API_BASE.format(region=region)
        url = f"{base_url}/lol/league/v4/grandmasterleagues/by-queue/{queue}"
        data = await make_riot_request(url)
        
        if not data:
            logger.warning("No data received from Riot API")
            return "Unable to fetch grandmaster league data."
        
        result = format_league_list(data)
        logger.info(f"get_grandmaster_league completed successfully")
        return result

    @mcp.tool()
    async def get_master_league(queue: str, region: str = "na1") -> str:
        """Get the master league for a given queue.

        Args:
            queue: Queue type (e.g., RANKED_SOLO_5x5, RANKED_FLEX_SR)
            region: LoL regional server (na1, euw1, eun1, kr, jp1, br1, la1, la2, oc1, tr1, ru)
        """
        logger.info(f"Tool called: get_master_league(queue={queue}, region={region})")
        
        if region not in LOL_REGIONS:
            logger.warning(f"Invalid region specified: {region}")
            return f"Error: Invalid region '{region}'. Valid regions: {', '.join(LOL_REGIONS)}"
        
        base_url = RIOT_API_BASE.format(region=region)
        url = f"{base_url}/lol/league/v4/masterleagues/by-queue/{queue}"
        data = await make_riot_request(url)
        
        if not data:
            logger.warning("No data received from Riot API")
            return "Unable to fetch master league data."
        
        result = format_league_list(data)
        logger.info(f"get_master_league completed successfully")
        return result

    @mcp.tool()
    async def get_league_entries_by_puuid(puuid: str, region: str = "na1") -> str:
        """Get league entries in all queues for a given PUUID.

        Args:
            puuid: Encrypted PUUID (78 characters) of the summoner
            region: LoL regional server (na1, euw1, eun1, kr, jp1, br1, la1, la2, oc1, tr1, ru)
        """
        logger.info(f"Tool called: get_league_entries_by_puuid(puuid={puuid[:8]}..., region={region})")
        
        if region not in LOL_REGIONS:
            logger.warning(f"Invalid region specified: {region}")
            return f"Error: Invalid region '{region}'. Valid regions: {', '.join(LOL_REGIONS)}"
        
        base_url = RIOT_API_BASE.format(region=region)
        url = f"{base_url}/lol/league/v4/entries/by-puuid/{puuid}"
        data = await make_riot_request(url)
        
        if not data:
            logger.warning("No data received from Riot API")
            return "Unable to fetch league entries data."
        
        result = format_league_entries(data)
        logger.info(f"get_league_entries_by_puuid completed successfully")
        return result

    @mcp.tool()
    async def get_league_entries_by_summoner_id(summoner_id: str, region: str = "na1") -> str:
        """Get league entries in all queues for a given summoner ID.

        Args:
            summoner_id: Encrypted summoner ID (max 63 characters)
            region: LoL regional server (na1, euw1, eun1, kr, jp1, br1, la1, la2, oc1, tr1, ru)
        """
        logger.info(f"Tool called: get_league_entries_by_summoner_id(summoner_id={summoner_id[:8]}..., region={region})")
        
        if region not in LOL_REGIONS:
            logger.warning(f"Invalid region specified: {region}")
            return f"Error: Invalid region '{region}'. Valid regions: {', '.join(LOL_REGIONS)}"
        
        base_url = RIOT_API_BASE.format(region=region)
        url = f"{base_url}/lol/league/v4/entries/by-summoner/{summoner_id}"
        data = await make_riot_request(url)
        
        if not data:
            logger.warning("No data received from Riot API")
            return "Unable to fetch league entries data."
        
        result = format_league_entries(data)
        logger.info(f"get_league_entries_by_summoner_id completed successfully")
        return result

    @mcp.tool()
    async def get_league_by_id(league_id: str, region: str = "na1") -> str:
        """Get league with given ID, including inactive entries.

        Args:
            league_id: The UUID of the league
            region: LoL regional server (na1, euw1, eun1, kr, jp1, br1, la1, la2, oc1, tr1, ru)
        """
        logger.info(f"Tool called: get_league_by_id(league_id={league_id}, region={region})")
        
        if region not in LOL_REGIONS:
            logger.warning(f"Invalid region specified: {region}")
            return f"Error: Invalid region '{region}'. Valid regions: {', '.join(LOL_REGIONS)}"
        
        base_url = RIOT_API_BASE.format(region=region)
        url = f"{base_url}/lol/league/v4/leagues/{league_id}"
        data = await make_riot_request(url)
        
        if not data:
            logger.warning("No data received from Riot API")
            return "Unable to fetch league data."
        
        result = format_league_list(data)
        logger.info(f"get_league_by_id completed successfully")
        return result

    @mcp.tool()
    async def get_league_entries_by_division(queue: str, tier: str, division: str, page: int = 1, region: str = "na1") -> str:
        """Get all league entries for a specific queue, tier, and division.

        Args:
            queue: Queue type (e.g., RANKED_SOLO_5x5, RANKED_FLEX_SR)
            tier: Tier (e.g., DIAMOND, PLATINUM, GOLD, SILVER, BRONZE, IRON)
            division: Division (I, II, III, IV)
            page: Page number (defaults to 1)
            region: LoL regional server (na1, euw1, eun1, kr, jp1, br1, la1, la2, oc1, tr1, ru)
        """
        logger.info(f"Tool called: get_league_entries_by_division(queue={queue}, tier={tier}, division={division}, page={page}, region={region})")
        
        if region not in LOL_REGIONS:
            logger.warning(f"Invalid region specified: {region}")
            return f"Error: Invalid region '{region}'. Valid regions: {', '.join(LOL_REGIONS)}"
        
        base_url = RIOT_API_BASE.format(region=region)
        url = f"{base_url}/lol/league/v4/entries/{queue}/{tier}/{division}?page={page}"
        data = await make_riot_request(url)
        
        if not data:
            logger.warning("No data received from Riot API")
            return "Unable to fetch league entries data."
        
        result = format_league_entries(data)
        logger.info(f"get_league_entries_by_division completed successfully")
        return result 