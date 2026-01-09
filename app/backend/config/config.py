"""
Configuration settings for the Smart AI Gym Trainer application.
"""

import os

# Base directory of the application
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Configuration dictionary
CONFIG = {
    "SERVER": {
        "HOST": "127.0.0.1",
        "PORT": 5000,
        "DEBUG": True,
        "THREADED": True
    },
    
    "CAMERA": {
        "RESOLUTION": {
            "WIDTH": 640,
            "HEIGHT": 480
        },
        "FPS": 30
    },
    
    "EXERCISE": {
        "VALID_TYPES": [
            "lateral-rise", 
            "alt-dumbbell-curls", 
            "barbell-row", 
            "push-up", 
            "squats", 
            "shoulder-press", 
            "tricep-dips"
        ]
    }
}

def get_config(section=None, key=None):
    """
    Get configuration values.
    
    Args:
        section (str, optional): Configuration section name
        key (str, optional): Key within the section
        
    Returns:
        The requested configuration value or the entire config if no specific value requested
    """
    if section is None:
        return CONFIG
    
    if key is None:
        return CONFIG.get(section, {})
        
    return CONFIG.get(section, {}).get(key, None)