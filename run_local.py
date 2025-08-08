#!/usr/bin/env python3
"""
Local development server for HackRx API
Run this script to start the FastAPI server locally
"""

import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    # Run the FastAPI app
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",  # Allow external connections
        port=8001,       # Default port
        reload=True,     # Auto-reload on code changes
        log_level="info"
    ) 