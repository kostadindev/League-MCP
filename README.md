# League MCP Server 🎮

A Model Context Protocol (MCP) server that provides access to Riot Games API endpoints for League of Legends account management. This project implements the Account-v1 API as MCP tools, allowing AI assistants to look up player information, account details, and regional data.

## 🚀 Features

- **Account Lookup**: Search by Riot ID (gameName#tagLine) or PUUID
- **Regional Support**: Americas, Asia, and Europe routing
- **Multi-Game Support**: League of Legends, VALORANT, TFT, and Legends of Runeterra
- **Smart AI Integration**: Powered by Google Gemini for natural language queries
- **Comprehensive Logging**: Detailed request/response tracking
- **Error Handling**: Robust API error management

## 📁 Project Structure

```
League-MCP/
├── mcp-server/          # MCP Server implementation
│   ├── league.py        # Main server with Riot API tools
│   ├── pyproject.toml   # Server dependencies
│   └── README.md        # Server-specific docs
├── mcp-client/          # MCP Client implementation
│   ├── client.py        # AI-powered client
│   ├── pyproject.toml   # Client dependencies
│   └── README.md        # Client-specific docs
└── README.md           # This file
```

## 🛠️ Available Tools

### Account Management
- **`get_account_by_riot_id`** - Look up account by Riot ID (e.g., "Faker#T1")
- **`get_account_by_puuid`** - Get account details by PUUID
- **`get_active_shard`** - Find active shard for a player
- **`get_active_region`** - Get active region for LoL/TFT players

### Supported Games
- **League of Legends** (`lol`)
- **VALORANT** (`val`) 
- **Teamfight Tactics** (`tft`)
- **Legends of Runeterra** (`lor`)

## ⚡ Quick Start

### 1. Prerequisites

- Python 3.8+
- Riot Games API Key ([Get one here](https://developer.riotgames.com/))
- Google API Key for Gemini (optional, for AI client)

### 2. Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd League-MCP
   ```

2. **Install dependencies**
   ```bash
   # Server dependencies
   cd mcp-server
   pip install -r requirements.txt  # or use uv/poetry based on pyproject.toml

   # Client dependencies  
   cd ../mcp-client
   pip install -r requirements.txt
   ```

3. **Set environment variables**
   ```bash
   # Required for server
   export RIOT_API_KEY="your-riot-api-key-here"
   
   # Optional for AI client
   export GOOGLE_API_KEY="your-gemini-api-key-here"
   ```

   **Windows PowerShell:**
   ```powershell
   $env:RIOT_API_KEY="your-riot-api-key-here"
   $env:GOOGLE_API_KEY="your-gemini-api-key-here"
   ```

### 3. Usage

**Start the AI-powered client:**
```bash
cd mcp-client
python client.py ../mcp-server/league.py
```

**Example queries:**
- `"look up Faker T1"`
- `"get account for Doublelift NA1"`  
- `"what region is [puuid] playing LoL in?"`
- `"get VALORANT shard for [puuid]"`

## 💬 Example Interaction

```
🎮 League Query: look up Faker T1

🔄 Executing: get_account_by_riot_id(game_name=Faker, tag_line=T1)

📊 Result:
PUUID: 4_Bc7dJQI8hKhRK_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
Game Name: Faker
Tag Line: T1  
Riot ID: Faker#T1
```

## 🌍 Regional Routing

The API supports three regional clusters:

- **Americas** (`americas`) - North/South America
- **Asia** (`asia`) - Asia Pacific  
- **Europe** (`europe`) - Europe, Middle East, Africa

## 🔧 Configuration

### Server Configuration
- **API Base**: `https://{region}.api.riotgames.com`
- **Default Region**: `americas`
- **Timeout**: 30 seconds
- **Logging Level**: INFO (configurable)

### Client Configuration  
- **AI Model**: Google Gemini 2.5 Flash
- **MCP Transport**: stdio
- **Logging**: Comprehensive request/response tracking

## 📝 API Reference

### get_account_by_riot_id
```python
await get_account_by_riot_id(
    game_name="Faker", 
    tag_line="T1", 
    region="americas"
)
```

### get_account_by_puuid
```python
await get_account_by_puuid(
    puuid="your-78-character-puuid",
    region="americas" 
)
```

### get_active_shard
```python
await get_active_shard(
    game="val",  # val, lol, tft, lor
    puuid="your-puuid",
    region="americas"
)
```

### get_active_region
```python
await get_active_region(
    game="lol",  # lol, tft
    puuid="your-puuid", 
    region="americas"
)
```

## 🐛 Troubleshooting

### Common Issues

**"RIOT_API_KEY environment variable not set"**
- Ensure you've set your API key: `export RIOT_API_KEY="your-key"`
- Check the key is valid at [Riot Developer Portal](https://developer.riotgames.com/)

**HTTP 403 Forbidden**
- Your API key may be expired or invalid
- Check if you're hitting rate limits

**HTTP 404 Not Found**
- Player/account doesn't exist
- Check spelling of gameName and tagLine
- Try a different region

**Connection Issues**
- Ensure Python dependencies are installed
- Check your internet connection
- Verify the server script path is correct

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable  
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This project is not affiliated with Riot Games. League of Legends, VALORANT, Teamfight Tactics, and Legends of Runeterra are trademarks of Riot Games, Inc.

## 📚 Resources

- [Riot Games API Documentation](https://developer.riotgames.com/docs/portal)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)

---

**Made with ❤️ for the League community** 