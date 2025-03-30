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
        self._file_path = file_path
        # Ensure the file exists with headers
        if not os.path.exists(self._file_path):
            with open(self._file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["title", "year", "rating"])

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
                    movies[title] = {
                        'year': int(row['year']),
                        'rating': float(row['rating'])
                    }
            return movies
        except (FileNotFoundError, csv.Error):
            return {}

    def add_movie(self, title, year, rating):
        """
        Adds a movie to the CSV file.
        
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
            writer = csv.writer(file)
            writer.writerow(["title", "year", "rating"])
            for title, details in movies.items():
                writer.writerow([title, details["year"], details["rating"]]) 