#!/usr/bin/env python3
import os
import sys

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.app import create_app
from src.streaming.streaming import streamer

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    # Run with SocketIO for real-time streaming support
    streamer.socketio.run(app, host='0.0.0.0', port=port, debug=False)