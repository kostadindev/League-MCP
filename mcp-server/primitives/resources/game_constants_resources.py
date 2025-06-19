"""Game constants resources for League of Legends."""

import logging
from mcp.server.fastmcp import FastMCP

logger = logging.getLogger(__name__)

# Game constants from the official documentation
QUEUE_TYPES = [
    {"queueId": 0, "map": "Custom games", "description": None, "notes": None},
    {"queueId": 2, "map": "Summoner's Rift", "description": "5v5 Blind Pick games", "notes": "Deprecated in patch 7.19 in favor of queueId 430"},
    {"queueId": 4, "map": "Summoner's Rift", "description": "5v5 Ranked Solo games", "notes": "Deprecated in favor of queueId 420"},
    {"queueId": 6, "map": "Summoner's Rift", "description": "5v5 Ranked Premade games", "notes": "Game mode deprecated"},
    {"queueId": 7, "map": "Summoner's Rift", "description": "Co-op vs AI games", "notes": None},
    {"queueId": 8, "map": "Twisted Treeline", "description": "3v3 Normal games", "notes": "Deprecated in patch 9.23"},
    {"queueId": 9, "map": "Twisted Treeline", "description": "3v3 Ranked Flex games", "notes": "Deprecated in patch 9.23"},
    {"queueId": 14, "map": "Summoner's Rift", "description": "5v5 Draft Pick games", "notes": None},
    {"queueId": 16, "map": "Crystal Scar", "description": "5v5 Dominion Blind Pick games", "notes": "Game mode deprecated"},
    {"queueId": 17, "map": "Crystal Scar", "description": "5v5 Dominion Draft Pick games", "notes": "Game mode deprecated"},
    {"queueId": 25, "map": "Crystal Scar", "description": "Dominion Co-op vs AI games", "notes": "Game mode deprecated"},
    {"queueId": 31, "map": "Summoner's Rift", "description": "Co-op vs AI Intro Bot games", "notes": None},
    {"queueId": 32, "map": "Summoner's Rift", "description": "Co-op vs AI Beginner Bot games", "notes": None},
    {"queueId": 33, "map": "Summoner's Rift", "description": "Co-op vs AI Intermediate Bot games", "notes": None},
    {"queueId": 34, "map": "Twisted Treeline", "description": "3v3 Ranked Team games", "notes": "Game mode deprecated"},
    {"queueId": 35, "map": "Summoner's Rift", "description": "5v5 Ranked Team games", "notes": "Game mode deprecated"},
    {"queueId": 36, "map": "Summoner's Rift", "description": "Co-op vs AI games", "notes": None},
    {"queueId": 37, "map": "Summoner's Rift", "description": "5v5 Ranked Team games", "notes": "Game mode deprecated"},
    {"queueId": 41, "map": "Twisted Treeline", "description": "3v3 Ranked Team games", "notes": "Game mode deprecated"},
    {"queueId": 42, "map": "Summoner's Rift", "description": "5v5 Ranked Team games", "notes": "Game mode deprecated"},
    {"queueId": 52, "map": "Twisted Treeline", "description": "3v3 Co-op vs AI games", "notes": "Deprecated in patch 9.23"},
    {"queueId": 61, "map": "Summoner's Rift", "description": "5v5 Team Builder games", "notes": "Game mode deprecated"},
    {"queueId": 65, "map": "Howling Abyss", "description": "5v5 ARAM games", "notes": None},
    {"queueId": 67, "map": "Howling Abyss", "description": "ARAM Co-op vs AI games", "notes": None},
    {"queueId": 70, "map": "Summoner's Rift", "description": "One for All games", "notes": None},
    {"queueId": 72, "map": "Howling Abyss", "description": "1v1 Snowdown Showdown games", "notes": None},
    {"queueId": 73, "map": "Howling Abyss", "description": "2v2 Snowdown Showdown games", "notes": None},
    {"queueId": 75, "map": "Summoner's Rift", "description": "6v6 Hexakill games", "notes": None},
    {"queueId": 76, "map": "Summoner's Rift", "description": "Ultra Rapid Fire games", "notes": None},
    {"queueId": 78, "map": "Howling Abyss", "description": "One For All: Mirror Mode games", "notes": None},
    {"queueId": 83, "map": "Summoner's Rift", "description": "Co-op vs AI Ultra Rapid Fire games", "notes": None},
    {"queueId": 84, "map": "Summoner's Rift", "description": "Doom Bots Rank 1 games", "notes": None},
    {"queueId": 85, "map": "Summoner's Rift", "description": "Doom Bots Rank 2 games", "notes": None},
    {"queueId": 86, "map": "Summoner's Rift", "description": "Doom Bots Rank 5 games", "notes": None},
    {"queueId": 91, "map": "Summoner's Rift", "description": "Doom Bots games", "notes": None},
    {"queueId": 92, "map": "Summoner's Rift", "description": "Ascension games", "notes": None},
    {"queueId": 93, "map": "Twisted Treeline", "description": "6v6 Hexakill games", "notes": None},
    {"queueId": 96, "map": "Crystal Scar", "description": "Ascension games", "notes": None},
    {"queueId": 98, "map": "Twisted Treeline", "description": "6v6 Hexakill games", "notes": None},
    {"queueId": 100, "map": "Butcher's Bridge", "description": "5v5 ARAM games", "notes": None},
    {"queueId": 300, "map": "Howling Abyss", "description": "Legend of the Poro King games", "notes": None},
    {"queueId": 310, "map": "Summoner's Rift", "description": "Nemesis games", "notes": None},
    {"queueId": 313, "map": "Summoner's Rift", "description": "Black Market Brawlers games", "notes": None},
    {"queueId": 315, "map": "Summoner's Rift", "description": "Nexus Siege games", "notes": None},
    {"queueId": 317, "map": "Crystal Scar", "description": "Definitely Not Dominion games", "notes": None},
    {"queueId": 318, "map": "Summoner's Rift", "description": "ARURF games", "notes": None},
    {"queueId": 325, "map": "Summoner's Rift", "description": "All Random games", "notes": None},
    {"queueId": 400, "map": "Summoner's Rift", "description": "5v5 Draft Pick games", "notes": None},
    {"queueId": 420, "map": "Summoner's Rift", "description": "5v5 Ranked Solo games", "notes": None},
    {"queueId": 430, "map": "Summoner's Rift", "description": "5v5 Blind Pick games", "notes": None},
    {"queueId": 440, "map": "Summoner's Rift", "description": "5v5 Ranked Flex games", "notes": None},
    {"queueId": 450, "map": "Howling Abyss", "description": "5v5 ARAM games", "notes": None},
    {"queueId": 460, "map": "Twisted Treeline", "description": "3v3 Blind Pick games", "notes": "Deprecated in patch 9.23"},
    {"queueId": 470, "map": "Twisted Treeline", "description": "3v3 Ranked Flex games", "notes": "Deprecated in patch 9.23"},
    {"queueId": 600, "map": "Summoner's Rift", "description": "Blood Hunt Assassin games", "notes": None},
    {"queueId": 610, "map": "Cosmic Ruins", "description": "Dark Star: Singularity games", "notes": None},
    {"queueId": 700, "map": "Summoner's Rift", "description": "Clash games", "notes": None},
    {"queueId": 720, "map": "Howling Abyss", "description": "ARAM Clash games", "notes": None},
    {"queueId": 800, "map": "Twisted Treeline", "description": "Co-op vs. AI Intermediate Bot games", "notes": "Deprecated in patch 9.23"},
    {"queueId": 810, "map": "Twisted Treeline", "description": "Co-op vs. AI Intro Bot games", "notes": "Deprecated in patch 9.23"},
    {"queueId": 820, "map": "Twisted Treeline", "description": "Co-op vs. AI Beginner Bot games", "notes": "Deprecated in patch 9.23"},
    {"queueId": 830, "map": "Summoner's Rift", "description": "Co-op vs. AI Intro Bot games", "notes": None},
    {"queueId": 840, "map": "Summoner's Rift", "description": "Co-op vs. AI Beginner Bot games", "notes": None},
    {"queueId": 850, "map": "Summoner's Rift", "description": "Co-op vs. AI Intermediate Bot games", "notes": None},
    {"queueId": 900, "map": "Summoner's Rift", "description": "ARURF games", "notes": "Pick URF games (queueId 1900) were split from ARURF in early 2022"},
    {"queueId": 910, "map": "Crystal Scar", "description": "Ascension games", "notes": None},
    {"queueId": 920, "map": "Howling Abyss", "description": "Legend of the Poro King games", "notes": None},
    {"queueId": 940, "map": "Summoner's Rift", "description": "Nexus Siege games", "notes": None},
    {"queueId": 950, "map": "Summoner's Rift", "description": "Doom Bots Voting games", "notes": None},
    {"queueId": 960, "map": "Summoner's Rift", "description": "Doom Bots Standard games", "notes": None},
    {"queueId": 980, "map": "Valoran City Park", "description": "Star Guardian Invasion: Normal games", "notes": None},
    {"queueId": 990, "map": "Valoran City Park", "description": "Star Guardian Invasion: Onslaught games", "notes": None},
    {"queueId": 1000, "map": "Overcharge", "description": "PROJECT: Hunters games", "notes": None},
    {"queueId": 1010, "map": "Summoner's Rift", "description": "Snow ARURF games", "notes": None},
    {"queueId": 1020, "map": "Summoner's Rift", "description": "One for All games", "notes": None},
    {"queueId": 1030, "map": "Crash Site", "description": "Odyssey Extraction: Intro games", "notes": None},
    {"queueId": 1040, "map": "Crash Site", "description": "Odyssey Extraction: Cadet games", "notes": None},
    {"queueId": 1050, "map": "Crash Site", "description": "Odyssey Extraction: Crewmember games", "notes": None},
    {"queueId": 1060, "map": "Crash Site", "description": "Odyssey Extraction: Captain games", "notes": None},
    {"queueId": 1070, "map": "Crash Site", "description": "Odyssey Extraction: Onslaught games", "notes": None},
    {"queueId": 1090, "map": "Convergence", "description": "Teamfight Tactics games", "notes": None},
    {"queueId": 1100, "map": "Convergence", "description": "Ranked Teamfight Tactics games", "notes": None},
    {"queueId": 1110, "map": "Convergence", "description": "Teamfight Tactics Tutorial games", "notes": None},
    {"queueId": 1111, "map": "Convergence", "description": "Teamfight Tactics test games", "notes": None},
    {"queueId": 1200, "map": "Nexus Blitz", "description": "Nexus Blitz games", "notes": None},
    {"queueId": 1300, "map": "Nexus Blitz", "description": "Nexus Blitz games", "notes": None},
    {"queueId": 1400, "map": "Summoner's Rift", "description": "Ultimate Spellbook games", "notes": None},
    {"queueId": 1900, "map": "Summoner's Rift", "description": "Pick URF games", "notes": "Introduced in early 2022 as a split from ARURF"},
    {"queueId": 2000, "map": "Summoner's Rift", "description": "Tutorial 1", "notes": None},
    {"queueId": 2010, "map": "Summoner's Rift", "description": "Tutorial 2", "notes": None},
    {"queueId": 2020, "map": "Summoner's Rift", "description": "Tutorial 3", "notes": None}
]

