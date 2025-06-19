# League Model Context Protocol (MCP)

A Model Context Protocol (MCP) server for League of Legends exposing all Riot Games APIs, static resources (champions, items, tiers, etc.), and workflow prompts. Includes a MCP client with a chatbot UI to demonstrate it's utility made using a ReAct agent for tool/resource/prompt calls. You can build your own client or use Claude for Desktop.

## MCP Server Features
- Riot Games API coverage: Account, Summoner, Match, League, Spectator, Champion, Clash, Tournament, Status, Challenges
- Static resources: champions, items, summoner spells, queues, maps, game modes, ranked tiers
- Workflow prompts: player stats, champion analysis, team comps, tournaments, improvement plans

## MCP Client Features (Optional)
- ReAct Agent
- Chatbot UI
- Tool calling logs

## Quickstart

1. Clone and install dependencies:
   ```bash
   git clone <this-repo-url>
   cd League-MCP
   # (pip install -r requirements in mcp-server and mcp-client as needed)
   ```

2. Set environment variables in `.env` files:
   - In `mcp-server/.env`:
     ```env
     RIOT_API_KEY=your_riot_api_key
     ```
   - In `mcp-client/.env`:
     ```env
     GOOGLE_API_KEY=your_google_api_key
     ```

3. Run the MCP server:
   ```bash
   cd mcp-server
   python main.py
   ```

4. Run the MCP client (from the project root):
   ```bash
   python mcp-client/client.py mcp-server/main.py
   ```

- The client launches a Gradio web UI. Example queries:
  - What is the current rank of Sneaky#NA69?
  - Show me ddragon://champions
  - Use find_player_stats for Faker#T1

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

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## ⚠️ Disclaimer

This project is not endorsed by Riot Games and does not reflect the views or opinions of Riot Games or anyone officially involved in producing or managing Riot Games properties. Riot Games and all associated properties are trademarks or registered trademarks of Riot Games, Inc.

## 📚 Resources

- [Riot Games API Documentation](https://developer.riotgames.com/docs/portal)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
---

**Made with ❤️ for the League community** 