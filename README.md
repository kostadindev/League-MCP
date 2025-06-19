# League of Legends Model Context Protocol (MCP)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

A Model Context Protocol (MCP) server for League of Legends exposing all Riot Games APIs, static resources (champions, items, tiers, etc.), and workflow prompts. Includes a MCP client with a chatbot UI to demonstrate it's utility made using a ReAct agent for tool/resource/prompt calls. You can build your own client or use Claude for Desktop.

## MCP Server Features
- Riot Games API coverage: Account, Summoner, Match, League, Spectator, Champion, Clash, Tournament, Status, Challenges
- Static resources: champions, items, summoner spells, queues, maps, game modes, ranked tiers
- Workflow prompts: player stats, champion analysis, team comps, tournaments, improvement plans

## MCP Client Features (Optional)
- ReAct Agent
- Chatbot UI
- Tool calling
- Resource Utilization
- Prompt Workflows

https://github.com/user-attachments/assets/101ee6dc-af42-4bf0-81b0-3caba49c83a7


## Quickstart

1. Clone the repository:
   ```bash
   git clone https://github.com/kostadindev/League-of-Legends-MCP.git
   cd League-of-Legends-MCP
Public
   ```

2. Install dependencies (choose one method):

   **Option A: Using pip**
   - In `mcp-server/`:
     ```bash
     cd mcp-server
     python -m venv .venv
     # Windows:
     .venv\Scripts\activate
     # macOS/Linux:
     # source .venv/bin/activate
     pip install -r requirements.txt
     cd ..
     ```
   - In `mcp-client/`:
     ```bash
     cd mcp-client
     python -m venv .venv
     # Windows:
     .venv\Scripts\activate
     # macOS/Linux:
     # source .venv/bin/activate
     pip install -r requirements.txt
     cd ..
     ```
   
   > **Note**: With pip, you need to manually create and activate virtual environments. Remember to activate the appropriate environment before running the applications!

   **Option B: Using uv (recommended for faster installs)**
   - First install uv if you haven't already:
     ```bash
     pip install uv
     ```
   - In `mcp-server/`:
     ```bash
     cd mcp-server
     uv sync
     cd ..
     ```
   - In `mcp-client/`:
     ```bash
     cd mcp-client
     uv sync
     cd ..
     ```
   
   > **Note**: uv automatically creates and manages `.venv` virtual environments in each directory. You don't need to manually create or activate them!

3. Set environment variables in `.env` files:
   - In `mcp-server/.env`:
     ```env
     RIOT_API_KEY=your_riot_api_key
     ```
   - In `mcp-client/.env` (only if you want to try out the client):
     ```env
     GOOGLE_API_KEY=your_gemini_api_key
     ```

4. Run the MCP server independently:

   **Using pip/python:**
   ```bash
   cd mcp-server
   python main.py
   ```

   **Using uv:**
   ```bash
   cd mcp-server
   uv run main.py
   ```

4.5. Run the MCP client and the MCP server together (from the project root):

   **Using pip/python:**
   ```bash
   python mcp-client/client.py mcp-server/main.py
   ```

   **Using uv:**
   ```bash
   uv run mcp-client/client.py mcp-server/main.py
   ```

- The client launches a Gradio web UI. Example queries:
  - What is the current rank of Sneaky#NA69?
  - Show me ddragon://champions

## Project Structure

- `mcp-server/` - MCP server (all Riot APIs, resources, prompts)
- `mcp-client/` - LangChain ReAct agent client (Gradio UI)

## Requirements

- Python 3.9+
- Riot API key (for server)
- Google API key (for client)

## References

- [Riot Games Developer Portal](https://developer.riotgames.com/)
- [Model Context Protocol (MCP)](https://github.com/langchain-ai/mcp)
- [LangChain](https://github.com/langchain-ai/langchain)


## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details on how to get started.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This project is not endorsed by Riot Games and does not reflect the views or opinions of Riot Games or anyone officially involved in producing or managing Riot Games properties. Riot Games and all associated properties are trademarks or registered trademarks of Riot Games, Inc.

## 📚 Resources

- [Riot Games API Documentation](https://developer.riotgames.com/docs/portal)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
---

**Made with ❤️ for the League community** 
