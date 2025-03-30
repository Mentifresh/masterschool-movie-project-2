import json
from istorage import IStorage


class StorageJson(IStorage):
    """
    Implementation of IStorage that stores movie data in a JSON file.
    """
    
    def __init__(self, file_path):
        """
        Initialize the JSON storage with a file path.
        
        Args:
            file_path (str): Path to the JSON file for storing movies data.
        """
        self._file_path = file_path
        # Ensure the file exists with at least an empty JSON object
        try:
            with open(self._file_path, 'r') as file:
                json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            with open(self._file_path, 'w') as file:
                json.dump({}, file)

    def list_movies(self):
        """
        Returns a dictionary of all movies from the JSON file.
        
        Returns:
            dict: A dictionary of movie information.
        """
        try:
            with open(self._file_path, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def add_movie(self, title, year, rating):
        """
        Adds a movie to the JSON file.
        
        Args:
            title (str): The title of the movie.
            year (int): The release year of the movie.
            rating (float): The rating of the movie.
        """
        movies = self.list_movies()
        movies[title] = {"year": year, "rating": rating}
        self._save_movies(movies)

    def delete_movie(self, title):
        """
        Deletes a movie from the JSON file.
        
        Args:
            title (str): The title of the movie to delete.
        """
        movies = self.list_movies()
        if title in movies:
            del movies[title]
            self._save_movies(movies)

    def update_movie(self, title, rating):
        """
        Updates a movie's rating in the JSON file.
        
        Args:
            title (str): The title of the movie to update.
            rating (float): The new rating of the movie.
        """
        movies = self.list_movies()
        if title in movies:
            movies[title]["rating"] = rating
            self._save_movies(movies)

    def _save_movies(self, movies):
        """
        Saves the movies dictionary to the JSON file.
        
        Args:
            movies (dict): A dictionary of movie information.
        """
        with open(self._file_path, 'w') as file:
            json.dump(movies, file, indent=4)