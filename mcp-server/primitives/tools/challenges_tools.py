"""Challenges API tools for League of Legends."""

import logging
from mcp.server.fastmcp import FastMCP
from services.riot_api_service import make_riot_request, RIOT_API_BASE, LOL_REGIONS
from utils.formatters import format_challenge_configs, format_challenge_config, format_challenge_leaderboard, format_player_challenges

logger = logging.getLogger(__name__)


def register_challenges_tools(mcp: FastMCP):
    """Register all challenges-related tools."""
    
    @mcp.tool()
    async def get_challenge_configs(region: str = "na1") -> str:
        """Get list of all basic challenge configuration information.

        Args:
            region: LoL regional server (na1, euw1, eun1, kr, jp1, br1, la1, la2, oc1, tr1, ru)
        """
        logger.info(f"Tool called: get_challenge_configs(region={region})")
        
        if region not in LOL_REGIONS:
            logger.warning(f"Invalid region specified: {region}")
            return f"Error: Invalid region '{region}'. Valid regions: {', '.join(LOL_REGIONS)}"
        
        base_url = RIOT_API_BASE.format(region=region)
        url = f"{base_url}/lol/challenges/v1/challenges/config"
        data = await make_riot_request(url)
        
        if not data:
            logger.warning("No data received from Riot API")
            return "Unable to fetch challenge configs data."
        
        result = format_challenge_configs(data)
        logger.info(f"get_challenge_configs completed successfully")
        return result

    @mcp.tool()
    async def get_challenge_config(challenge_id: int, region: str = "na1") -> str:
        """Get challenge configuration for a specific challenge.

        Args:
            challenge_id: The challenge ID
            region: LoL regional server (na1, euw1, eun1, kr, jp1, br1, la1, la2, oc1, tr1, ru)
        """
        logger.info(f"Tool called: get_challenge_config(challenge_id={challenge_id}, region={region})")
        
        if region not in LOL_REGIONS:
            logger.warning(f"Invalid region specified: {region}")
            return f"Error: Invalid region '{region}'. Valid regions: {', '.join(LOL_REGIONS)}"
        
        base_url = RIOT_API_BASE.format(region=region)
        url = f"{base_url}/lol/challenges/v1/challenges/{challenge_id}/config"
        data = await make_riot_request(url)
        
        if not data:
            logger.warning("No data received from Riot API")
            return "Unable to fetch challenge config data."
        
        result = format_challenge_config(data)
        logger.info(f"get_challenge_config completed successfully")
        return result

    @mcp.tool()
    async def get_challenge_leaderboard(challenge_id: int, level: str, limit: int = 50, region: str = "na1") -> str:
        """Get top players for a challenge at a specific level.

        Args:
            challenge_id: The challenge ID
            level: Level (MASTER, GRANDMASTER, or CHALLENGER)
            limit: Number of players to return (defaults to 50)
            region: LoL regional server (na1, euw1, eun1, kr, jp1, br1, la1, la2, oc1, tr1, ru)
        """
        logger.info(f"Tool called: get_challenge_leaderboard(challenge_id={challenge_id}, level={level}, limit={limit}, region={region})")
        
        if region not in LOL_REGIONS:
            logger.warning(f"Invalid region specified: {region}")
            return f"Error: Invalid region '{region}'. Valid regions: {', '.join(LOL_REGIONS)}"
        
        if level.upper() not in ['MASTER', 'GRANDMASTER', 'CHALLENGER']:
            logger.warning(f"Invalid level specified: {level}")
            return f"Error: Invalid level '{level}'. Valid levels: MASTER, GRANDMASTER, CHALLENGER"
        
        base_url = RIOT_API_BASE.format(region=region)
        url = f"{base_url}/lol/challenges/v1/challenges/{challenge_id}/leaderboards/by-level/{level.upper()}?limit={limit}"
        data = await make_riot_request(url)
        
        if not data:
            logger.warning("No data received from Riot API")
            return "Unable to fetch challenge leaderboard data."
        
        result = format_challenge_leaderboard(data, level)
        logger.info(f"get_challenge_leaderboard completed successfully")
        return result

    @mcp.tool()
    async def get_player_challenges(puuid: str, region: str = "na1") -> str:
        """Get player challenge information with list of all progressed challenges.

        Args:
            puuid: Encrypted PUUID (78 characters) of the summoner
            region: LoL regional server (na1, euw1, eun1, kr, jp1, br1, la1, la2, oc1, tr1, ru)
        """
        logger.info(f"Tool called: get_player_challenges(puuid={puuid[:8]}..., region={region})")
        
        if region not in LOL_REGIONS:
            logger.warning(f"Invalid region specified: {region}")
            return f"Error: Invalid region '{region}'. Valid regions: {', '.join(LOL_REGIONS)}"
        
        base_url = RIOT_API_BASE.format(region=region)
        url = f"{base_url}/lol/challenges/v1/player-data/{puuid}"
        data = await make_riot_request(url)
        
        if not data:
            logger.warning("No data received from Riot API")
            return "Unable to fetch player challenges data."
        
        result = format_player_challenges(data)
        logger.info(f"get_player_challenges completed successfully")
        return result

    @mcp.tool()
    async def get_challenge_percentiles(region: str = "na1") -> str:
        """Get challenge percentile data for all challenges.

        Args:
            region: LoL regional server (na1, euw1, eun1, kr, jp1, br1, la1, la2, oc1, tr1, ru)
        """
        logger.info(f"Tool called: get_challenge_percentiles(region={region})")
        
        if region not in LOL_REGIONS:
            logger.warning(f"Invalid region specified: {region}")
            return f"Error: Invalid region '{region}'. Valid regions: {', '.join(LOL_REGIONS)}"
        
        base_url = RIOT_API_BASE.format(region=region)
        url = f"{base_url}/lol/challenges/v1/challenges/percentiles"
        data = await make_riot_request(url)
        
        if not data:
            logger.warning("No data received from Riot API")
            return "Unable to fetch challenge percentiles data."
        
        if "error" in data:
            return f"Error: {data['error']}"
        
        result = f"""
CHALLENGE PERCENTILES
====================
Total Challenges: {len(data)}

SAMPLE PERCENTILE DATA:
"""
        
        # Show first 10 challenges as examples
        for i, (challenge_id, percentiles) in enumerate(list(data.items())[:10], 1):
            result += f"""
Challenge ID {challenge_id}:
  Iron: {percentiles.get('IRON', 'N/A')}
  Bronze: {percentiles.get('BRONZE', 'N/A')}
  Silver: {percentiles.get('SILVER', 'N/A')}
  Gold: {percentiles.get('GOLD', 'N/A')}
  Platinum: {percentiles.get('PLATINUM', 'N/A')}
  Diamond: {percentiles.get('DIAMOND', 'N/A')}
  Master: {percentiles.get('MASTER', 'N/A')}
  Grandmaster: {percentiles.get('GRANDMASTER', 'N/A')}
  Challenger: {percentiles.get('CHALLENGER', 'N/A')}
"""
        
        if len(data) > 10:
            result += f"\n... and {len(data) - 10} more challenges"
        
        logger.info(f"get_challenge_percentiles completed successfully")
        return result 