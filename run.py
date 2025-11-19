#!/usr/bin/env python3
import os
import sys
import argparse

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.app import create_app
from src.core.streaming.streaming import streamer

def run_flask():
    """Run the Flask application"""
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    # Run with SocketIO for real-time streaming support
    streamer.socketio.run(app, host='0.0.0.0', port=port, debug=False)

def run_streamlit():
    """Run the Streamlit dashboard"""
    import subprocess
    import sys
    
    # Run the Streamlit dashboard
    subprocess.run([
        sys.executable, "run_streamlit.py"
    ])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run Urban Mobility Analytics')
    parser.add_argument('--mode', choices=['flask', 'streamlit'], default='flask',
                        help='Run mode: flask (default) or streamlit')
    
    args = parser.parse_args()
    
    if args.mode == 'streamlit':
        run_streamlit()
    else:
        run_flask()