MAPS = [
    {"mapId": 1, "mapName": "Summoner's Rift", "notes": "Original Summer variant"},
    {"mapId": 2, "mapName": "Summoner's Rift", "notes": "Original Autumn variant"},
    {"mapId": 3, "mapName": "The Proving Grounds", "notes": "Tutorial Map"},
    {"mapId": 4, "mapName": "Twisted Treeline", "notes": "Original Version"},
    {"mapId": 8, "mapName": "The Crystal Scar", "notes": "Dominion map"},
    {"mapId": 10, "mapName": "Twisted Treeline", "notes": "Current Version"},
    {"mapId": 11, "mapName": "Summoner's Rift", "notes": "Current Version"},
    {"mapId": 12, "mapName": "Howling Abyss", "notes": "ARAM map"},
    {"mapId": 14, "mapName": "Butcher's Bridge", "notes": "Alternate ARAM map"},
    {"mapId": 16, "mapName": "Cosmic Ruins", "notes": "Dark Star: Singularity map"},
    {"mapId": 18, "mapName": "Valoran City Park", "notes": "Star Guardian Invasion map"},
    {"mapId": 19, "mapName": "Substructure 43", "notes": "PROJECT: Hunters map"},
    {"mapId": 20, "mapName": "Crash Site", "notes": "Odyssey: Extraction map"},
    {"mapId": 21, "mapName": "Nexus Blitz", "notes": "Nexus Blitz map"},
    {"mapId": 22, "mapName": "Convergence", "notes": "Teamfight Tactics map"},
    {"mapId": 30, "mapName": "Rings of Wrath", "notes": "Arena map"}
]

