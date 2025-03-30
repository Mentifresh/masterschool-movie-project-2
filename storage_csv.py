import csv
import os
from istorage import IStorage


class StorageCsv(IStorage):
    """
    Implementation of IStorage that stores movie data in a CSV file.
    """
    
    def __init__(self, file_path):
        """
        Initialize the CSV storage with a file path.
        
        Args:
            file_path (str): Path to the CSV file for storing movies data.
        """
        # Ensure data directory exists
        self._data_dir = os.path.join(os.path.dirname(__file__), "data")
        os.makedirs(self._data_dir, exist_ok=True)
        
        # Create full path to the CSV file in the data directory
        self._file_path = os.path.join(self._data_dir, file_path)
        
        # Ensure the file exists with headers
        if not os.path.exists(self._file_path):
            with open(self._file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["title", "year", "rating", "poster"])

    def list_movies(self):
        """
        Returns a dictionary of all movies from the CSV file.
        
        Returns:
            dict: A dictionary of movie information.
        """
        movies = {}
        try:
            with open(self._file_path, 'r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    title = row['title']
                    movie_data = {
                        'year': int(row['year']),
                        'rating': float(row['rating'])
                    }
                    if 'poster' in row and row['poster']:
                        movie_data['poster'] = row['poster']
                    movies[title] = movie_data
            return movies
        except (FileNotFoundError, csv.Error):
            return {}

    def add_movie(self, title, year, rating, poster=None):
        """
        Adds a movie to the CSV file.
        
        Args:
            title (str): The title of the movie.
            year (int): The release year of the movie.
            rating (float): The rating of the movie.
            poster (str, optional): URL to the movie poster image.
        """
        movies = self.list_movies()
        movie_data = {"year": year, "rating": rating}
        if poster:
            movie_data["poster"] = poster
        movies[title] = movie_data
        self._save_movies(movies)

    def delete_movie(self, title):
        """
        Deletes a movie from the CSV file.
        
        Args:
            title (str): The title of the movie to delete.
        """
        movies = self.list_movies()
        if title in movies:
            del movies[title]
            self._save_movies(movies)

    def update_movie(self, title, rating):
        """
        Updates a movie's rating in the CSV file.
        
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
        Saves the movies dictionary to the CSV file.
        
        Args:
            movies (dict): A dictionary of movie information.
        """
        with open(self._file_path, 'w', newline='') as file:
            fieldnames = ["title", "year", "rating", "poster"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for title, details in movies.items():
                row = {
                    "title": title,
                    "year": details["year"],
                    "rating": details["rating"],
                    "poster": details.get("poster", "")
                }
                writer.writerow(row) 