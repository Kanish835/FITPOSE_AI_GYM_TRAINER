"""
Smart AI Gym Trainer - Main Entry Point
--------------------------------------
This script serves as the main entry point for running the Smart AI Gym Trainer application.
"""

from app.app import create_app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, threaded=True, host='127.0.0.1', port=5000)