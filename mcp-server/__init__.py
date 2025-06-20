"""
League MCP - Model Context Protocol server for League of Legends data.

This package provides access to League of Legends game data through the Riot Games API
via the Model Context Protocol (MCP). It supports multiple transport types for 
different integration scenarios.
"""

__version__ = "0.1.1"
__author__ = "League MCP Contributors"
__description__ = "Model Context Protocol server for League of Legends game data via Riot Games API"

from .main import main

__all__ = ["main"] 