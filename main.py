#!/usr/bin/env python3
"""
Main entry point for the Movie Database Application.
"""
import sys
from storage_json import StorageJson
from movie_app import MovieApp


def main():
    """
    Main function that initializes the movie application with JSON storage and runs it.
    """
    try:
        # Initialize storage with JSON file path
        storage = StorageJson("data.json")
        
        # Create and run the movie application
        movie_app = MovieApp(storage)
        movie_app.run()
    except KeyboardInterrupt:
        print("\nApplication terminated by user.")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
