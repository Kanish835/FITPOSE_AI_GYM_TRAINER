"""
Smart AI Gym Trainer - Main Application
---------------------------------------
This is the main entry point for the Smart AI Gym Trainer application.
It imports all necessary modules and initializes the Flask server.
"""

import os
from flask import Flask
from app.backend.api.routes import register_routes

def create_app():
    """Create and configure the Flask application"""
    
    # Create Flask app
    app = Flask(__name__, 
                template_folder='frontend/templates',
                static_folder='frontend/static')
    
    # Register all routes
    register_routes(app)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, threaded=True, host='127.0.0.1', port=5000)