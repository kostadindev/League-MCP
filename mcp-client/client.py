import asyncio
import os
import sys
import logging
from typing import Optional, Generator, List
from pathlib import Path
import gradio as gr
from gradio import ChatMessage
import threading
import queue

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
    
    def __init__(self, message_queue: Optional[queue.Queue] = None):
        super().__init__()
        self.message_queue = message_queue
    
    def on_tool_start(self, serialized: dict, input_str: str, **kwargs) -> None:
        """Log when a tool starts executing"""
        tool_name = serialized.get("name", "Unknown")
        
        if self.message_queue:
            self.message_queue.put(("tool_start", tool_name, input_str))
        
        logger.info(f"Tool started: {tool_name} with input: {input_str}")
    
    def on_tool_end(self, output: str, **kwargs) -> None:
        """Log when a tool finishes executing"""
        if self.message_queue:
            self.message_queue.put(("tool_end", output))
            
        logger.info(f"Tool completed with output: {output[:200]}...")
    
    def on_tool_error(self, error: Exception, **kwargs) -> None:
        """Log when a tool encounters an error"""
        if self.message_queue:
            self.message_queue.put(("tool_error", str(error)))
            
        logger.error(f"Tool error: {error}")

class LeagueMCPClient:
    def __init__(self):
        # Initialize client objects
        self.mcp_client: Optional[MultiServerMCPClient] = None
        self.agent = None
        self.tools = []
        self.is_connected = False
        self.message_queue = queue.Queue()
        
        # Event loop management
        self.loop = None
        self.loop_thread = None
        self.loop_ready = threading.Event()
        
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
        self.callback_handler = ToolCallLogger(self.message_queue)
        
        logger.info("LeagueMCPClient initialized with LangChain and Google Gemini")
    
    async def process_query_async(self, query: str) -> str:
        """Process a League-related query using LangChain ReAct agent with Gemini"""
        logger.info(f"Processing user query: {query}")
        
        if not self.agent:
            return "❌ Agent not initialized. Please connect to the MCP server first."
        
        try:
            # Create the input for the agent
            input_messages = [HumanMessage(content=query)]
            
            # Run the agent with callback for tool logging
            logger.info("Running LangChain ReAct agent with Google Gemini...")
            
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
                return response
            else:
                return "❌ No response from agent"
                
        except Exception as e:
            error_msg = f"Error processing query with agent: {str(e)}"
            logger.error(error_msg)
            return error_msg

    def _start_event_loop(self):
        """Start the event loop in a background thread"""
        def run_loop():
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            self.loop_ready.set()
            self.loop.run_forever()
        
        self.loop_thread = threading.Thread(target=run_loop, daemon=True)
        self.loop_thread.start()
        self.loop_ready.wait()  # Wait for the loop to be ready
        logger.info("Background event loop started")

    def _run_in_loop(self, coro):
        """Run a coroutine in the background event loop"""
        if not self.loop:
            raise RuntimeError("Event loop not started")
        
        future = asyncio.run_coroutine_threadsafe(coro, self.loop)
        return future.result()

    async def connect_to_server(self, server_script_path: str):
        """Connect to the League MCP server and initialize the LangChain agent"""
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
        
        self.tools = await self.mcp_client.get_tools()
        logger.info(f"✅ Retrieved {len(self.tools)} tools from MCP server")
        
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
        
        self.is_connected = True

    def get_connection_status(self) -> str:
        """Get the current connection status and available tools"""
        if not self.is_connected:
            return "❌ **Not Connected** - Please connect to MCP server first"
        
        tool_names = [tool.name for tool in self.tools]
        return f"✅ **Connected** - {len(self.tools)} tools available: {', '.join(tool_names[:5])}{'...' if len(tool_names) > 5 else ''}"
    
    def generate_response(self, history: List[ChatMessage], query: str) -> Generator[List[ChatMessage], None, None]:
        """Generate response with tool call logging"""
        if not query.strip():
            return
        
        # Add user message
        history.append(ChatMessage(role="user", content=query))
        yield history
        
        if not self.is_connected:
            history.append(ChatMessage(
                role="assistant", 
                content="❌ Not connected to MCP server. Please check connection."
            ))
            yield history
            return
        
        # Add thinking message
        history.append(ChatMessage(
            role="assistant",
            content="Let me help you with that League of Legends query. I'll use the available tools to get the information you need."
        ))
        yield history
        
        try:
            # Clear the message queue
            while not self.message_queue.empty():
                try:
                    self.message_queue.get_nowait()
                except queue.Empty:
                    break
            
            # Process the query in the background
            def run_query():
                return self._run_in_loop(self.process_query_async(query))
            
            # Start processing
            import threading
            result_container = {"result": None, "error": None}
            
            def query_thread():
                try:
                    result_container["result"] = run_query()
                except Exception as e:
                    result_container["error"] = str(e)
            
            thread = threading.Thread(target=query_thread)
            thread.start()
            
            # Monitor for tool calls while processing
            current_tool = None
            while thread.is_alive():
                try:
                    # Check for tool messages
                    message_type, *args = self.message_queue.get(timeout=0.1)
                    
                    if message_type == "tool_start":
                        tool_name, input_str = args
                        current_tool = tool_name
                        # Truncate long inputs
                        display_input = input_str[:200] + "..." if len(input_str) > 200 else input_str
                        history.append(ChatMessage(
                            role="assistant",
                            content=f"Using {tool_name} tool with input: {display_input}",
                            metadata={"title": f"🔧 Calling tool '{tool_name}'"}
                        ))
                        yield history
                    
                    elif message_type == "tool_end":
                        output = args[0]
                        if current_tool:
                            # Truncate long outputs
                            display_output = output[:300] + "..." if len(output) > 300 else output
                            history.append(ChatMessage(
                                role="assistant",
                                content=f"Tool returned: {display_output}",
                                metadata={"title": f"🛠️ Used tool '{current_tool}'"}
                            ))
                            yield history
                            current_tool = None
                    
                    elif message_type == "tool_error":
                        error = args[0]
                        if current_tool:
                            history.append(ChatMessage(
                                role="assistant",
                                content=f"Tool error: {error}",
                                metadata={"title": f"💥 Error in tool '{current_tool}'"}
                            ))
                            yield history
                            current_tool = None
                
                except queue.Empty:
                    continue
                except Exception as e:
                    logger.error(f"Error processing tool message: {e}")
                    continue
            
            # Wait for the query to complete
            thread.join()
            
            # Add the final response
            if result_container["error"]:
                history.append(ChatMessage(
                    role="assistant",
                    content=f"❌ Error: {result_container['error']}"
                ))
            else:
                history.append(ChatMessage(
                    role="assistant",
                    content=result_container["result"]
                ))
            
            yield history
            
        except Exception as e:
            error_msg = f"Error processing query: {str(e)}"
            logger.error(error_msg)
            history.append(ChatMessage(
                role="assistant",
                content=f"❌ {error_msg}"
            ))
            yield history

    async def cleanup(self):
        """Clean up resources"""
        logger.info("Cleaning up resources...")
        if self.mcp_client:
            try:
                # MultiServerMCPClient doesn't have a close method, so we'll just clean up references
                self.mcp_client = None
                logger.info("MCP client cleaned up successfully")
            except Exception as e:
                logger.warning(f"Error cleaning up MCP client: {e}")
        
        # Stop the event loop
        if self.loop:
            self.loop.call_soon_threadsafe(self.loop.stop)
            if self.loop_thread:
                self.loop_thread.join(timeout=5)
            logger.info("Event loop cleaned up successfully")


