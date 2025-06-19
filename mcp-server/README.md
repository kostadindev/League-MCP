# League MCP Server

A Model Context Protocol (MCP) server for interacting with the Riot Games API for League of Legends.

## Project Structure

```
mcp-server/
├── main.py                     # Main entry point of the MCP server
├── services/                   # Business logic and external integrations
│   ├── __init__.py
│   └── riot_api_service.py     # Riot API HTTP client and constants
├── utils/                      # Helper functions and utilities
│   ├── __init__.py
│   └── formatters.py           # Response formatting functions
├── primitives/                 # MCP primitives (Tools, Resources, Prompts)
│   ├── __init__.py
│   ├── tools/                  # MCP Tools organized by API endpoint
│   │   ├── __init__.py
│   │   ├── account_tools.py    # Riot Account API tools
│   │   ├── summoner_tools.py   # LoL Summoner API tools
│   │   ├── spectator_tools.py  # LoL Spectator API tools
│   │   ├── champion_tools.py   # LoL Champion API tools
│   │   ├── clash_tools.py      # LoL Clash API tools
│   │   ├── league_tools.py     # LoL League API tools
│   │   └── status_tools.py     # LoL Status API tools
│   ├── resources/              # MCP Resources (currently empty)
│   │   └── __init__.py
│   └── prompts/               # MCP Prompts (currently empty)
│       └── __init__.py
└── league_original.py          # Original monolithic implementation (backup)
```

## API Coverage

### Account API (`account_tools.py`)
- Get account by PUUID
- Get account by Riot ID
- Get active shard for a player
- Get active region for a player

### Summoner API (`summoner_tools.py`)
- Get summoner by PUUID
- Get summoner by account ID
- Get summoner by summoner ID
- Get summoner by RSO PUUID

### Spectator API (`spectator_tools.py`)
- Get active game information
- Get featured games

### Champion API (`champion_tools.py`)
- Get champion rotation (free-to-play champions)

### Clash API (`clash_tools.py`)
- Get Clash player registrations
- Get Clash team information
- Get Clash tournaments
- Get tournament by team ID
- Get tournament by ID

### League API (`league_tools.py`)
- Get challenger/grandmaster/master leagues
- Get league entries by PUUID/summoner ID
- Get league by ID
- Get league entries by division

### Status API (`status_tools.py`)
- Get platform status and maintenance information

## Setup

1. Set your Riot API key as an environment variable:
   ```
   RIOT_API_KEY=your_api_key_here
   ```

2. Run the server:
   ```bash
   python main.py
   ```

## Architecture

The project follows a modular architecture:

- **Services**: Handle external API communication and business logic
- **Utils**: Provide formatting and helper functions
- **Primitives**: Define MCP tools, resources, and prompts organized by functionality
- **Main**: Entry point that registers all tools and starts the server

Each API endpoint category is separated into its own file with a registration function that adds all related tools to the MCP server. 