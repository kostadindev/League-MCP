import asyncio
import os
import json
import re
import logging
from typing import Optional
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class LeagueMCPClient:
    def __init__(self):
        # Initialize session and client objects
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        logger.info("LeagueMCPClient initialized")
    
    async def process_query(self, query: str) -> str:
        """Process a League-related query using Google Gemini and available MCP tools"""
        logger.info(f"Processing user query: {query}")
        try:
            # Get available tools from the MCP session
            if self.session:
                tools_response = await self.session.list_tools()
                tools_info = []
                for tool in tools_response.tools:
                    tool_desc = f"- {tool.name}: {tool.description}"
                    if hasattr(tool, 'inputSchema') and tool.inputSchema:
                        props = tool.inputSchema.get('properties', {})
                        params = [f"{name} ({info.get('type', 'any')})" for name, info in props.items()]
                        if params:
                            tool_desc += f" [Parameters: {', '.join(params)}]"
                    tools_info.append(tool_desc)
                tools_context = "Available League API tools:\n" + "\n".join(tools_info)
                logger.debug(f"Tools context prepared: {len(tools_response.tools)} tools available")
            else:
                tools_context = "No League MCP tools available."
                logger.warning("No MCP session available")
            
            # Create a League-specific prompt
            prompt = f"""You are a League of Legends AI assistant with access to Riot Games API tools. When a user asks about League accounts, player information, or Riot IDs, you should USE the tools to get actual results.

{tools_context}

User query: {query}

If this query can be answered using available League API tools:
1. Respond with: USE_TOOL: <tool_name>(<param1>=<value1>, <param2>=<value2>, ...)
2. Make sure parameter values are appropriate for the League API

Region options: americas, asia, europe (default: americas)
Game options for shards/regions: lol (League of Legends), tft (Teamfight Tactics), val (VALORANT), lor (Legends of Runeterra)

Examples:
- "look up Faker T1" -> USE_TOOL: get_account_by_riot_id(game_name="Faker", tag_line="T1")
- "get account for PUUID abc123..." -> USE_TOOL: get_account_by_puuid(puuid="abc123...")
- "what region is this player in for LoL: [puuid]" -> USE_TOOL: get_active_region(game="lol", puuid="[puuid]")
- "get active shard for VALORANT player [puuid]" -> USE_TOOL: get_active_shard(game="val", puuid="[puuid]")

If the query cannot be answered with available tools, provide helpful League-related information or suggest what the user might need to provide.
"""
            
            # Generate response using Gemini
            logger.info("Sending query to Gemini for processing...")
            response = await self.model.generate_content_async(prompt)
            response_text = response.text.strip()
            logger.info(f"Gemini response received: {response_text[:100]}...")
            
            # Check if Gemini wants to use a tool
            if response_text.startswith("USE_TOOL:"):
                logger.info("Gemini decided to use a tool")
                return await self._execute_tool_from_response(response_text)
            else:
                logger.info("Gemini provided a direct response (no tool usage)")
                return response_text
                
        except Exception as e:
            error_msg = f"Error processing query: {str(e)}"
            logger.error(error_msg)
            return error_msg

    async def _execute_tool_from_response(self, response: str) -> str:
        """Parse and execute a tool call from Gemini's response"""
        logger.info("Parsing and executing tool call from Gemini response")
        try:
            # Extract tool call from response like "USE_TOOL: get_account_by_riot_id(game_name="Faker", tag_line="T1")"
            tool_call = response.replace("USE_TOOL:", "").strip()
            logger.debug(f"Extracted tool call: {tool_call}")
            
            # Parse tool name and parameters
            match = re.match(r"(\w+)\((.*)\)", tool_call)
            if not match:
                error_msg = f"Could not parse tool call: {tool_call}"
                logger.error(error_msg)
                return error_msg
            
            tool_name = match.group(1)
            params_str = match.group(2)
            logger.info(f"Parsed tool name: {tool_name}")
            logger.debug(f"Raw parameters string: {params_str}")
            
            # Parse parameters with better handling for League API parameters
            arguments = {}
            if params_str:
                # Handle both key=value and key="value" formats
                param_pattern = r'(\w+)=([^,]+?)(?=,\s*\w+=|$)'
                matches = re.findall(param_pattern, params_str)
                
                for key, value in matches:
                    key = key.strip()
                    value = value.strip().strip('"\'')
                    # Convert to appropriate type
                    try:
                        if value.lower() in ['true', 'false']:
                            arguments[key] = value.lower() == 'true'
                        elif value.isdigit() or (value.startswith('-') and value[1:].isdigit()):
                            arguments[key] = int(value)
                        elif value.replace('.', '').replace('-', '').isdigit():
                            arguments[key] = float(value)
                        else:
                            arguments[key] = value
                    except:
                        arguments[key] = value
            
            logger.info(f"🎯 Calling League API tool: {tool_name}")
            logger.info(f"📋 Arguments: {arguments}")
            print(f"🔄 Executing: {tool_name}({', '.join([f'{k}={v}' for k, v in arguments.items()])})")
            
            # Execute the tool
            result = await self.session.call_tool(tool_name, arguments)
            
            if result.isError:
                error_msg = f"League API Error: {result.error}"
                logger.error(error_msg)
                return error_msg
            else:
                # Format the result nicely
                if hasattr(result, 'content') and result.content:
                    content_parts = []
                    for content in result.content:
                        if hasattr(content, 'text'):
                            content_parts.append(content.text)
                        elif hasattr(content, 'data'):
                            content_parts.append(str(content.data))
                    final_result = "\n".join(content_parts) if content_parts else str(result)
                else:
                    final_result = str(result)
                
                logger.info(f"✅ Tool execution completed successfully")
                logger.debug(f"Tool result: {final_result[:200]}...")
                return final_result
                    
        except Exception as e:
            error_msg = f"Error executing League API tool: {str(e)}"
            logger.error(error_msg)
            return error_msg

    async def connect_to_server(self, server_script_path: str):
        """Connect to the League MCP server

        Args:
            server_script_path: Path to the League server script
        """
        logger.info(f"Connecting to League MCP server: {server_script_path}")
        
        is_python = server_script_path.endswith('.py')
        is_js = server_script_path.endswith('.js')
        if not (is_python or is_js):
            raise ValueError("Server script must be a .py or .js file")

        command = "python" if is_python else "node"
        server_params = StdioServerParameters(
            command=command,
            args=[server_script_path],
            env=None
        )

        logger.info(f"Starting server with command: {command} {server_script_path}")
        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))

        await self.session.initialize()
        logger.info("MCP session initialized successfully")

        # List available tools
        response = await self.session.list_tools()
        tools = response.tools
        logger.info(f"Connected with {len(tools)} available tools: {[tool.name for tool in tools]}")
        
        print(f"\n🎮 Connected to League MCP Server!")
        print("🛠️  Available League API tools:", [tool.name for tool in tools])
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
                print(f"\n📊 Result:\n{response}\n")

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
        await self.exit_stack.aclose()


async def main():
    if len(sys.argv) < 2:
        print("Usage: python client.py <path_to_league_server_script>")
        print("Example: python client.py ../mcp-server/league.py")
        sys.exit(1)

    client = LeagueMCPClient()
    try:
        await client.connect_to_server(sys.argv[1])
        await client.chat_loop()
    finally:
        await client.cleanup()

if __name__ == "__main__":
    import sys
    asyncio.run(main())