from abc import ABC, abstractmethod


class IStorage(ABC):
    """
    Abstract interface for storage operations for a movie database.
    Defines methods for listing, adding, deleting, and updating movies.
    """
    
    @abstractmethod
    def list_movies(self):
        """
        Returns a dictionary of all movies.
        
        Returns:
            dict: A dictionary of movie information where the keys are movie titles
                 and the values are dictionaries containing movie details.
        """
        pass

    @abstractmethod
    def add_movie(self, title, year, rating):
        """
        Adds a movie to the storage.
        
        Args:
            title (str): The title of the movie.
            year (int): The release year of the movie.
            rating (float): The rating of the movie.
        """
        pass

    @abstractmethod
    def delete_movie(self, title):
        """
        Deletes a movie from the storage.
        
        Args:
            title (str): The title of the movie to delete.
        """
        pass

    @abstractmethod
    def update_movie(self, title, rating):
        """
        Updates a movie's rating in the storage.
        
        Args:
            title (str): The title of the movie to update.
            rating (float): The new rating of the movie.
        """
        pass
