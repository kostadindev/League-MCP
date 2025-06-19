from typing import Any
import httpx
import logging
import os
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

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

# Get API key from environment
API_KEY = os.getenv("RIOT_API_KEY")

def get_routing_region(platform_region: str) -> str:
    """Convert platform region to routing region for Match v5 API."""
    return PLATFORM_TO_ROUTING.get(platform_region, "americas")

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