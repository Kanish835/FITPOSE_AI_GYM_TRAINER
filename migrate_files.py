"""
Migration script to move files from the old structure to the new one.
This script helps organize the project according to the new structure.
"""

import os
import shutil
import sys

def create_directory_if_not_exists(directory):
    """Create a directory if it doesn't exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")

def migrate_files():
    """Migrate files from the old structure to the new one."""
    # Get the base directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define source and destination directories
    sources = {
        'templates': os.path.join(base_dir, 'templates'),
        'static': os.path.join(base_dir, 'static'),
        'images': os.path.join(base_dir, 'images'),
        'gifs': os.path.join(base_dir, 'gifs'),
        'exercise': os.path.join(base_dir, 'exercise'),
    }
    
    destinations = {
        'templates': os.path.join(base_dir, 'app', 'frontend', 'templates'),
        'static': os.path.join(base_dir, 'app', 'frontend', 'static'),
        'images': os.path.join(base_dir, 'app', 'frontend', 'static', 'images'),
        'gifs': os.path.join(base_dir, 'app', 'frontend', 'static', 'gifs'),
        'exercise': os.path.join(base_dir, 'app', 'backend', 'exercise_modules'),
    }
    
    # Create destination directories
    for dest in destinations.values():
        create_directory_if_not_exists(dest)
    
    # Copy files
    for key, source in sources.items():
        if os.path.exists(source):
            destination = destinations[key]
            
            # Copy all files from source to destination
            for item in os.listdir(source):
                source_item = os.path.join(source, item)
                dest_item = os.path.join(destination, item)
                
                if os.path.isfile(source_item):
                    shutil.copy2(source_item, dest_item)
                    print(f"Copied file: {source_item} -> {dest_item}")
                elif os.path.isdir(source_item):
                    if not os.path.exists(dest_item):
                        shutil.copytree(source_item, dest_item)
                        print(f"Copied directory: {source_item} -> {dest_item}")
    
    print("\nMigration completed successfully!")
    print("Please review the files in the new structure to ensure everything was copied correctly.")
    print("After verifying, you can delete the old files if they're no longer needed.")

if __name__ == "__main__":
    # Ask for confirmation before proceeding
    confirm = input("This will migrate files from the old structure to the new one. Continue? (y/n): ")
    
    if confirm.lower() == 'y':
        migrate_files()
    else:
        print("Migration cancelled.")
        sys.exit(0)