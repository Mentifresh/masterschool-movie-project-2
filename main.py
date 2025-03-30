#!/usr/bin/env python3
"""
Main entry point for the Movie Database Application.
"""
from storage_json import StorageJson
from movie_app import MovieApp


def main():
    """
    Main function that initializes the movie application with JSON storage and runs it.
    """
    # Initialize storage with JSON file path
    storage = StorageJson("data.json")
    
    # Create and run the movie application
    movie_app = MovieApp(storage)
    movie_app.run()


if __name__ == "__main__":
    main()
