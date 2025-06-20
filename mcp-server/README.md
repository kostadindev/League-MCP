# League of Legends MCP Server

A Model Context Protocol server that provides LLMs comprehensive access to League of Legends game data through the Riot Games API. This server enables LLMs to retrieve player statistics, match history, champion information, tournament data, and much more.

https://github.com/user-attachments/assets/101ee6dc-af42-4bf0-81b0-3caba49c83a7

> **Note**: This server requires a valid Riot Games API key. You can obtain one for free at [developer.riotgames.com](https://developer.riotgames.com/).

## Available Tools

### Account API
- `get_account_by_puuid` - Get account information by PUUID
- `get_account_by_riot_id` - Get account by Riot ID (gameName#tagLine)
- `get_active_shard` - Get the active shard for a player
- `get_active_region` - Get the active region for a player

### Summoner API
- `get_summoner_by_puuid` - Get summoner information by PUUID
- `get_summoner_by_account_id` - Get summoner by account ID
- `get_summoner_by_summoner_id` - Get summoner by summoner ID
- `get_summoner_by_rso_puuid` - Get summoner by RSO PUUID

### Match API
- `get_match_history` - Get match history IDs with filtering options
- `get_match_details` - Get detailed match information and player statistics
- `get_match_timeline` - Get match timeline with events and frame-by-frame data

### League API
- `get_challenger_league` - Get challenger tier league information
- `get_grandmaster_league` - Get grandmaster tier league information
- `get_master_league` - Get master tier league information
- `get_league_entries_by_puuid` - Get league entries for a player
- `get_league_entries_by_summoner` - Get league entries by summoner ID
- `get_league_by_id` - Get league information by ID
- `get_league_entries` - Get league entries by tier and division

### Champion API
- `get_champion_rotations` - Get current free-to-play champion rotation

### Spectator API
- `get_active_game` - Get active game information for a summoner
- `get_featured_games` - Get list of featured games

### Clash API
- `get_clash_player` - Get Clash tournament registrations for a player
- `get_clash_team` - Get Clash team information
- `get_clash_tournaments` - Get list of Clash tournaments
- `get_clash_tournament_by_team` - Get tournament information by team ID
- `get_clash_tournament_by_id` - Get tournament by ID

### Challenges API
- `get_all_challenges` - Get all challenge configuration data
- `get_challenge_config` - Get specific challenge configuration details
- `get_challenge_leaderboards` - Get challenge leaderboards (Master/Grandmaster/Challenger)
- `get_player_challenges` - Get player challenge progress and achievements
- `get_challenge_percentiles` - Get challenge percentile data

### Tournament API
- `register_tournament_provider` - Register as tournament provider (Production key required)
- `create_tournament` - Create tournaments for organized play
- `create_tournament_code` - Generate tournament codes for matches
- `get_tournament_code` - Get tournament code details and participants
- `get_lobby_events` - Monitor tournament lobby events

### Status API
- `get_platform_status` - Get platform status and maintenance information

## Resources

### Data Dragon Resources
- `ddragon://versions` - All available Data Dragon versions
- `ddragon://languages` - Supported localization languages  
- `ddragon://champions` - All champions summary data
- `ddragon://champion/{id}` - Detailed champion information
- `ddragon://items` - Complete items database
- `ddragon://summoner_spells` - Summoner spells data

### Game Constants
- `constants://queues` - Queue types and IDs reference
- `constants://routing` - Platform/regional routing guide


## Installation

### Using pip
```bash
pip install league-mcp
```

### Using uv
When using uv no specific installation is needed. We will use uvx to directly run league-mcp.

### Using pip from source
```bash
git clone https://github.com/kostadindevLeague-of-Legends-MCP.git
cd League-of-Legends-MCP/mcp-server
pip install -e .
```

After installation, you can run it as a script using:
```bash
league-mcp
```

## Configuration

### Configure for Claude.app
Add to your Claude settings:

#### Using pip installation
```json
{
  "mcpServers": {
    "league-mcp": {
      "command": "league-mcp",
      "args": ["--transport", "stdio"],
      "env": {
        "RIOT_API_KEY": "your_riot_api_key_here"
      }
    }
  }
}
```

#### Using uvx
```json
{
  "mcpServers": {
    "league-mcp": {
      "command": "uvx",
      "args": ["league-mcp", "--transport", "stdio"],
      "env": {
        "RIOT_API_KEY": "your_riot_api_key_here"
      }
    }
  }
}
```

## Usage

### Basic Usage
```bash
# Run with default stdio transport
league-mcp

# Run with SSE transport for remote integrations
league-mcp --transport sse

# Get help
league-mcp --help
```

### Environment Variables
Set your Riot API key:
```bash
export RIOT_API_KEY=your_riot_api_key_here
```

Or create a `.env` file:
```env
RIOT_API_KEY=your_riot_api_key_here
```

## Testing the Server

You can test the League MCP Server using:

### Option 1: Provided MCP Client (Recommended)
Use the included MCP client with a web UI for interactive testing

The MCP client is available at: https://github.com/kostadindev/League-of-Legends-MCP/tree/main/mcp-client

### Option 2: Claude Desktop
Configure the server in Claude Desktop using the configuration examples above.

## Customization

### Transport Types
The server supports two transport types:

- **stdio** (default): Standard input/output transport for direct integration with MCP clients like Claude Desktop
- **sse**: Server-Sent Events transport for web-based integrations and HTTP connections


## API Coverage

This server provides comprehensive coverage of the Riot Games API:

- **10 API endpoints** with 35+ tools
- **Static game data** via Data Dragon resources
- **Game constants** for queues, routing, and more

## Contributing

We encourage contributions to help expand and improve league-mcp. Whether you want to add new tools, enhance existing functionality, or improve documentation, your input is valuable.

For examples of other MCP servers and implementation patterns, see: https://github.com/modelcontextprotocol/servers

Pull requests are welcome! Feel free to contribute new ideas, bug fixes, or enhancements to make league-mcp even more powerful and useful.

## License

league-mcp is licensed under the MIT License. This means you are free to use, modify, and distribute the software, subject to the terms and conditions of the MIT License. For more details, please see the LICENSE file in the project repository.

## Disclaimer

This project is not endorsed by Riot Games and does not reflect the views or opinions of Riot Games or anyone officially involved in producing or managing Riot Games properties. Riot Games and all associated properties are trademarks or registered trademarks of Riot Games, Inc. 