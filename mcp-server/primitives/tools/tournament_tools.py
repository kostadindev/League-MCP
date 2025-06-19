"""Tournament API tools for League of Legends."""

import logging
from mcp.server.fastmcp import FastMCP
from services.riot_api_service import make_riot_request, RIOT_API_BASE, LOL_REGIONS

logger = logging.getLogger(__name__)


def register_tournament_tools(mcp: FastMCP):
    """Register all tournament-related tools."""
    
    @mcp.tool()
    async def create_tournament_provider(region: str, url: str) -> str:
        """Register as a tournament provider.

        Args:
            region: The region to register the provider for (BR1, EUN1, EUW1, JP1, KR, LA1, LA2, NA1, OC1, TR1, RU)
            url: The provider's callback URL for tournament updates
        """
        logger.info(f"Tool called: create_tournament_provider(region={region}, url={url})")
        
        if region not in LOL_REGIONS:
            logger.warning(f"Invalid region specified: {region}")
            return f"Error: Invalid region '{region}'. Valid regions: {', '.join(LOL_REGIONS)}"
        
        base_url = RIOT_API_BASE.format(region=region)
        url_endpoint = f"{base_url}/lol/tournament/v5/providers"
        
        payload = {
            "region": region,
            "url": url
        }
        
        # This would require a POST request with API key authentication
        # For now, return a placeholder response
        result = f"""
TOURNAMENT PROVIDER REGISTRATION
===============================
This endpoint requires POST request with API key authentication.

Request would be sent to: {url_endpoint}
Payload:
  Region: {region}
  Callback URL: {url}

Note: This is a production-level feature that requires:
1. A Production API Key
2. Proper tournament organizer verification
3. Adherence to tournament policies

Please refer to the Tournament API documentation for complete implementation.
"""
        
        logger.info(f"create_tournament_provider completed successfully")
        return result

    @mcp.tool()
    async def create_tournament(provider_id: int, name: str, region: str) -> str:
        """Create a tournament for a given provider.

        Args:
            provider_id: The provider ID obtained from creating a tournament provider
            name: The tournament name
            region: The region for the tournament
        """
        logger.info(f"Tool called: create_tournament(provider_id={provider_id}, name={name}, region={region})")
        
        if region not in LOL_REGIONS:
            logger.warning(f"Invalid region specified: {region}")
            return f"Error: Invalid region '{region}'. Valid regions: {', '.join(LOL_REGIONS)}"
        
        result = f"""
TOURNAMENT CREATION
==================
This endpoint requires POST request with API key authentication.

Tournament Details:
  Provider ID: {provider_id}
  Name: {name}
  Region: {region}

Note: This is a production-level feature that requires:
1. A valid provider ID from a registered tournament provider
2. Production API Key
3. Adherence to tournament policies

The tournament creation would return a tournament ID for generating tournament codes.
"""
        
        logger.info(f"create_tournament completed successfully")
        return result

    @mcp.tool()
    async def generate_tournament_codes(tournament_id: int, count: int = 1, team_size: int = 5, 
                                       pick_type: str = "TOURNAMENT_DRAFT", map_type: str = "SUMMONERS_RIFT",
                                       spectator_type: str = "LOBBYONLY", region: str = "na1") -> str:
        """Generate tournament codes for a tournament.

        Args:
            tournament_id: The tournament ID
            count: Number of codes to generate (max 1000)
            team_size: Team size (1-5)
            pick_type: Pick type (BLIND_PICK, DRAFT_MODE, ALL_RANDOM, TOURNAMENT_DRAFT)
            map_type: Map type (SUMMONERS_RIFT, TWISTED_TREELINE, HOWLING_ABYSS)
            spectator_type: Spectator type (NONE, LOBBYONLY, ALL)
            region: The region for the tournament
        """
        logger.info(f"Tool called: generate_tournament_codes(tournament_id={tournament_id}, count={count})")
        
        if region not in LOL_REGIONS:
            logger.warning(f"Invalid region specified: {region}")
            return f"Error: Invalid region '{region}'. Valid regions: {', '.join(LOL_REGIONS)}"
        
        if count > 1000:
            return "Error: Maximum 1000 tournament codes can be generated at once."
        
        if team_size < 1 or team_size > 5:
            return "Error: Team size must be between 1 and 5."
        
        result = f"""
TOURNAMENT CODE GENERATION
=========================
This endpoint requires POST request with API key authentication.

Tournament Code Parameters:
  Tournament ID: {tournament_id}
  Number of Codes: {count}
  Team Size: {team_size}
  Pick Type: {pick_type}
  Map Type: {map_type}
  Spectator Type: {spectator_type}
  Region: {region}

Generated codes would be returned as an array of tournament code strings.
Each code can be used to create a custom game lobby with the specified settings.

Note: 
- Tournament codes should be generated as needed, not all at once
- Each code should ideally be used for a single match
- Codes may expire after 3 months of inactivity
"""
        
        logger.info(f"generate_tournament_codes completed successfully")
        return result

    @mcp.tool()
    async def get_tournament_code_details(tournament_code: str, region: str = "na1") -> str:
        """Get tournament code details.

        Args:
            tournament_code: The tournament code
            region: The region for the tournament
        """
        logger.info(f"Tool called: get_tournament_code_details(tournament_code={tournament_code}, region={region})")
        
        if region not in LOL_REGIONS:
            logger.warning(f"Invalid region specified: {region}")
            return f"Error: Invalid region '{region}'. Valid regions: {', '.join(LOL_REGIONS)}"
        
        base_url = RIOT_API_BASE.format(region=region)
        url = f"{base_url}/lol/tournament/v5/codes/{tournament_code}"
        data = await make_riot_request(url)
        
        if not data:
            logger.warning("No data received from Riot API")
            return "Unable to fetch tournament code details."
        
        if "error" in data:
            return f"Error: {data['error']}"
        
        result = f"""
TOURNAMENT CODE DETAILS
======================
Tournament Code: {tournament_code}
Tournament ID: {data.get('tournamentId', 'N/A')}
Provider ID: {data.get('providerId', 'N/A')}
Team Size: {data.get('teamSize', 'N/A')}
Pick Type: {data.get('pickType', 'N/A')}
Map Type: {data.get('mapType', 'N/A')}
Spectator Type: {data.get('spectatorType', 'N/A')}
Metadata: {data.get('metaData', 'N/A')}
Participants: {len(data.get('participants', []))}
"""
        
        if data.get('participants'):
            result += "\nParticipants:\n"
            for participant in data.get('participants', []):
                result += f"  - {participant}\n"
        
        logger.info(f"get_tournament_code_details completed successfully")
        return result

    @mcp.tool()
    async def get_tournament_lobby_events(tournament_code: str, region: str = "na1") -> str:
        """Get lobby events for a tournament code.

        Args:
            tournament_code: The tournament code
            region: The region for the tournament
        """
        logger.info(f"Tool called: get_tournament_lobby_events(tournament_code={tournament_code}, region={region})")
        
        if region not in LOL_REGIONS:
            logger.warning(f"Invalid region specified: {region}")
            return f"Error: Invalid region '{region}'. Valid regions: {', '.join(LOL_REGIONS)}"
        
        base_url = RIOT_API_BASE.format(region=region)
        url = f"{base_url}/lol/tournament/v5/lobby-events/by-code/{tournament_code}"
        data = await make_riot_request(url)
        
        if not data:
            logger.warning("No data received from Riot API")
            return "Unable to fetch tournament lobby events."
        
        if "error" in data:
            return f"Error: {data['error']}"
        
        events = data.get('eventList', [])
        
        result = f"""
TOURNAMENT LOBBY EVENTS
======================
Tournament Code: {tournament_code}
Total Events: {len(events)}

EVENT TIMELINE:
"""
        
        import datetime
        
        for i, event in enumerate(events, 1):
            timestamp = event.get('timestamp', 0)
            event_type = event.get('eventType', 'Unknown')
            summoner_id = event.get('summonerId', 'N/A')
            
            # Convert timestamp
            try:
                event_time = datetime.datetime.fromtimestamp(int(timestamp) / 1000).strftime('%H:%M:%S') if timestamp else 'N/A'
            except (ValueError, TypeError):
                event_time = f"Raw: {timestamp}"
            
            result += f"""
{i:2d}. [{event_time}] {event_type}
    Summoner ID: {summoner_id}
"""
        
        if not events:
            result += "No lobby events found for this tournament code."
        
        logger.info(f"get_tournament_lobby_events completed successfully")
        return result 