GAME_MODES = [
    {"gameMode": "CLASSIC", "description": "Classic Summoner's Rift and Twisted Treeline games"},
    {"gameMode": "ODIN", "description": "Dominion/Crystal Scar games"},
    {"gameMode": "ARAM", "description": "ARAM games"},
    {"gameMode": "TUTORIAL", "description": "Tutorial games"},
    {"gameMode": "URF", "description": "Ultra Rapid Fire games"},
    {"gameMode": "DOOMBOTSTEEMO", "description": "Doom Bot games"},
    {"gameMode": "ONEFORALL", "description": "One for All games"},
    {"gameMode": "ASCENSION", "description": "Ascension games"},
    {"gameMode": "FIRSTBLOOD", "description": "Snowdown Showdown games"},
    {"gameMode": "KINGPORO", "description": "Legend of the Poro King games"},
    {"gameMode": "SIEGE", "description": "Nexus Siege games"},
    {"gameMode": "ASSASSINATE", "description": "Blood Hunt Assassin games"},
    {"gameMode": "ARSR", "description": "All Random Summoner's Rift games"},
    {"gameMode": "DARKSTAR", "description": "Dark Star: Singularity games"},
    {"gameMode": "STARGUARDIAN", "description": "Star Guardian Invasion games"},
    {"gameMode": "PROJECT", "description": "PROJECT: Hunters games"},
    {"gameMode": "GAMEMODEX", "description": "Nexus Blitz games"},
    {"gameMode": "ODYSSEY", "description": "Odyssey: Extraction games"},
    {"gameMode": "NEXUSBLITZ", "description": "Nexus Blitz games"},
    {"gameMode": "ULTBOOK", "description": "Ultimate Spellbook games"}
]