def create_gradio_interface(client: LeagueMCPClient):
    """Create and configure the Gradio interface"""
    
    def respond(history, message):
        """Handle user input and generate response"""
        if not message.strip():
            return history, ""
        
        # Use the client's generator to create responses
        for updated_history in client.generate_response(history, message):
            yield updated_history, ""
    
    def like_handler(evt: gr.LikeData):
        """Handle like/dislike events"""
        logger.info(f"User {'liked' if evt.liked else 'disliked'} message at index {evt.index}")
        print(f"Feedback: {evt.index}, {evt.liked}, {evt.value}")
    
    with gr.Blocks(
        title="League of Legends MCP Client",
        theme=gr.themes.Soft()
    ) as interface:
        
        with gr.Row():
            # Left column - Instructions and status
            with gr.Column(scale=1, min_width=300):
                gr.Markdown("""
                # 🎮 League of Legends MCP Client
                
                **AI-powered League of Legends assistant with access to Riot Games API**
                
                Ask about players, matches, rankings, and more using natural language!
                
                ### 💡 Example Queries:
                - "Look up Faker T1"
                - "Get recent matches for Doublelift NA1"  
                - "Show challenger league for ranked solo queue"
                - "Is there a featured game in NA?"
                """)
                
                # Connection status
                gr.Markdown(f"**Status:** {client.get_connection_status()}")
            
            # Right column - Chat interface
            with gr.Column(scale=2):
                # Main chat interface
                chatbot = gr.Chatbot(
                    type="messages", 
                    height=600, 
                    show_copy_button=True,
                    placeholder="Start chatting with the League assistant..."
                )
                
                msg = gr.Textbox(
                    placeholder="Ask about League players, matches, rankings... (e.g., 'look up Faker T1')",
                    label="Your Question",
                    lines=2
                )
                
                with gr.Row():
                    submit_btn = gr.Button("🚀 Send", variant="primary")
                    clear_btn = gr.Button("🗑️ Clear", variant="secondary")
        
        # Event handlers
        msg.submit(respond, [chatbot, msg], [chatbot, msg])
        submit_btn.click(respond, [chatbot, msg], [chatbot, msg])
        clear_btn.click(lambda: [], outputs=[chatbot])
        chatbot.like(like_handler)
    
    return interface

def main():
    if len(sys.argv) < 2:
        print("Usage: python client.py <path_to_league_server_script>")
        print("Example: python client.py ../mcp-server/main.py")
        sys.exit(1)

    print("🚀 Initializing League MCP Client...")
    client = LeagueMCPClient()
    
    try:
        # Start the persistent event loop
        print("🔧 Starting event loop...")
        client._start_event_loop()
        
        print("🔗 Connecting to MCP server...")
        client._run_in_loop(client.connect_to_server(sys.argv[1]))
        print("✅ Connected successfully!")
        
        # Create and launch Gradio interface
        print("🌐 Launching Gradio interface...")
        interface = create_gradio_interface(client)
        
        # Launch the interface
        interface.launch(
            server_name="127.0.0.1",
            server_port=7860,
            share=False,
            inbrowser=True,
            show_error=True
        )
        
    except Exception as e:
        print(f"❌ Error: {e}")
        logger.error(f"Startup error: {e}")
    finally:
        asyncio.run(client.cleanup())

if __name__ == "__main__":
    main()