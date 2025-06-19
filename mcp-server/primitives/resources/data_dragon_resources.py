"""Data Dragon resources for League of Legends static data."""

import logging
from mcp.server.fastmcp import FastMCP
import httpx

logger = logging.getLogger(__name__)

# Data Dragon constants
DATA_DRAGON_BASE = "https://ddragon.leagueoflegends.com"
LATEST_VERSION = "15.12.1"  # This should be updated or fetched dynamically


def register_data_dragon_resources(mcp: FastMCP):
    """Register all Data Dragon resources."""
    
    @mcp.resource(name="ddragon://versions", description="Get all available Data Dragon versions")
    async def get_versions() -> str:
        """Get all available Data Dragon versions."""
        logger.info("Resource called: get_versions")
        
        url = f"{DATA_DRAGON_BASE}/api/versions.json"
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, timeout=30.0)
                response.raise_for_status()
                versions = response.json()
                
                result = f"""
DATA DRAGON VERSIONS
===================
Total Versions: {len(versions)}
Latest Version: {versions[0] if versions else 'N/A'}

Recent Versions:
"""
                for i, version in enumerate(versions[:10], 1):
                    result += f"{i:2d}. {version}\n"
                
                if len(versions) > 10:
                    result += f"\n... and {len(versions) - 10} more versions"
                
                return result
                
            except Exception as e:
                error_msg = f"Failed to fetch versions: {str(e)}"
                logger.error(error_msg)
                return f"Error: {error_msg}"

    @mcp.resource(name="ddragon://languages", description="Get all supported languages")
    async def get_languages() -> str:
        """Get all supported Data Dragon languages."""
        logger.info("Resource called: get_languages")
        
        url = f"{DATA_DRAGON_BASE}/cdn/languages.json"
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, timeout=30.0)
                response.raise_for_status()
                languages = response.json()
                
                # Language mapping
                language_names = {
                    "cs_CZ": "Czech (Czech Republic)",
                    "el_GR": "Greek (Greece)",
                    "pl_PL": "Polish (Poland)",
                    "ro_RO": "Romanian (Romania)",
                    "hu_HU": "Hungarian (Hungary)",
                    "en_GB": "English (United Kingdom)",
                    "de_DE": "German (Germany)",
                    "es_ES": "Spanish (Spain)",
                    "it_IT": "Italian (Italy)",
                    "fr_FR": "French (France)",
                    "ja_JP": "Japanese (Japan)",
                    "ko_KR": "Korean (Korea)",
                    "es_MX": "Spanish (Mexico)",
                    "es_AR": "Spanish (Argentina)",
                    "pt_BR": "Portuguese (Brazil)",
                    "en_US": "English (United States)",
                    "en_AU": "English (Australia)",
                    "ru_RU": "Russian (Russia)",
                    "tr_TR": "Turkish (Turkey)",
                    "ms_MY": "Malay (Malaysia)",
                    "en_PH": "English (Republic of the Philippines)",
                    "en_SG": "English (Singapore)",
                    "th_TH": "Thai (Thailand)",
                    "vi_VN": "Vietnamese (Viet Nam)",
                    "id_ID": "Indonesian (Indonesia)",
                    "zh_MY": "Chinese (Malaysia)",
                    "zh_CN": "Chinese (China)",
                    "zh_TW": "Chinese (Taiwan)"
                }
                
                result = f"""
DATA DRAGON LANGUAGES
====================
Total Languages: {len(languages)}

Supported Languages:
"""
                for i, lang_code in enumerate(languages, 1):
                    lang_name = language_names.get(lang_code, "Unknown")
                    result += f"{i:2d}. {lang_code} - {lang_name}\n"
                
                return result
                
            except Exception as e:
                error_msg = f"Failed to fetch languages: {str(e)}"
                logger.error(error_msg)
                return f"Error: {error_msg}"

    @mcp.resource(name="ddragon://champion/{champion_id}", description="Get champion data by ID")
    async def get_champion_data(champion_id: str, version: str = LATEST_VERSION, language: str = "en_US") -> str:
        """Get detailed champion data."""
        logger.info(f"Resource called: get_champion_data(champion_id={champion_id})")
        
        url = f"{DATA_DRAGON_BASE}/cdn/{version}/data/{language}/champion/{champion_id}.json"
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, timeout=30.0)
                response.raise_for_status()
                data = response.json()
                
                champion = data['data'][champion_id]
                
                result = f"""
CHAMPION DATA: {champion['name']}
{'=' * (15 + len(champion['name']))}
ID: {champion['id']}
Key: {champion['key']}
Title: {champion['title']}
Version: {version}
Language: {language}

LORE:
{champion.get('lore', 'No lore available')}

TAGS: {', '.join(champion.get('tags', []))}

STATS:
"""
                stats = champion.get('stats', {})
                for stat_name, value in stats.items():
                    result += f"  {stat_name}: {value}\n"
                
                # Spells
                spells = champion.get('spells', [])
                result += f"\nABILITIES ({len(spells)}):\n"
                for i, spell in enumerate(spells):
                    result += f"  {i+1}. {spell['name']} ({spell['id']})\n"
                    result += f"     {spell.get('description', 'No description')}\n\n"
                
                # Passive
                passive = champion.get('passive', {})
                if passive:
                    result += f"PASSIVE: {passive.get('name', 'N/A')}\n"
                    result += f"  {passive.get('description', 'No description')}\n"
                
                return result
                
            except Exception as e:
                error_msg = f"Failed to fetch champion data: {str(e)}"
                logger.error(error_msg)
                return f"Error: {error_msg}"

    @mcp.resource(name="ddragon://champions", description="Get all champions summary")
    async def get_champions_summary(version: str = LATEST_VERSION, language: str = "en_US") -> str:
        """Get summary of all champions."""
        logger.info("Resource called: get_champions_summary")
        
        url = f"{DATA_DRAGON_BASE}/cdn/{version}/data/{language}/champion.json"
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, timeout=30.0)
                response.raise_for_status()
                data = response.json()
                
                champions = data['data']
                
                result = f"""
ALL CHAMPIONS SUMMARY
====================
Version: {version}
Language: {language}
Total Champions: {len(champions)}

CHAMPION LIST:
"""
                for i, (champ_id, champ_data) in enumerate(champions.items(), 1):
                    name = champ_data['name']
                    title = champ_data['title']
                    tags = ', '.join(champ_data.get('tags', []))
                    result += f"{i:3d}. {name} ({champ_id}) - {title}\n"
                    result += f"     Tags: {tags}\n\n"
                
                return result
                
            except Exception as e:
                error_msg = f"Failed to fetch champions summary: {str(e)}"
                logger.error(error_msg)
                return f"Error: {error_msg}"

    @mcp.resource(name="ddragon://items", description="Get all items data")
    async def get_items_data(version: str = LATEST_VERSION, language: str = "en_US") -> str:
        """Get all items data."""
        logger.info("Resource called: get_items_data")
        
        url = f"{DATA_DRAGON_BASE}/cdn/{version}/data/{language}/item.json"
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, timeout=30.0)
                response.raise_for_status()
                data = response.json()
                
                items = data['data']
                
                result = f"""
ALL ITEMS DATA
=============
Version: {version}
Language: {language}
Total Items: {len(items)}

SAMPLE ITEMS (First 20):
"""
                for i, (item_id, item_data) in enumerate(list(items.items())[:20], 1):
                    name = item_data['name']
                    description = item_data.get('plaintext', 'No description')
                    gold = item_data.get('gold', {})
                    total_cost = gold.get('total', 0)
                    
                    result += f"{i:2d}. {name} (ID: {item_id})\n"
                    result += f"    Cost: {total_cost} gold\n"
                    result += f"    {description}\n\n"
                
                if len(items) > 20:
                    result += f"... and {len(items) - 20} more items\n"
                
                return result
                
            except Exception as e:
                error_msg = f"Failed to fetch items data: {str(e)}"
                logger.error(error_msg)
                return f"Error: {error_msg}"

    @mcp.resource(name="ddragon://summoner_spells", description="Get all summoner spells")
    async def get_summoner_spells(version: str = LATEST_VERSION, language: str = "en_US") -> str:
        """Get all summoner spells data."""
        logger.info("Resource called: get_summoner_spells")
        
        url = f"{DATA_DRAGON_BASE}/cdn/{version}/data/{language}/summoner.json"
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, timeout=30.0)
                response.raise_for_status()
                data = response.json()
                
                spells = data['data']
                
                result = f"""
SUMMONER SPELLS
==============
Version: {version}
Language: {language}
Total Spells: {len(spells)}

AVAILABLE SUMMONER SPELLS:
"""
                for i, (spell_id, spell_data) in enumerate(spells.items(), 1):
                    name = spell_data['name']
                    description = spell_data.get('description', 'No description')
                    cooldown = spell_data.get('cooldownBurn', 'N/A')
                    
                    result += f"{i:2d}. {name} (ID: {spell_id})\n"
                    result += f"    Cooldown: {cooldown}\n"
                    result += f"    {description}\n\n"
                
                return result
                
            except Exception as e:
                error_msg = f"Failed to fetch summoner spells: {str(e)}"
                logger.error(error_msg)
                return f"Error: {error_msg}" 