GAME_TYPES = [
    {"gameType": "CUSTOM_GAME", "description": "Custom games"},
    {"gameType": "TUTORIAL_GAME", "description": "Tutorial games"},
    {"gameType": "MATCHED_GAME", "description": "All other games"}
]

SEASONS = [
    {"id": 0, "season": "PRESEASON 3"},
    {"id": 1, "season": "SEASON 3"},
    {"id": 2, "season": "PRESEASON 2014"},
    {"id": 3, "season": "SEASON 4"},
    {"id": 4, "season": "PRESEASON 2015"},
    {"id": 5, "season": "SEASON 5"},
    {"id": 6, "season": "PRESEASON 2016"},
    {"id": 7, "season": "SEASON 6"},
    {"id": 8, "season": "PRESEASON 2017"},
    {"id": 9, "season": "SEASON 7"},
    {"id": 10, "season": "PRESEASON 2018"},
    {"id": 11, "season": "SEASON 8"},
    {"id": 12, "season": "PRESEASON 2019"},
    {"id": 13, "season": "SEASON 9"},
    {"id": 14, "season": "PRESEASON 2020"},
    {"id": 15, "season": "SEASON 10"},
    {"id": 16, "season": "PRESEASON 2021"},
    {"id": 17, "season": "SEASON 11"},
    {"id": 18, "season": "PRESEASON 2022"},
    {"id": 19, "season": "SEASON 12"},
    {"id": 20, "season": "PRESEASON 2023"},
    {"id": 21, "season": "SEASON 13"},
    {"id": 22, "season": "PRESEASON 2024"},
    {"id": 23, "season": "SEASON 14"},
    {"id": 24, "season": "PRESEASON 2025"},
    {"id": 25, "season": "SEASON 15"}
]


