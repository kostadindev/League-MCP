import asyncio
import os
import sys
import logging
from typing import Optional
from pathlib import Path

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.messages import HumanMessage
from langchain_core.callbacks import BaseCallbackHandler
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ToolCallLogger(BaseCallbackHandler):
    """Custom callback handler to log tool calls"""
    
    def on_tool_start(self, serialized: dict, input_str: str, **kwargs) -> None:
        """Log when a tool starts executing"""
        tool_name = serialized.get("name", "Unknown")
        print(f"\n🔧 TOOL CALL START: {tool_name}")
        print(f"📋 Tool Input: {input_str}")
        logger.info(f"Tool started: {tool_name} with input: {input_str}")
    
    def on_tool_end(self, output: str, **kwargs) -> None:
        """Log when a tool finishes executing"""
        print(f"✅ TOOL CALL RESULT:")
        print(f"📤 Output: {output}")
        print(f"{'='*50}")
        logger.info(f"Tool completed with output: {output[:200]}...")
    
    def on_tool_error(self, error: Exception, **kwargs) -> None:
        """Log when a tool encounters an error"""
        print(f"❌ TOOL CALL ERROR: {error}")
        logger.error(f"Tool error: {error}")

class LeagueMCPClient:
    def __init__(self):
        # Initialize client objects
        self.mcp_client: Optional[MultiServerMCPClient] = None
        self.agent = None
        self.tools = []
        
        # Initialize LangChain model with Google Gemini
        google_api_key = os.getenv('GOOGLE_API_KEY')
        if not google_api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is required")
        
        self.model = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",
            temperature=0,
            google_api_key=google_api_key
        )
        
        # Initialize callback handler for tool logging
        self.callback_handler = ToolCallLogger()
        
        logger.info("LeagueMCPClient initialized with LangChain and Google Gemini")
    
    async def process_query(self, query: str) -> str:
        """Process a League-related query using LangChain ReAct agent with Gemini"""
        logger.info(f"Processing user query: {query}")
        
        if not self.agent:
            return "❌ Agent not initialized. Please connect to the MCP server first."
        
        try:
            # Create the input for the agent
            input_messages = [HumanMessage(content=query)]
            
            # Run the agent with callback for tool logging
            logger.info("Running LangChain ReAct agent with Google Gemini...")
            print(f"\n🤖 AGENT PROCESSING: {query}")
            print(f"{'='*60}")
            
            result = await self.agent.ainvoke(
                {"messages": input_messages},
                config={"callbacks": [self.callback_handler]}
            )
            
            # Extract the final message
            messages = result.get("messages", [])
            if messages:
                final_message = messages[-1]
                response = final_message.content if hasattr(final_message, 'content') else str(final_message)
                logger.info("✅ Agent processing completed successfully")
                
                print(f"\n🎯 FINAL AGENT RESPONSE:")
                print(f"📝 Response: {response}")
                print(f"{'='*60}")
                
                return response
            else:
                return "❌ No response from agent"
                
        except Exception as e:
            error_msg = f"Error processing query with agent: {str(e)}"
            logger.error(error_msg)
            print(f"\n❌ AGENT ERROR: {error_msg}")
            return error_msg

    async def connect_to_server(self, server_script_path: str):
        """Connect to the League MCP server and initialize the LangChain agent

        Args:
            server_script_path: Path to the League server script
        """
        logger.info(f"Connecting to League MCP server: {server_script_path}")
        
        # Convert to absolute path
        server_path = Path(server_script_path).resolve()
        if not server_path.exists():
            raise FileNotFoundError(f"Server script not found: {server_path}")
        
        is_python = server_script_path.endswith('.py')
        if not is_python:
            raise ValueError("Server script must be a .py file")

        # Create MCP client configuration
        logger.info("Setting up MCP client with langchain-mcp-adapters...")
        print(f"🔗 Setting up MCP connection to: {server_path}")
        
        self.mcp_client = MultiServerMCPClient(
            {
                "league": {
                    "command": "python",
                    "args": [str(server_path)],
                    "transport": "stdio",
                }
            }
        )
        
        # Get tools from MCP server
        logger.info("Getting tools from MCP server...")
        print("📡 Retrieving tools from MCP server...")
        
        self.tools = await self.mcp_client.get_tools()
        logger.info(f"✅ Retrieved {len(self.tools)} tools from MCP server")
        
        # Log all available tools with their schemas
        print(f"\n🛠️  AVAILABLE TOOLS ({len(self.tools)}):")
        for i, tool in enumerate(self.tools, 1):
            print(f"  {i}. {tool.name}")
            print(f"     Description: {tool.description}")
            if hasattr(tool, 'args_schema') and tool.args_schema:
                schema = tool.args_schema.schema() if hasattr(tool.args_schema, 'schema') else str(tool.args_schema)
                print(f"     Schema: {schema}")
            print()
        
        # Create the ReAct agent
        logger.info("Creating LangChain ReAct agent with Google Gemini...")
        
        system_prompt = """You are a League of Legends AI assistant with access to Riot Games API tools through MCP (Model Context Protocol).

CRITICAL: You MUST use the provided tools to get real data. NEVER generate code snippets, fake data, or example responses.

Available Tools:

ACCOUNT TOOLS:
- get_account_by_riot_id(game_name, tag_line, region="americas") - Look up account by Riot ID (e.g., game_name="Faker", tag_line="T1")
- get_account_by_puuid(puuid, region="americas") - Get account info by PUUID
- get_active_shard(game, puuid, region="americas") - Get active shard for games like VALORANT, Legends of Runeterra
- get_active_region(game, puuid, region="americas") - Get active region for LoL/TFT

MATCH TOOLS:
- get_match_ids_by_puuid(puuid, start_time=None, end_time=None, queue=None, match_type=None, start=0, count=20, region="na1") - Get match IDs for a player
- get_match_details(match_id, region="na1") - Get detailed match information
- get_match_timeline(match_id, region="na1") - Get match timeline

SUMMONER TOOLS:
- get_summoner_by_puuid(puuid, region="na1") - Get summoner info by PUUID
- get_summoner_by_name(name, region="na1") - Get summoner info by name

SPECTATOR TOOLS:
- get_active_game(puuid, region="na1") - Get current game info
- get_featured_games(region="na1") - Get featured games

LEAGUE TOOLS:
- get_challenger_league(queue, region="na1") - Get challenger league
- get_grandmaster_league(queue, region="na1") - Get grandmaster league  
- get_master_league(queue, region="na1") - Get master league

IMPORTANT PARAMETERS:
- Routing regions: americas, asia, europe (for account tools)
- Platform regions: na1, euw1, eun1, kr, jp1, br1, la1, la2, oc1, tr1, ru (for game-specific tools)
- Games: lol (League of Legends), tft (Teamfight Tactics), val (VALORANT), lor (Legends of Runeterra)

EXAMPLE WORKFLOW for "get puuid of Sneaky#NA1 then get match ids":
1. Call get_account_by_riot_id(game_name="Sneaky", tag_line="NA1", region="americas")
2. Extract the puuid from the result
3. Call get_match_ids_by_puuid(puuid=extracted_puuid, region="na1")

DO NOT generate Python code, print statements, or fake data. USE THE ACTUAL TOOLS."""

        self.agent = create_react_agent(
            model=self.model,
            tools=self.tools,
            prompt=system_prompt,
            debug=True  # Enable debug mode for more logging
        )
        
        logger.info("✅ LangChain ReAct agent created successfully with Google Gemini")

        # List available tools
        tool_names = [tool.name for tool in self.tools]
        logger.info(f"Connected with {len(self.tools)} available tools: {tool_names}")
        
        print(f"\n🎮 Connected to League MCP Server!")
        print(f"🛠️  Available League API tools: {tool_names}")
        print(f"🤖 Using LangChain ReAct Agent with Google Gemini ({self.model.model})")
        print(f"🔍 Debug mode enabled - tool calls will be logged")
        print("\n💡 Example queries:")
        print("- 'look up Faker T1'")
        print("- 'get account for PUUID [your-puuid]'")
        print("- 'what region is [puuid] playing LoL in?'")
        print("- 'get VALORANT shard for [puuid]'")

    async def chat_loop(self):
        """Run an interactive chat loop for League queries"""
        print("\n🚀 League MCP Client Started!")
        print("🎯 Ask about League accounts, player info, or Riot IDs.")
        print("💬 Type 'quit' to exit.\n")

        while True:
            try:
                query = input("🎮 League Query: ").strip()

                if query.lower() == 'quit':
                    logger.info("User requested to quit")
                    break

                if not query:
                    continue

                logger.info(f"New user query received: {query}")
                response = await self.process_query(query)
                print(f"\n📊 Final Result:\n{response}\n")
                print(f"{'='*80}\n")

            except KeyboardInterrupt:
                print("\n👋 Exiting...")
                logger.info("Received keyboard interrupt, exiting")
                break
            except Exception as e:
                error_msg = f"Error: {str(e)}"
                print(f"\n❌ {error_msg}")
                logger.error(error_msg)

    async def cleanup(self):
        """Clean up resources"""
        logger.info("Cleaning up resources...")
        if self.mcp_client:
            try:
                await self.mcp_client.close()
            except Exception as e:
                logger.warning(f"Error closing MCP client: {e}")


async def main():
    if len(sys.argv) < 2:
        print("Usage: python client.py <path_to_league_server_script>")
        print("Example: python client.py ../mcp-server/main.py")
        sys.exit(1)

    client = LeagueMCPClient()
    try:
        await client.connect_to_server(sys.argv[1])
        await client.chat_loop()
    finally:
        await client.cleanup()

if __name__ == "__main__":
    asyncio.run(main())