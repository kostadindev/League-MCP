"""Clash API tools for League of Legends."""

import logging
from mcp.server.fastmcp import FastMCP
from services.riot_api_service import make_riot_request, RIOT_API_BASE, LOL_REGIONS
from utils.formatters import format_clash_player, format_clash_team, format_clash_tournaments, format_clash_tournament

logger = logging.getLogger(__name__)


def register_clash_tools(mcp: FastMCP):
    """Register all clash-related tools."""
    
    @mcp.tool()
    async def get_clash_players_by_puuid(puuid: str, region: str = "na1") -> str:
        """Get active Clash players/registrations for a given PUUID.

        Args:
            puuid: Encrypted PUUID (78 characters) of the summoner
            region: LoL regional server (na1, euw1, eun1, kr, jp1, br1, la1, la2, oc1, tr1, ru)
        """
        logger.info(f"Tool called: get_clash_players_by_puuid(puuid={puuid[:8]}..., region={region})")
        
        if region not in LOL_REGIONS:
            logger.warning(f"Invalid region specified: {region}")
            return f"Error: Invalid region '{region}'. Valid regions: {', '.join(LOL_REGIONS)}"
        
        base_url = RIOT_API_BASE.format(region=region)
        url = f"{base_url}/lol/clash/v1/players/by-puuid/{puuid}"
        data = await make_riot_request(url)
        
        if not data:
            logger.warning("No data received from Riot API")
            return "Unable to fetch Clash player data."
        
        result = format_clash_player(data)
        logger.info(f"get_clash_players_by_puuid completed successfully")
        return result

    @mcp.tool()
    async def get_clash_team(team_id: str, region: str = "na1") -> str:
        """Get Clash team information by team ID.

        Args:
            team_id: The Clash team ID
            region: LoL regional server (na1, euw1, eun1, kr, jp1, br1, la1, la2, oc1, tr1, ru)
        """
        logger.info(f"Tool called: get_clash_team(team_id={team_id}, region={region})")
        
        if region not in LOL_REGIONS:
            logger.warning(f"Invalid region specified: {region}")
            return f"Error: Invalid region '{region}'. Valid regions: {', '.join(LOL_REGIONS)}"
        
        base_url = RIOT_API_BASE.format(region=region)
        url = f"{base_url}/lol/clash/v1/teams/{team_id}"
        data = await make_riot_request(url)
        
        if not data:
            logger.warning("No data received from Riot API")
            return "Unable to fetch Clash team data."
        
        result = format_clash_team(data)
        logger.info(f"get_clash_team completed successfully")
        return result

    @mcp.tool()
    async def get_clash_tournaments(region: str = "na1") -> str:
        """Get all active or upcoming Clash tournaments.

        Args:
            region: LoL regional server (na1, euw1, eun1, kr, jp1, br1, la1, la2, oc1, tr1, ru)
        """
        logger.info(f"Tool called: get_clash_tournaments(region={region})")
        
        if region not in LOL_REGIONS:
            logger.warning(f"Invalid region specified: {region}")
            return f"Error: Invalid region '{region}'. Valid regions: {', '.join(LOL_REGIONS)}"
        
        base_url = RIOT_API_BASE.format(region=region)
        url = f"{base_url}/lol/clash/v1/tournaments"
        data = await make_riot_request(url)
        
        if not data:
            logger.warning("No data received from Riot API")
            return "Unable to fetch Clash tournaments data."
        
        result = format_clash_tournaments(data)
        logger.info(f"get_clash_tournaments completed successfully")
        return result

    @mcp.tool()
    async def get_clash_tournament_by_team(team_id: str, region: str = "na1") -> str:
        """Get Clash tournament information by team ID.

        Args:
            team_id: The Clash team ID
            region: LoL regional server (na1, euw1, eun1, kr, jp1, br1, la1, la2, oc1, tr1, ru)
        """
        logger.info(f"Tool called: get_clash_tournament_by_team(team_id={team_id}, region={region})")
        
        if region not in LOL_REGIONS:
            logger.warning(f"Invalid region specified: {region}")
            return f"Error: Invalid region '{region}'. Valid regions: {', '.join(LOL_REGIONS)}"
        
        base_url = RIOT_API_BASE.format(region=region)
        url = f"{base_url}/lol/clash/v1/tournaments/by-team/{team_id}"
        data = await make_riot_request(url)
        
        if not data:
            logger.warning("No data received from Riot API")
            return "Unable to fetch Clash tournament data."
        
        result = format_clash_tournament(data)
        logger.info(f"get_clash_tournament_by_team completed successfully")
        return result

    @mcp.tool()
    async def get_clash_tournament_by_id(tournament_id: int, region: str = "na1") -> str:
        """Get Clash tournament information by tournament ID.

        Args:
            tournament_id: The Clash tournament ID
            region: LoL regional server (na1, euw1, eun1, kr, jp1, br1, la1, la2, oc1, tr1, ru)
        """
        logger.info(f"Tool called: get_clash_tournament_by_id(tournament_id={tournament_id}, region={region})")
        
        if region not in LOL_REGIONS:
            logger.warning(f"Invalid region specified: {region}")
            return f"Error: Invalid region '{region}'. Valid regions: {', '.join(LOL_REGIONS)}"
        
        base_url = RIOT_API_BASE.format(region=region)
        url = f"{base_url}/lol/clash/v1/tournaments/{tournament_id}"
        data = await make_riot_request(url)
        
        if not data:
            logger.warning("No data received from Riot API")
            return "Unable to fetch Clash tournament data."
        
        result = format_clash_tournament(data)
        logger.info(f"get_clash_tournament_by_id completed successfully")
        return result 