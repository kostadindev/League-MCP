import asyncio
import os
import sys
import logging
from typing import Optional
from pathlib import Path
import gradio as gr
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
    
    def __init__(self, status_queue: Optional[queue.Queue] = None):
        super().__init__()
        self.status_queue = status_queue
    
    def on_tool_start(self, serialized: dict, input_str: str, **kwargs) -> None:
        """Log when a tool starts executing"""
        tool_name = serialized.get("name", "Unknown")
        status_msg = f"🔧 **Tool Call:** {tool_name}\n📋 **Input:** {input_str}"
        
        if self.status_queue:
            self.status_queue.put(("tool_start", status_msg))
        
        logger.info(f"Tool started: {tool_name} with input: {input_str}")
    
    def on_tool_end(self, output: str, **kwargs) -> None:
        """Log when a tool finishes executing"""
        # Truncate output for display
        display_output = output[:500] + "..." if len(output) > 500 else output
        status_msg = f"✅ **Tool Result:**\n📤 {display_output}"
        
        if self.status_queue:
            self.status_queue.put(("tool_end", status_msg))
            
        logger.info(f"Tool completed with output: {output[:200]}...")
    
    def on_tool_error(self, error: Exception, **kwargs) -> None:
        """Log when a tool encounters an error"""
        status_msg = f"❌ **Tool Error:** {error}"
        
        if self.status_queue:
            self.status_queue.put(("tool_error", status_msg))
            
        logger.error(f"Tool error: {error}")

class LeagueMCPClient:
    def __init__(self):
        # Initialize client objects
        self.mcp_client: Optional[MultiServerMCPClient] = None
        self.agent = None
        self.tools = []
        self.is_connected = False
        self.status_queue = queue.Queue()
        
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
        self.callback_handler = ToolCallLogger(self.status_queue)
        
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
            
            # Signal that processing started
            self.status_queue.put(("processing_start", f"🤖 **Processing:** {query}"))
            
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
                
                # Signal that processing completed
                self.status_queue.put(("processing_end", "✅ **Processing completed**"))
                
                return response
            else:
                return "❌ No response from agent"
                
        except Exception as e:
            error_msg = f"Error processing query with agent: {str(e)}"
            logger.error(error_msg)
            self.status_queue.put(("error", f"❌ **Error:** {error_msg}"))
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

    def get_connection_status(self):
        """Get the current connection status and available tools"""
        if not self.is_connected:
            return "❌ **Not Connected** - Please connect to MCP server first"
        
        tool_names = [tool.name for tool in self.tools]
        return f"✅ **Connected** - {len(self.tools)} tools available: {', '.join(tool_names[:5])}{'...' if len(tool_names) > 5 else ''}"
    
    def _start_event_loop(self):
        """Start the event loop in a background thread"""
        def run_loop():
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            self.loop_ready.set()
            self.loop.run_forever()
        
        self.loop_thread = threading.Thread(target=run_loop, daemon=True)
        self.loop_thread.start()
        self.loop_ready.wait()  # Wait for loop to be ready
    
    def _run_in_loop(self, coro):
        """Run a coroutine in the background event loop"""
        if not self.loop:
            raise RuntimeError("Event loop not started")
        
        future = asyncio.run_coroutine_threadsafe(coro, self.loop)
        return future.result()
    
    def chat_response(self, message, history):
        """Process chat message and return response (sync wrapper for async)"""
        if not message.strip():
            return history, ""
        
        if not self.is_connected:
            response = "❌ Not connected to MCP server. Please check connection."
            history.append({"role": "user", "content": message})
            history.append({"role": "assistant", "content": response})
            return history, ""
        
        try:
            # Run in the persistent event loop
            response = self._run_in_loop(self.process_query(message))
            history.append({"role": "user", "content": message})
            history.append({"role": "assistant", "content": response})
        except Exception as e:
            error_msg = f"Error processing query: {str(e)}"
            logger.error(error_msg)
            history.append({"role": "user", "content": message})
            history.append({"role": "assistant", "content": f"❌ {error_msg}"})
        
        return history, ""
    
    def get_status_updates(self):
        """Get status updates from the queue"""
        updates = []
        while not self.status_queue.empty():
            try:
                status_type, message = self.status_queue.get_nowait()
                updates.append(f"{message}")
            except queue.Empty:
                break
        return "\n\n".join(updates) if updates else ""

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
    
    with gr.Blocks(
        title="League of Legends MCP Client",
        theme=gr.themes.Soft(),
        css="""
        .gradio-container {
            max-width: 1200px !important;
        }
        .status-box {
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 0.5rem;
            padding: 1rem;
            margin: 0.5rem 0;
        }
        """
    ) as interface:
        
        gr.Markdown("""
        # 🎮 League of Legends MCP Client
        
        **AI-powered League of Legends assistant with access to Riot Games API**
        
        Ask about players, matches, rankings, and more using natural language!
        """)
        
        # Connection status
        with gr.Row():
            status_display = gr.Markdown(
                value=client.get_connection_status(),
                elem_classes=["status-box"]
            )
            refresh_btn = gr.Button("🔄 Refresh Status", size="sm")
        
        # Tool status updates
        tool_status = gr.Markdown(
            value="",
            label="🔧 Tool Activity",
            visible=False
        )
        
        # Main chat interface
        chatbot = gr.Chatbot(
            value=[],
            label="💬 Chat with League Assistant",
            height=500,
            show_label=True,
            type="messages"
        )
        
        msg = gr.Textbox(
            placeholder="Ask about League players, matches, rankings... (e.g., 'look up Faker T1')",
            label="🎯 Your Question",
            lines=2
        )
        
        with gr.Row():
            submit_btn = gr.Button("🚀 Send", variant="primary", size="lg")
            clear_btn = gr.Button("🗑️ Clear Chat", variant="secondary")
        
        # Example queries
        gr.Markdown("""
        ### 💡 Example Queries
        
        **Player Information:**
        - "Look up Faker T1"
        - "Get account info for Doublelift NA1"
        - "What region is [PUUID] playing in?"
        
        **Match Data:**
        - "Get recent matches for [PUUID]"
        - "Show match details for [match-id]"
        - "Get match timeline for [match-id]"
        
        **Rankings:**
        - "Show challenger league for ranked solo queue"
        - "Get grandmaster players in Korea"
        - "Display master tier in EUW"
        
        **Live Games:**
        - "Is [PUUID] currently in a game?"
        - "Show featured games in NA"
        """)
        
        # Event handlers
        def submit_message(message, history):
            history, _ = client.chat_response(message, history)
            return history, ""
        
        def clear_chat():
            return []
        
        def update_status():
            return client.get_connection_status()
        
        def update_tool_status():
            updates = client.get_status_updates()
            if updates:
                return gr.update(value=updates, visible=True)
            return gr.update(visible=False)
        
        # Set up interactions
        msg.submit(submit_message, [msg, chatbot], [chatbot, msg])
        submit_btn.click(submit_message, [msg, chatbot], [chatbot, msg])
        clear_btn.click(clear_chat, outputs=[chatbot])
        refresh_btn.click(update_status, outputs=[status_display])
        
        # Note: Auto-refresh removed due to compatibility issues
        # Use the refresh button to update status manually
    
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