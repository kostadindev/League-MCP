# League MCP Client with LangChain

A League of Legends MCP (Model Context Protocol) client powered by LangChain's ReAct agent framework and Google Gemini.

## Features

- 🤖 **LangChain ReAct Agent**: Uses LangChain's `create_react_agent` for intelligent tool calling
- 🧠 **Google Gemini**: Powered by Google's Gemini 2.0 Flash model for advanced reasoning
- 🎮 **League API Integration**: Connects to League MCP server for Riot Games API access
- 🛠️ **Automatic Tool Discovery**: Dynamically converts MCP tools to LangChain tools
- 💬 **Interactive Chat**: Simple command-line interface for querying League data

## Setup

1. **Install dependencies**:
   ```bash
   pip install -e .
   ```

2. **Set up environment variables**:
   Create a `.env` file in this directory with:
   ```env
   GOOGLE_API_KEY=your_google_api_key_here
   ```

3. **Start the League MCP server** (in another terminal):
   ```bash
   cd ../mcp-server
   python main.py
   ```

4. **Run the client**:
   ```bash
   python client.py ../mcp-server/main.py
   ```

## Usage

The client supports natural language queries about League of Legends data:

- `"look up Faker T1"` - Get account info by Riot ID
- `"get account for PUUID abc123..."` - Look up by PUUID
- `"what region is [puuid] playing LoL in?"` - Find active region
- `"get VALORANT shard for [puuid]"` - Get game shard info

## How it Works

1. **MCP Connection**: Connects to the League MCP server to access Riot API tools
2. **Tool Conversion**: Automatically converts MCP tools to LangChain-compatible tools
3. **Agent Creation**: Creates a ReAct agent with Google Gemini and League-specific prompt
4. **Query Processing**: Uses the agent to intelligently decide when and how to use tools

## Dependencies

- `langchain-core>=0.3.8` - Core LangChain functionality
- `langchain-google-genai>=2.0.0` - Google Gemini integration for LangChain
- `langgraph>=0.2.35` - LangGraph for the ReAct agent
- `mcp>=1.9.4` - Model Context Protocol client
- `python-dotenv>=1.1.0` - Environment variable management

## Configuration

The client uses Google Gemini 2.0 Flash Experimental by default. You can customize the model in the code if needed. 