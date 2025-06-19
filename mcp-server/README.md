# League MCP Server

A Model Context Protocol (MCP) server for interacting with the Riot Games API for League of Legends.

## Project Structure

```
mcp-server/
├── main.py                           # Main entry point with enhanced registrations
├── services/                         # Business logic and external integrations
│   ├── __init__.py
│   └── riot_api_service.py          # Riot API HTTP client and constants
├── utils/                           # Helper functions and utilities
│   ├── __init__.py
│   └── formatters.py                # Enhanced response formatting functions
├── primitives/                      # MCP primitives (Tools, Resources, Prompts)
│   ├── __init__.py
│   ├── tools/                       # MCP Tools organized by API endpoint
│   │   ├── __init__.py
│   │   ├── account_tools.py         # Riot Account API tools
│   │   ├── summoner_tools.py        # LoL Summoner API tools
│   │   ├── spectator_tools.py       # LoL Spectator API tools
│   │   ├── champion_tools.py        # LoL Champion API tools
│   │   ├── clash_tools.py           # LoL Clash API tools
│   │   ├── league_tools.py          # LoL League API tools
│   │   ├── status_tools.py          # LoL Status API tools
│   │   ├── match_tools.py           # ⚡ LoL Match API tools (NEW)
│   │   ├── challenges_tools.py      # ⚡ LoL Challenges API tools (NEW)
│   │   └── tournament_tools.py      # ⚡ LoL Tournament API tools (NEW)
│   ├── resources/                   # ⚡ MCP Resources for static data (NEW)
│   │   ├── __init__.py
│   │   ├── data_dragon_resources.py # ⚡ Data Dragon static data access
│   │   └── game_constants_resources.py # ⚡ Game constants and routing info
│   └── prompts/                     # ⚡ MCP Prompts for workflows (NEW)
│       ├── __init__.py
│       └── common_workflows.py      # ⚡ Common use case workflows
└── league_original.py               # Original monolithic implementation (backup)
```

## Enhanced API Coverage ⚡

### 🔧 Tools (35+ API Endpoints)

#### Account API (`account_tools.py`)
- Get account by PUUID
- Get account by Riot ID (gameName#tagLine)
- Get active shard for a player
- Get active region for a player

#### Summoner API (`summoner_tools.py`)
- Get summoner by PUUID
- Get summoner by account ID
- Get summoner by summoner ID
- Get summoner by RSO PUUID

#### Match API (`match_tools.py`) ⚡ **NEW**
- Get match history IDs by PUUID with filtering options
- Get detailed match information and player statistics
- Get match timeline with events and frame-by-frame data

#### Challenges API (`challenges_tools.py`) ⚡ **NEW**
- Get all challenge configuration data
- Get specific challenge configuration details
- Get challenge leaderboards (Master/Grandmaster/Challenger)
- Get player challenge progress and achievements
- Get challenge percentile data across all challenges

#### Tournament API (`tournament_tools.py`) ⚡ **NEW**
- Register as tournament provider (Production key required)
- Create tournaments for organized play
- Generate tournament codes for matches
- Get tournament code details and participants
- Monitor tournament lobby events

#### Spectator API (`spectator_tools.py`)
- Get active game information
- Get featured games

#### Champion API (`champion_tools.py`)
- Get champion rotation (free-to-play champions)

#### Clash API (`clash_tools.py`)
- Get Clash player registrations
- Get Clash team information
- Get Clash tournaments
- Get tournament by team ID
- Get tournament by ID

#### League API (`league_tools.py`)
- Get challenger/grandmaster/master leagues
- Get league entries by PUUID/summoner ID
- Get league by ID
- Get league entries by division

#### Status API (`status_tools.py`)
- Get platform status and maintenance information

### 📚 Resources (Static Game Data)

#### Data Dragon Resources (`data_dragon_resources.py`) ⚡
- **ddragon://versions**: All available Data Dragon versions
- **ddragon://languages**: Supported localization languages
- **ddragon://champions**: All champions summary data
- **ddragon://champion/{id}**: Detailed champion information
- **ddragon://items**: Complete items database
- **ddragon://summoner_spells**: Summoner spells data

#### Game Constants (`game_constants_resources.py`) ⚡
- **constants://queues**: Queue types and IDs reference
- **constants://routing**: Platform/regional routing guide

### 🚀 Prompts (Workflow Automation)

#### Common Workflows (`common_workflows.py`) ⚡
- **find_player_stats**: Complete player analysis workflow
- **tournament_setup**: Tournament organization guide with compliance

## Setup

1. Set your Riot API key as an environment variable:
   ```
   RIOT_API_KEY=your_api_key_here
   ```

2. Run the server:
   ```bash
   python main.py
   ```

## New Capabilities ⚡

### 🔍 Comprehensive Player Analysis
- Complete match history analysis with detailed statistics
- Challenge progression tracking and leaderboard positions
- Cross-referenced champion mastery and performance data
- Automated player profile generation with insights

### 🏆 Tournament Organization Support
- Full tournament provider registration workflow
- Tournament code generation and management
- Real-time lobby event monitoring
- Match result callback handling (Production key required)

### 📊 Static Game Data Access
- Champion abilities, stats, and lore from Data Dragon
- Complete items database with costs and effects
- Summoner spells and their cooldowns
- Game constants (queues, maps, seasons) for reference

### 🚀 Workflow Automation
- Pre-built prompts for common analysis tasks
- Step-by-step tournament setup guidance
- Player improvement recommendation workflows
- Champion and team composition analysis guides

### 🎯 Advanced Features
- Multi-language support for game data
- Regional routing optimization
- Challenge system integration
- Ranked tier and division tracking

## Architecture

The project follows a modular architecture:

- **Services**: Handle external API communication and business logic
- **Utils**: Provide formatting and helper functions  
- **Primitives**: Define MCP tools, resources, and prompts organized by functionality
  - **Tools**: API endpoint wrappers (35+ tools across 10 APIs)
  - **Resources**: Static data access (Data Dragon, game constants)
  - **Prompts**: Workflow automation and analysis guides
- **Main**: Entry point that registers all components and starts the server

Each API endpoint category is separated into its own file with a registration function that adds all related tools to the MCP server.

## Compliance & Best Practices

This server implements Riot Games API best practices:

- **Rate Limiting**: Proper rate limit handling and backoff strategies
- **Security**: API key protection and HTTPS-only communication
- **Tournament Policies**: Full compliance with tournament organization requirements
- **Data Usage**: Adherence to Riot's developer API policies
- **Routing**: Correct platform and regional routing for optimal performance 