def register_game_constants_resources(mcp: FastMCP):
    """Register all game constants resources."""
    
    @mcp.resource("constants://queues", description="Get all queue types and IDs")
    async def get_queue_types() -> str:
        """Get all queue types with descriptions."""
        logger.info("Resource called: get_queue_types")
        
        result = """
LEAGUE OF LEGENDS QUEUE TYPES
============================

CURRENT ACTIVE QUEUES:
"""
        
        for queue in QUEUE_TYPES:
            result += f"""
Queue ID: {queue['queueId']}
  Map: {queue['map']}
  Description: {queue['description'] or 'N/A'}
  Notes: {queue['notes'] or 'None'}
"""
        
        return result

    @mcp.resource("constants://maps", description="Get all map IDs and names")
    async def get_maps() -> str:
        """Get all map information."""
        logger.info("Resource called: get_maps")
        
        result = f"""
LEAGUE OF LEGENDS MAPS
=====================
Total Maps: {len(MAPS)}

MAP DETAILS:
"""
        
        for map_info in MAPS:
            result += f"""
Map ID: {map_info['mapId']}
  Name: {map_info['mapName']}
  Notes: {map_info['notes']}
"""
        
        return result

    @mcp.resource("constants://game_modes", description="Get all game modes")
    async def get_game_modes() -> str:
        """Get all game mode information."""
        logger.info("Resource called: get_game_modes")
        
        result = f"""
LEAGUE OF LEGENDS GAME MODES
===========================
Total Game Modes: {len(GAME_MODES)}

GAME MODE DETAILS:
"""
        
        for mode in GAME_MODES:
            result += f"""
Mode: {mode['gameMode']}
  Description: {mode['description']}
"""
        
        return result

    @mcp.resource("constants://game_types", description="Get all game types")
    async def get_game_types() -> str:
        """Get all game type information."""
        logger.info("Resource called: get_game_types")
        
        result = f"""
LEAGUE OF LEGENDS GAME TYPES
===========================
Total Game Types: {len(GAME_TYPES)}

GAME TYPE DETAILS:
"""
        
        for game_type in GAME_TYPES:
            result += f"""
Type: {game_type['gameType']}
  Description: {game_type['description']}
"""
        
        return result

    @mcp.resource("constants://seasons", description="Get all season IDs")
    async def get_seasons() -> str:
        """Get all season information."""
        logger.info("Resource called: get_seasons")
        
        result = f"""
LEAGUE OF LEGENDS SEASONS
========================
Total Seasons: {len(SEASONS)}

SEASON DETAILS:
"""
        
        for season in SEASONS:
            result += f"ID {season['id']:2d}: {season['season']}\n"
        
        return result

    @mcp.resource("constants://ranked_tiers", description="Get ranked tier information")
    async def get_ranked_tiers() -> str:
        """Get ranked tier and division information."""
        logger.info("Resource called: get_ranked_tiers")
        
        result = """
LEAGUE OF LEGENDS RANKED SYSTEM
==============================

RANKED TIERS (Lowest to Highest):
1. IRON (IV, III, II, I)
2. BRONZE (IV, III, II, I)
3. SILVER (IV, III, II, I)
4. GOLD (IV, III, II, I)
5. PLATINUM (IV, III, II, I)
6. EMERALD (IV, III, II, I)
7. DIAMOND (IV, III, II, I)
8. MASTER (Single tier, LP-based)
9. GRANDMASTER (Single tier, LP-based)
10. CHALLENGER (Single tier, LP-based)

QUEUE TYPES FOR RANKING:
- RANKED_SOLO_5x5: Solo/Duo Queue
- RANKED_FLEX_SR: Flex Queue (Summoner's Rift)
- RANKED_FLEX_TT: Flex Queue (Twisted Treeline) [DEPRECATED]

NOTES:
- Tiers 1-7 have divisions (IV being lowest, I being highest)
- Master, Grandmaster, and Challenger use LP (League Points) system
- Each queue type has separate rankings
- Emerald tier was added in Season 13
"""
        
        return result

    @mcp.resource("constants://routing", description="Get platform and regional routing information")
    async def get_routing_info() -> str:
        """Get routing information for API calls."""
        logger.info("Resource called: get_routing_info")
        
        result = """
RIOT API ROUTING INFORMATION
===========================

PLATFORM ROUTING VALUES:
Platform    Host
--------    ----
BR1         br1.api.riotgames.com
EUN1        eun1.api.riotgames.com
EUW1        euw1.api.riotgames.com
JP1         jp1.api.riotgames.com
KR          kr.api.riotgames.com
LA1         la1.api.riotgames.com
LA2         la2.api.riotgames.com
NA1         na1.api.riotgames.com
OC1         oc1.api.riotgames.com
TR1         tr1.api.riotgames.com
RU          ru.api.riotgames.com

REGIONAL ROUTING VALUES:
Region      Host
------      ----
AMERICAS    americas.api.riotgames.com
ASIA        asia.api.riotgames.com
EUROPE      europe.api.riotgames.com

PLATFORM TO REGION MAPPING:
AMERICAS: BR1, LA1, LA2, NA1, OC1
ASIA: JP1, KR
EUROPE: EUN1, EUW1, TR1, RU
"""
        
        return result 