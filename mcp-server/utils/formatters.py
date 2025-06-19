"""Formatters for various Riot API responses."""

import datetime
from typing import Dict, List, Any


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