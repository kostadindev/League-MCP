from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("league")

# Constants
RIOT_API_BASE = "https://{region}.api.riotgames.com"
USER_AGENT = "league-mcp-server/1.0"

# Regional endpoints for different APIs
LOL_REGIONS = ["na1", "euw1", "eun1", "kr", "jp1", "br1", "la1", "la2", "oc1", "tr1", "ru"]

# Match v5 API uses routing regions instead of platform regions
MATCH_ROUTING_REGIONS = ["americas", "asia", "europe", "sea"]

# Mapping from platform regions to routing regions for Match v5
PLATFORM_TO_ROUTING = {
    "na1": "americas", "br1": "americas", "la1": "americas", "la2": "americas",
    "kr": "asia", "jp1": "asia",
    "euw1": "europe", "eun1": "europe", "tr1": "europe", "ru": "europe",
    "oc1": "sea"
}

# You'll need to set your Riot API key as an environment variable
# Get your key from: https://developer.riotgames.com/
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("RIOT_API_KEY")

async def make_riot_request(url: str) -> dict[str, Any] | None:
    """Make a request to the Riot API with proper error handling."""
    logger.info(f"Making Riot API request to: {url}")
    
    if not API_KEY:
        logger.error("RIOT_API_KEY environment variable not set")
        return {"error": "RIOT_API_KEY environment variable not set"}
    
    headers = {
        "User-Agent": USER_AGENT,
        "X-Riot-Token": API_KEY,
        "Accept": "application/json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            data = response.json()
            logger.info(f"Successfully received response from Riot API")
            logger.debug(f"Response data: {data}")
            return data
        except httpx.HTTPStatusError as e:
            error_msg = f"HTTP {e.response.status_code}: {e.response.text}"
            logger.error(f"Riot API HTTP error: {error_msg}")
            return {"error": error_msg}
        except Exception as e:
            error_msg = f"Request failed: {str(e)}"
            logger.error(f"Riot API request failed: {error_msg}")
            return {"error": error_msg}

def format_account(account_data: dict) -> str:
    """Format account data into a readable string."""
    if "error" in account_data:
        return f"Error: {account_data['error']}"
    
    puuid = account_data.get('puuid', 'N/A')
    game_name = account_data.get('gameName', 'N/A')
    tag_line = account_data.get('tagLine', 'N/A')
    
    return f"""
PUUID: {puuid}
Game Name: {game_name}
Tag Line: {tag_line}
Riot ID: {game_name}#{tag_line}
"""

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

def format_active_game(game_data: dict) -> str:
    """Format active game data into a readable string."""
    if "error" in game_data:
        return f"Error: {game_data['error']}"
    
    game_id = game_data.get('gameId', 'N/A')
    game_type = game_data.get('gameType', 'N/A')
    game_mode = game_data.get('gameMode', 'N/A')
    game_length = game_data.get('gameLength', 0)
    map_id = game_data.get('mapId', 'N/A')
    queue_id = game_data.get('gameQueueConfigId', 'N/A')
    
    # Format game length into minutes:seconds
    minutes = game_length // 60
    seconds = game_length % 60
    game_duration = f"{minutes}:{seconds:02d}"
    
    # Format participants
    participants = game_data.get('participants', [])
    team1_players = []
    team2_players = []
    
    for participant in participants:
        player_info = f"Champion ID: {participant.get('championId', 'N/A')}"
        if participant.get('teamId') == 100:
            team1_players.append(player_info)
        else:
            team2_players.append(player_info)
    
    # Format banned champions
    banned_champions = game_data.get('bannedChampions', [])
    team1_bans = []
    team2_bans = []
    
    for ban in banned_champions:
        ban_info = f"Champion ID: {ban.get('championId', 'N/A')}"
        if ban.get('teamId') == 100:
            team1_bans.append(ban_info)
        else:
            team2_bans.append(ban_info)
    
    result = f"""
ACTIVE GAME INFORMATION
=======================
Game ID: {game_id}
Game Type: {game_type}
Game Mode: {game_mode}
Map ID: {map_id}
Queue ID: {queue_id}
Duration: {game_duration}

TEAM 1 (Blue Side):
Players: {len(team1_players)}
{chr(10).join(f"  - {player}" for player in team1_players) if team1_players else "  No players found"}

Bans:
{chr(10).join(f"  - {ban}" for ban in team1_bans) if team1_bans else "  No bans"}

TEAM 2 (Red Side):
Players: {len(team2_players)}
{chr(10).join(f"  - {player}" for player in team2_players) if team2_players else "  No players found"}

Bans:
{chr(10).join(f"  - {ban}" for ban in team2_bans) if team2_bans else "  No bans"}
"""
    return result

def format_featured_games(games_data: dict) -> str:
    """Format featured games data into a readable string."""
    if "error" in games_data:
        return f"Error: {games_data['error']}"
    
    game_list = games_data.get('gameList', [])
    refresh_interval = games_data.get('clientRefreshInterval', 'N/A')
    
    if not game_list:
        return "No featured games currently available."
    
    result = f"""
FEATURED GAMES
==============
Refresh Interval: {refresh_interval} seconds
Total Games: {len(game_list)}

"""
    
    for i, game in enumerate(game_list, 1):
        game_id = game.get('gameId', 'N/A')
        game_mode = game.get('gameMode', 'N/A')
        game_type = game.get('gameType', 'N/A')
        game_length = game.get('gameLength', 0)
        map_id = game.get('mapId', 'N/A')
        queue_id = game.get('gameQueueConfigId', 'N/A')
        
        # Format game length
        minutes = game_length // 60
        seconds = game_length % 60
        game_duration = f"{minutes}:{seconds:02d}"
        
        # Count participants per team
        participants = game.get('participants', [])
        team1_count = sum(1 for p in participants if p.get('teamId') == 100)
        team2_count = sum(1 for p in participants if p.get('teamId') == 200)
        
        result += f"""
Game #{i}:
  Game ID: {game_id}
  Mode: {game_mode}
  Type: {game_type}
  Map ID: {map_id}
  Queue ID: {queue_id}
  Duration: {game_duration}
  Players: {team1_count} vs {team2_count}
"""
    
    return result

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

def format_summoner(summoner_data: dict) -> str:
    """Format summoner data into a readable string."""
    if "error" in summoner_data:
        return f"Error: {summoner_data['error']}"
    
    account_id = summoner_data.get('accountId', 'N/A')
    summoner_id = summoner_data.get('id', 'N/A')
    puuid = summoner_data.get('puuid', 'N/A')
    profile_icon_id = summoner_data.get('profileIconId', 'N/A')
    summoner_level = summoner_data.get('summonerLevel', 'N/A')
    revision_date = summoner_data.get('revisionDate', 0)
    
    # Convert revision date from epoch milliseconds to readable format
    import datetime
    if revision_date and revision_date != 'N/A':
        try:
            revision_datetime = datetime.datetime.fromtimestamp(revision_date / 1000)
            revision_str = revision_datetime.strftime('%Y-%m-%d %H:%M:%S UTC')
        except (ValueError, TypeError):
            revision_str = f"Epoch: {revision_date}"
    else:
        revision_str = "N/A"
    
    return f"""
SUMMONER INFORMATION
====================
Summoner ID: {summoner_id}
Account ID: {account_id}
PUUID: {puuid}
Profile Icon ID: {profile_icon_id}
Summoner Level: {summoner_level}
Last Modified: {revision_str}
"""

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

# Note: The /lol/summoner/v4/summoners/me endpoint requires Bearer token authentication
# which is different from the API key authentication used by other endpoints.
# This would require additional implementation for OAuth2 flow and is not included here.

def format_champion_rotation(rotation_data: dict) -> str:
    """Format champion rotation data into a readable string."""
    if "error" in rotation_data:
        return f"Error: {rotation_data['error']}"
    
    free_champions = rotation_data.get('freeChampionIds', [])
    new_player_champions = rotation_data.get('freeChampionIdsForNewPlayers', [])
    max_new_player_level = rotation_data.get('maxNewPlayerLevel', 'N/A')
    
    result = f"""
CHAMPION ROTATION
=================
Max New Player Level: {max_new_player_level}

Free Champions (All Players): {len(free_champions)} champions
{', '.join(map(str, free_champions)) if free_champions else 'None'}

Free Champions (New Players): {len(new_player_champions)} champions
{', '.join(map(str, new_player_champions)) if new_player_champions else 'None'}
"""
    return result

def format_clash_player(player_data: list) -> str:
    """Format clash player data into a readable string."""
    if not player_data:
        return "No active Clash registrations found for this player."
    
    if isinstance(player_data, dict) and "error" in player_data:
        return f"Error: {player_data['error']}"
    
    result = f"""
CLASH PLAYER REGISTRATIONS
==========================
Active Registrations: {len(player_data)}

"""
    
    for i, registration in enumerate(player_data, 1):
        summoner_id = registration.get('summonerId', 'N/A')
        puuid = registration.get('puuid', 'N/A')
        team_id = registration.get('teamId', 'N/A')
        position = registration.get('position', 'N/A')
        role = registration.get('role', 'N/A')
        
        result += f"""
Registration #{i}:
  Summoner ID: {summoner_id}
  PUUID: {puuid}
  Team ID: {team_id}
  Position: {position}
  Role: {role}
"""
    
    return result

def format_clash_team(team_data: dict) -> str:
    """Format clash team data into a readable string."""
    if "error" in team_data:
        return f"Error: {team_data['error']}"
    
    team_id = team_data.get('id', 'N/A')
    tournament_id = team_data.get('tournamentId', 'N/A')
    name = team_data.get('name', 'N/A')
    icon_id = team_data.get('iconId', 'N/A')
    tier = team_data.get('tier', 'N/A')
    captain = team_data.get('captain', 'N/A')
    abbreviation = team_data.get('abbreviation', 'N/A')
    players = team_data.get('players', [])
    
    result = f"""
CLASH TEAM INFORMATION
======================
Team ID: {team_id}
Tournament ID: {tournament_id}
Name: {name}
Abbreviation: {abbreviation}
Icon ID: {icon_id}
Tier: {tier}
Captain: {captain}

Team Members ({len(players)}):
"""
    
    for i, player in enumerate(players, 1):
        summoner_id = player.get('summonerId', 'N/A')
        position = player.get('position', 'N/A')
        role = player.get('role', 'N/A')
        
        result += f"""
  Player #{i}:
    Summoner ID: {summoner_id}
    Position: {position}
    Role: {role}
"""
    
    return result

def format_clash_tournaments(tournaments_data: list) -> str:
    """Format clash tournaments data into a readable string."""
    if not tournaments_data:
        return "No active or upcoming tournaments found."
    
    if isinstance(tournaments_data, dict) and "error" in tournaments_data:
        return f"Error: {tournaments_data['error']}"
    
    result = f"""
CLASH TOURNAMENTS
=================
Active/Upcoming Tournaments: {len(tournaments_data)}

"""
    
    import datetime
    
    for i, tournament in enumerate(tournaments_data, 1):
        tournament_id = tournament.get('id', 'N/A')
        theme_id = tournament.get('themeId', 'N/A')
        name_key = tournament.get('nameKey', 'N/A')
        name_key_secondary = tournament.get('nameKeySecondary', 'N/A')
        schedule = tournament.get('schedule', [])
        
        result += f"""
Tournament #{i}:
  ID: {tournament_id}
  Theme ID: {theme_id}
  Name Key: {name_key}
  Secondary Name Key: {name_key_secondary}
  Phases: {len(schedule)}
"""
        
        for j, phase in enumerate(schedule, 1):
            phase_id = phase.get('id', 'N/A')
            registration_time = phase.get('registrationTime', 0)
            start_time = phase.get('startTime', 0)
            cancelled = phase.get('cancelled', False)
            
            # Convert timestamps
            try:
                reg_time = datetime.datetime.fromtimestamp(registration_time / 1000).strftime('%Y-%m-%d %H:%M:%S UTC') if registration_time else 'N/A'
                start_time_str = datetime.datetime.fromtimestamp(start_time / 1000).strftime('%Y-%m-%d %H:%M:%S UTC') if start_time else 'N/A'
            except (ValueError, TypeError):
                reg_time = f"Epoch: {registration_time}"
                start_time_str = f"Epoch: {start_time}"
            
            status = "CANCELLED" if cancelled else "ACTIVE"
            
            result += f"""
    Phase #{j}:
      ID: {phase_id}
      Registration: {reg_time}
      Start Time: {start_time_str}
      Status: {status}
"""
    
    return result

def format_clash_tournament(tournament_data: dict) -> str:
    """Format single clash tournament data into a readable string."""
    if "error" in tournament_data:
        return f"Error: {tournament_data['error']}"
    
    tournament_id = tournament_data.get('id', 'N/A')
    theme_id = tournament_data.get('themeId', 'N/A')
    name_key = tournament_data.get('nameKey', 'N/A')
    name_key_secondary = tournament_data.get('nameKeySecondary', 'N/A')
    schedule = tournament_data.get('schedule', [])
    
    result = f"""
CLASH TOURNAMENT DETAILS
========================
Tournament ID: {tournament_id}
Theme ID: {theme_id}
Name Key: {name_key}
Secondary Name Key: {name_key_secondary}
Total Phases: {len(schedule)}

TOURNAMENT SCHEDULE:
"""
    
    import datetime
    
    for i, phase in enumerate(schedule, 1):
        phase_id = phase.get('id', 'N/A')
        registration_time = phase.get('registrationTime', 0)
        start_time = phase.get('startTime', 0)
        cancelled = phase.get('cancelled', False)
        
        # Convert timestamps
        try:
            reg_time = datetime.datetime.fromtimestamp(registration_time / 1000).strftime('%Y-%m-%d %H:%M:%S UTC') if registration_time else 'N/A'
            start_time_str = datetime.datetime.fromtimestamp(start_time / 1000).strftime('%Y-%m-%d %H:%M:%S UTC') if start_time else 'N/A'
        except (ValueError, TypeError):
            reg_time = f"Epoch: {registration_time}"
            start_time_str = f"Epoch: {start_time}"
        
        status = "CANCELLED" if cancelled else "ACTIVE"
        
        result += f"""
Phase #{i}:
  Phase ID: {phase_id}
  Registration Opens: {reg_time}
  Tournament Start: {start_time_str}
  Status: {status}
"""
    
    return result

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

def format_league_list(league_data: dict) -> str:
    """Format league list data (challenger/grandmaster/master/league by ID) into a readable string."""
    if "error" in league_data:
        return f"Error: {league_data['error']}"
    
    league_id = league_data.get('leagueId', 'N/A')
    tier = league_data.get('tier', 'N/A')
    name = league_data.get('name', 'N/A')
    queue = league_data.get('queue', 'N/A')
    entries = league_data.get('entries', [])
    
    result = f"""
{tier.upper()} LEAGUE
{'=' * (len(tier) + 7)}
League ID: {league_id}
Name: {name}
Queue: {queue}
Total Players: {len(entries)}

TOP PLAYERS:
"""
    
    # Sort entries by league points descending and show top 10
    sorted_entries = sorted(entries, key=lambda x: x.get('leaguePoints', 0), reverse=True)
    
    for i, entry in enumerate(sorted_entries[:10], 1):
        summoner_id = entry.get('summonerId', 'N/A')
        puuid = entry.get('puuid', 'N/A')[:8] + '...' if entry.get('puuid') else 'N/A'
        rank = entry.get('rank', 'N/A')
        lp = entry.get('leaguePoints', 0)
        wins = entry.get('wins', 0)
        losses = entry.get('losses', 0)
        hot_streak = entry.get('hotStreak', False)
        veteran = entry.get('veteran', False)
        fresh_blood = entry.get('freshBlood', False)
        
        winrate = (wins / (wins + losses) * 100) if (wins + losses) > 0 else 0
        
        flags = []
        if hot_streak:
            flags.append("🔥HOT")
        if veteran:
            flags.append("⭐VET")
        if fresh_blood:
            flags.append("🆕NEW")
        
        flag_str = " " + " ".join(flags) if flags else ""
        
        result += f"""
#{i:2d}. {rank} {lp} LP - {wins}W/{losses}L ({winrate:.1f}%){flag_str}
     Summoner: {summoner_id[:20]}...
     PUUID: {puuid}
"""
    
    return result

def format_league_entries(entries_data: list) -> str:
    """Format league entries data into a readable string."""
    if not entries_data:
        return "No ranked entries found for this player."
    
    if isinstance(entries_data, dict) and "error" in entries_data:
        return f"Error: {entries_data['error']}"
    
    result = f"""
RANKED LEAGUE ENTRIES
=====================
Total Queues: {len(entries_data)}

"""
    
    for i, entry in enumerate(entries_data, 1):
        league_id = entry.get('leagueId', 'N/A')
        summoner_id = entry.get('summonerId', 'N/A')
        puuid = entry.get('puuid', 'N/A')[:8] + '...' if entry.get('puuid') else 'N/A'
        queue_type = entry.get('queueType', 'N/A')
        tier = entry.get('tier', 'N/A')
        rank = entry.get('rank', 'N/A')
        lp = entry.get('leaguePoints', 0)
        wins = entry.get('wins', 0)
        losses = entry.get('losses', 0)
        hot_streak = entry.get('hotStreak', False)
        veteran = entry.get('veteran', False)
        fresh_blood = entry.get('freshBlood', False)
        inactive = entry.get('inactive', False)
        
        winrate = (wins / (wins + losses) * 100) if (wins + losses) > 0 else 0
        
        # Handle mini series
        mini_series = entry.get('miniSeries')
        series_info = ""
        if mini_series:
            target = mini_series.get('target', 0)
            progress = mini_series.get('progress', '')
            series_wins = mini_series.get('wins', 0)
            series_losses = mini_series.get('losses', 0)
            series_info = f"\n  Promotion Series: {progress} (Bo{target}) - {series_wins}W/{series_losses}L"
        
        flags = []
        if hot_streak:
            flags.append("🔥HOT STREAK")
        if veteran:
            flags.append("⭐VETERAN")
        if fresh_blood:
            flags.append("🆕FRESH BLOOD")
        if inactive:
            flags.append("😴INACTIVE")
        
        flag_str = f"\n  Status: {' | '.join(flags)}" if flags else ""
        
        result += f"""
Queue #{i}: {queue_type}
  Rank: {tier} {rank} ({lp} LP)
  Record: {wins}W/{losses}L ({winrate:.1f}% WR)
  League ID: {league_id}
  Summoner: {summoner_id[:30]}...
  PUUID: {puuid}{series_info}{flag_str}

"""
    
    return result

def format_challenge_configs(configs_data: list) -> str:
    """Format challenge configs data into a readable string."""
    if not configs_data:
        return "No challenge configurations found."
    
    if isinstance(configs_data, dict) and "error" in configs_data:
        return f"Error: {configs_data['error']}"
    
    result = f"""
CHALLENGE CONFIGURATIONS
========================
Total Challenges: {len(configs_data)}

"""
    
    # Group by state
    enabled = [c for c in configs_data if c.get('state') == 'ENABLED']
    hidden = [c for c in configs_data if c.get('state') == 'HIDDEN']
    disabled = [c for c in configs_data if c.get('state') == 'DISABLED']
    archived = [c for c in configs_data if c.get('state') == 'ARCHIVED']
    
    result += f"""
ENABLED: {len(enabled)} challenges
HIDDEN: {len(hidden)} challenges  
DISABLED: {len(disabled)} challenges
ARCHIVED: {len(archived)} challenges

SAMPLE ENABLED CHALLENGES:
"""
    
    for i, challenge in enumerate(enabled[:10], 1):
        challenge_id = challenge.get('id', 'N/A')
        localized_names = challenge.get('localizedNames', {})
        name = localized_names.get('en_US', {}).get('name', f'Challenge {challenge_id}')
        tracking = challenge.get('tracking', 'N/A')
        leaderboard = challenge.get('leaderboard', False)
        
        result += f"""
{i:2d}. {name} (ID: {challenge_id})
    Tracking: {tracking}
    Leaderboard: {'Yes' if leaderboard else 'No'}
"""
    
    return result

def format_challenge_config(config_data: dict) -> str:
    """Format single challenge config data into a readable string."""
    if "error" in config_data:
        return f"Error: {config_data['error']}"
    
    challenge_id = config_data.get('id', 'N/A')
    localized_names = config_data.get('localizedNames', {})
    en_names = localized_names.get('en_US', {})
    name = en_names.get('name', f'Challenge {challenge_id}')
    description = en_names.get('description', 'No description available')
    
    state = config_data.get('state', 'N/A')
    tracking = config_data.get('tracking', 'N/A')
    start_timestamp = config_data.get('startTimestamp', 0)
    end_timestamp = config_data.get('endTimestamp', 0)
    leaderboard = config_data.get('leaderboard', False)
    thresholds = config_data.get('thresholds', {})
    
    import datetime
    
    # Convert timestamps
    try:
        start_time = datetime.datetime.fromtimestamp(start_timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S UTC') if start_timestamp else 'N/A'
        end_time = datetime.datetime.fromtimestamp(end_timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S UTC') if end_timestamp else 'N/A'
    except (ValueError, TypeError):
        start_time = f"Epoch: {start_timestamp}"
        end_time = f"Epoch: {end_timestamp}"
    
    result = f"""
CHALLENGE DETAILS
=================
Name: {name}
ID: {challenge_id}
Description: {description}

Status: {state}
Tracking: {tracking}
Leaderboard: {'Enabled' if leaderboard else 'Disabled'}
Start Time: {start_time}
End Time: {end_time}

THRESHOLDS:
"""
    
    for level, threshold in thresholds.items():
        result += f"  {level.upper()}: {threshold}\n"
    
    return result

def format_challenge_leaderboard(leaderboard_data: list, level: str) -> str:
    """Format challenge leaderboard data into a readable string."""
    if not leaderboard_data:
        return f"No {level} players found for this challenge."
    
    if isinstance(leaderboard_data, dict) and "error" in leaderboard_data:
        return f"Error: {leaderboard_data['error']}"
    
    result = f"""
{level.upper()} CHALLENGE LEADERBOARD
{'=' * (len(level) + 21)}
Total Players: {len(leaderboard_data)}

TOP PLAYERS:
"""
    
    for i, player in enumerate(leaderboard_data[:25], 1):
        puuid = player.get('puuid', 'N/A')[:8] + '...' if player.get('puuid') else 'N/A'
        value = player.get('value', 0)
        position = player.get('position', i)
        
        result += f"""
#{position:3d}. Score: {value:,.0f}
      PUUID: {puuid}
"""
    
    return result

def format_player_challenges(player_data: dict) -> str:
    """Format player challenge data into a readable string."""
    if "error" in player_data:
        return f"Error: {player_data['error']}"
    
    challenges = player_data.get('challenges', [])
    total_points = player_data.get('totalPoints', {})
    category_points = player_data.get('categoryPoints', {})
    
    current_points = total_points.get('current', 0)
    level = total_points.get('level', 'NONE')
    percentile = total_points.get('percentile', 0)
    
    result = f"""
PLAYER CHALLENGE SUMMARY
========================
Total Points: {current_points:,}
Overall Level: {level}
Percentile: {percentile:.2f}%
Active Challenges: {len(challenges)}

CATEGORY BREAKDOWN:
"""
    
    for category, points in category_points.items():
        cat_current = points.get('current', 0)
        cat_level = points.get('level', 'NONE')
        cat_percentile = points.get('percentile', 0)
        
        result += f"""
  {category.upper()}:
    Points: {cat_current:,}
    Level: {cat_level}
    Percentile: {cat_percentile:.2f}%
"""
    
    # Show top challenges by points
    sorted_challenges = sorted(challenges, key=lambda x: x.get('value', 0), reverse=True)
    
    result += f"""

TOP CHALLENGES BY PROGRESS:
"""
    
    for i, challenge in enumerate(sorted_challenges[:10], 1):
        challenge_id = challenge.get('challengeId', 'N/A')
        percentile = challenge.get('percentile', 0)
        level = challenge.get('level', 'NONE')
        value = challenge.get('value', 0)
        achieved_time = challenge.get('achievedTime', 0)
        
        # Convert timestamp
        import datetime
        try:
            achieved = datetime.datetime.fromtimestamp(achieved_time / 1000).strftime('%Y-%m-%d') if achieved_time else 'In Progress'
        except (ValueError, TypeError):
            achieved = 'In Progress'
        
        result += f"""
{i:2d}. Challenge {challenge_id}: {level}
    Progress: {value:,.0f} (Top {percentile:.1f}%)
    Achieved: {achieved}
"""
    
    return result

def format_platform_status(status_data: dict) -> str:
    """Format platform status data into a readable string."""
    if "error" in status_data:
        return f"Error: {status_data['error']}"
    
    platform_id = status_data.get('id', 'N/A')
    name = status_data.get('name', 'N/A')
    locales = status_data.get('locales', [])
    maintenances = status_data.get('maintenances', [])
    incidents = status_data.get('incidents', [])
    
    result = f"""
PLATFORM STATUS
===============
Platform: {name} ({platform_id})
Supported Locales: {', '.join(locales)}

Current Status: {'🟢 OPERATIONAL' if not maintenances and not incidents else '🟡 ISSUES DETECTED'}

"""
    
    if maintenances:
        result += f"""
ACTIVE MAINTENANCES ({len(maintenances)}):
"""
        for i, maintenance in enumerate(maintenances, 1):
            status_id = maintenance.get('id', 'N/A')
            maintenance_status = maintenance.get('maintenance_status', 'N/A')
            titles = maintenance.get('titles', [])
            platforms = maintenance.get('platforms', [])
            created_at = maintenance.get('created_at', 'N/A')
            
            title = next((t.get('content', 'No title') for t in titles if t.get('locale') == 'en_US'), 'No title')
            
            result += f"""
{i}. {title}
   Status: {maintenance_status.upper()}
   Platforms: {', '.join(platforms)}
   Created: {created_at}
"""
    
    if incidents:
        result += f"""
ACTIVE INCIDENTS ({len(incidents)}):
"""
        for i, incident in enumerate(incidents, 1):
            status_id = incident.get('id', 'N/A')
            severity = incident.get('incident_severity', 'N/A')
            titles = incident.get('titles', [])
            platforms = incident.get('platforms', [])
            created_at = incident.get('created_at', 'N/A')
            
            title = next((t.get('content', 'No title') for t in titles if t.get('locale') == 'en_US'), 'No title')
            
            severity_icon = {'info': '🔵', 'warning': '🟡', 'critical': '🔴'}.get(severity, '⚪')
            
            result += f"""
{i}. {severity_icon} {title}
   Severity: {severity.upper()}
   Platforms: {', '.join(platforms)}
   Created: {created_at}
"""
    
    if not maintenances and not incidents:
        result += "✅ No active maintenances or incidents\n"
    
    return result

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

def get_routing_region(platform_region: str) -> str:
    """Convert platform region to routing region for Match v5 API."""
    return PLATFORM_TO_ROUTING.get(platform_region, "americas")

def format_match_ids(match_ids: list, puuid: str) -> str:
    """Format match IDs list into a readable string."""
    if not match_ids:
        return f"No matches found for PUUID: {puuid[:8]}..."
    
    if isinstance(match_ids, dict) and "error" in match_ids:
        return f"Error: {match_ids['error']}"
    
    result = f"""
MATCH HISTORY
=============
PUUID: {puuid[:8]}...
Total Matches: {len(match_ids)}

RECENT MATCH IDs:
"""
    
    for i, match_id in enumerate(match_ids[:10], 1):
        result += f"{i:2d}. {match_id}\n"
    
    if len(match_ids) > 10:
        result += f"\n... and {len(match_ids) - 10} more matches"
    
    return result

def format_match_detail(match_data: dict) -> str:
    """Format detailed match data into a readable string."""
    if "error" in match_data:
        return f"Error: {match_data['error']}"
    
    metadata = match_data.get('metadata', {})
    info = match_data.get('info', {})
    
    match_id = metadata.get('matchId', 'N/A')
    participants_puuids = metadata.get('participants', [])
    
    # Game info
    game_creation = info.get('gameCreation', 0)
    game_duration = info.get('gameDuration', 0)
    game_end = info.get('gameEndTimestamp', 0)
    game_mode = info.get('gameMode', 'N/A')
    game_type = info.get('gameType', 'N/A')
    game_version = info.get('gameVersion', 'N/A')
    map_id = info.get('mapId', 'N/A')
    queue_id = info.get('queueId', 'N/A')
    platform_id = info.get('platformId', 'N/A')
    
    # Convert timestamps
    import datetime
    try:
        created_time = datetime.datetime.fromtimestamp(game_creation / 1000).strftime('%Y-%m-%d %H:%M:%S UTC') if game_creation else 'N/A'
        # Handle duration format change in patch 11.20
        if game_end:
            duration_str = f"{game_duration // 60}:{game_duration % 60:02d}"
        else:
            duration_str = f"{game_duration // 60000}:{(game_duration % 60000) // 1000:02d}"
    except (ValueError, TypeError):
        created_time = f"Epoch: {game_creation}"
        duration_str = f"{game_duration}s"
    
    participants = info.get('participants', [])
    teams = info.get('teams', [])
    
    # Determine winning team
    winning_team = next((team['teamId'] for team in teams if team.get('win')), None)
    
    result = f"""
MATCH DETAILS
=============
Match ID: {match_id}
Platform: {platform_id}
Game Mode: {game_mode}
Game Type: {game_type}
Queue ID: {queue_id}
Map ID: {map_id}
Version: {game_version}
Created: {created_time}
Duration: {duration_str}
Participants: {len(participants)}

TEAM RESULTS:
"""
    
    # Group participants by team
    team_100 = [p for p in participants if p.get('teamId') == 100]
    team_200 = [p for p in participants if p.get('teamId') == 200]
    
    result += f"""
TEAM 1 (Blue Side): {'🏆 VICTORY' if winning_team == 100 else '💀 DEFEAT'}
"""
    
    for i, participant in enumerate(team_100, 1):
        champion = participant.get('championName', 'Unknown')
        riot_id = f"{participant.get('riotIdGameName', 'N/A')}#{participant.get('riotIdTagline', 'N/A')}"
        kda = f"{participant.get('kills', 0)}/{participant.get('deaths', 0)}/{participant.get('assists', 0)}"
        cs = participant.get('totalMinionsKilled', 0) + participant.get('neutralMinionsKilled', 0)
        gold = participant.get('goldEarned', 0)
        damage = participant.get('totalDamageDealtToChampions', 0)
        position = participant.get('teamPosition', 'N/A')
        
        result += f"""
  {i}. {champion} ({position}) - {riot_id}
     KDA: {kda} | CS: {cs} | Gold: {gold:,} | Damage: {damage:,}
"""
    
    result += f"""
TEAM 2 (Red Side): {'🏆 VICTORY' if winning_team == 200 else '💀 DEFEAT'}
"""
    
    for i, participant in enumerate(team_200, 1):
        champion = participant.get('championName', 'Unknown')
        riot_id = f"{participant.get('riotIdGameName', 'N/A')}#{participant.get('riotIdTagline', 'N/A')}"
        kda = f"{participant.get('kills', 0)}/{participant.get('deaths', 0)}/{participant.get('assists', 0)}"
        cs = participant.get('totalMinionsKilled', 0) + participant.get('neutralMinionsKilled', 0)
        gold = participant.get('goldEarned', 0)
        damage = participant.get('totalDamageDealtToChampions', 0)
        position = participant.get('teamPosition', 'N/A')
        
        result += f"""
  {i}. {champion} ({position}) - {riot_id}
     KDA: {kda} | CS: {cs} | Gold: {gold:,} | Damage: {damage:,}
"""
    
    # Team objectives
    result += f"""
OBJECTIVES:
"""
    
    for team in teams:
        team_id = team.get('teamId', 'N/A')
        objectives = team.get('objectives', {})
        team_name = "Blue Side" if team_id == 100 else "Red Side"
        
        baron_kills = objectives.get('baron', {}).get('kills', 0)
        dragon_kills = objectives.get('dragon', {}).get('kills', 0)
        tower_kills = objectives.get('tower', {}).get('kills', 0)
        inhibitor_kills = objectives.get('inhibitor', {}).get('kills', 0)
        rift_herald_kills = objectives.get('riftHerald', {}).get('kills', 0)
        
        result += f"""
{team_name}: Baron {baron_kills} | Dragons {dragon_kills} | Towers {tower_kills} | Inhibitors {inhibitor_kills} | Rift Herald {rift_herald_kills}
"""
    
    return result

def format_match_timeline(timeline_data: dict) -> str:
    """Format match timeline data into a readable string."""
    if "error" in timeline_data:
        return f"Error: {timeline_data['error']}"
    
    metadata = timeline_data.get('metadata', {})
    info = timeline_data.get('info', {})
    
    match_id = metadata.get('matchId', 'N/A')
    frame_interval = info.get('frameInterval', 60000)  # Usually 60 seconds
    frames = info.get('frames', [])
    
    result = f"""
MATCH TIMELINE
==============
Match ID: {match_id}
Frame Interval: {frame_interval / 1000}s
Total Frames: {len(frames)}

KEY EVENTS:
"""
    
    # Collect important events
    important_events = []
    
    for frame in frames:
        timestamp = frame.get('timestamp', 0)
        events = frame.get('events', [])
        
        for event in events:
            event_type = event.get('type', '')
            
            # Filter for important events
            if event_type in ['CHAMPION_KILL', 'ELITE_MONSTER_KILL', 'BUILDING_KILL', 'CHAMPION_SPECIAL_KILL']:
                important_events.append({
                    'timestamp': timestamp,
                    'type': event_type,
                    'data': event
                })
    
    # Sort by timestamp and show first 20 events
    important_events.sort(key=lambda x: x['timestamp'])
    
    for i, event in enumerate(important_events[:20], 1):
        timestamp = event['timestamp']
        minutes = timestamp // 60000
        seconds = (timestamp % 60000) // 1000
        time_str = f"{minutes:02d}:{seconds:02d}"
        
        event_type = event['type']
        event_data = event['data']
        
        if event_type == 'CHAMPION_KILL':
            killer_id = event_data.get('killerId', 0)
            victim_id = event_data.get('victimId', 0)
            assist_ids = event_data.get('assistingParticipantIds', [])
            
            result += f"{time_str} - Champion Kill: P{killer_id} killed P{victim_id}"
            if assist_ids:
                result += f" (Assists: {', '.join(f'P{aid}' for aid in assist_ids)})"
            result += "\n"
            
        elif event_type == 'ELITE_MONSTER_KILL':
            killer_id = event_data.get('killerId', 0)
            monster_type = event_data.get('monsterType', 'Unknown')
            
            result += f"{time_str} - Elite Monster Kill: P{killer_id} killed {monster_type}\n"
            
        elif event_type == 'BUILDING_KILL':
            killer_id = event_data.get('killerId', 0)
            building_type = event_data.get('buildingType', 'Unknown')
            lane_type = event_data.get('laneType', '')
            
            result += f"{time_str} - Building Kill: P{killer_id} destroyed {building_type}"
            if lane_type:
                result += f" in {lane_type}"
            result += "\n"
    
    if len(important_events) > 20:
        result += f"\n... and {len(important_events) - 20} more events"
    
    return result

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

if __name__ == "__main__":
    logger.info("Starting League MCP Server...")
    # Initialize and run the server
    mcp.run(transport='stdio')