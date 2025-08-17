#!/usr/bin/env python3
import streamlit.web.cli as stcli
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    sys.argv = [
        "streamlit",
        "run",
        "frontend/streamlit_app.py",
        "--server.port=12000",
        "--server.address=0.0.0.0",
        "--server.allowRunOnSave=true",
        "--server.enableCORS=true",
        "--server.enableXsrfProtection=false"
    ]
    sys.exit(stcli.main())