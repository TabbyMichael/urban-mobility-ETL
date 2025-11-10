#!/usr/bin/env python3
"""
Script to run the Streamlit dashboard for Urban Mobility Analytics
"""

import subprocess
import sys
import os

def main():
    """Run the Streamlit dashboard"""
    try:
        # Change to the project directory
        project_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(project_dir)
        
        # Run the Streamlit app
        subprocess.run([
            "streamlit", "run", 
            "src/dashboard/streamlit_app.py",
            "--server.port", "8503",
            "--server.address", "0.0.0.0"
        ], check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"Error running Streamlit dashboard: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("Streamlit dashboard stopped by user")
        sys.exit(0)

if __name__ == "__main__":
    main()