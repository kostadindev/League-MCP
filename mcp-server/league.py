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

if __name__ == "__main__":
    logger.info("Starting League MCP Server...")
    # Initialize and run the server
    mcp.run(transport='stdio')