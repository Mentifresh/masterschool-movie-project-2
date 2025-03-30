import random
from istorage import IStorage


class MovieApp:
    """
    Movie application class that provides a command-line interface 
    for managing a movie database.
    """
    
    def __init__(self, storage):
        """
        Initialize the movie application with a storage implementation.
        
        Args:
            storage (IStorage): An implementation of the IStorage interface.
        """
        self._storage = storage

    def _command_list_movies(self):
        """
        Lists all movies in the database.
        """
        movies = self._storage.list_movies()
        
        if not movies:
            print("No movies in the database.")
            return
            
        print("\nMovies in database:\n")
        for title, details in movies.items():
            print(f"{title} ({details['year']}): {details['rating']}")
        print("\n")

    def _command_add_movie(self):
        """
        Adds a new movie to the database.
        """
        title = input("Enter new movie name: ").strip()
        if not title:
            print("Error: Movie title cannot be empty.")
            return
            
        movies = self._storage.list_movies()
        if title in movies:
            print(f"Movie '{title}' already exists!")
            return

        try:
            year = int(input("Enter release year: "))
        except ValueError:
            print("Error: Invalid input for year.")
            return

        try:
            rating = float(input("Enter rating (0-10): "))
        except ValueError:
            print("Error: Invalid input for rating.")
            return

        if not 0 <= rating <= 10:
            print("Error: Rating must be between 0 and 10.")
            return

        self._storage.add_movie(title, year, rating)
        print(f"Movie '{title}' successfully added")

    def _command_delete_movie(self):
        """
        Deletes a movie from the database.
        """
        title = input("Enter movie name to delete: ").strip()
        if not title:
            print("Error: Movie title cannot be empty.")
            return
            
        movies = self._storage.list_movies()
        if title not in movies:
            print(f"Movie '{title}' does not exist.")
            return
            
        self._storage.delete_movie(title)
        print(f"Movie '{title}' deleted!")

    def _command_update_movie(self):
        """
        Updates the rating of an existing movie.
        """
        title = input("Enter movie name to update: ").strip()
        if not title:
            print("Error: Movie title cannot be empty.")
            return
            
        movies = self._storage.list_movies()
        if title not in movies:
            print(f"Movie '{title}' does not exist.")
            return

        try:
            rating = float(input("Enter new rating (0-10): "))
        except ValueError:
            print("Error: Invalid input for rating.")
            return

        if not 0 <= rating <= 10:
            print("Error: Rating must be between 0 and 10.")
            return

        self._storage.update_movie(title, rating)
        print(f"Movie '{title}' updated successfully!")

    def _command_movie_stats(self):
        """
        Displays statistics about movies in the database.
        """
        movies = self._storage.list_movies()
        if not movies:
            print("\nNo movies in the database.\n")
            return

        ratings = [details["rating"] for details in movies.values()]
        average = sum(ratings) / len(ratings)
        sorted_ratings = sorted(ratings)
        length = len(sorted_ratings)
        mid = length // 2
        median = (
            (sorted_ratings[mid - 1] + sorted_ratings[mid]) / 2
            if length % 2 == 0 else sorted_ratings[mid]
        )

        best_movie = max(movies.items(), key=lambda x: x[1]["rating"])
        worst_movie = min(movies.items(), key=lambda x: x[1]["rating"])

        print(f"\nAverage rating: {average:.2f}")
        print(f"Median rating: {median:.2f}")
        print(f"Best movie: {best_movie[0]} ({best_movie[1]['rating']})")
        print(f"Worst movie: {worst_movie[0]} ({worst_movie[1]['rating']})\n")

    def _command_random_movie(self):
        """
        Selects and displays a random movie from the database.
        """
        movies = self._storage.list_movies()
        if not movies:
            print("No movies in the database.")
            return
            
        title, details = random.choice(list(movies.items()))
        print(f"\nTonight you will watch: {title} ({details['year']}) - Rating: {details['rating']}\n")

    def _command_search_movies(self):
        """
        Searches for movies containing a user-input term.
        """
        movies = self._storage.list_movies()
        search_term = input("\nEnter search term: ").lower()
        found_movies = {title: details for title, details in movies.items()
                      if search_term in title.lower()}
                      
        if found_movies:
            print("\nFound movies:")
            for title, details in found_movies.items():
                print(f"{title} ({details['year']}): {details['rating']}")
            print("\n")
        else:
            print("\nNo movies found.\n")
            
    def _command_movies_by_rating(self):
        """
        Sorts movies by rating in descending order and displays them.
        """
        movies = self._storage.list_movies()

        if not movies:
            print("No movies in the database.")
            return

        movie_list = [(details["rating"], title) for title, details in movies.items()]
        movie_list.sort(key=lambda x: x[0], reverse=True)
        print("\nMovies sorted by rating (descending):")
        for rating, title in movie_list:
            print(f"{title}: {rating}")
        print("\n")

    def run(self):
        """
        Runs the movie application, displaying a menu and processing user commands.
        """
        while True:
            print("********** My Movies Database **********")
            print("\nMenu:")
            print("0. Exit")
            print("1. List movies")
            print("2. Add movie")
            print("3. Delete movie")
            print("4. Update movie")
            print("5. Stats")
            print("6. Random movie")
            print("7. Search movie")
            print("8. Movies sorted by rating")

            choice = input("Enter choice (0-8): ")

            if choice == '0':
                print("Bye!")
                break
            elif choice == '1':
                self._command_list_movies()
            elif choice == '2':
                self._command_add_movie()
            elif choice == '3':
                self._command_delete_movie()
            elif choice == '4':
                self._command_update_movie()
            elif choice == '5':
                self._command_movie_stats()
            elif choice == '6':
                self._command_random_movie()
            elif choice == '7':
                self._command_search_movies()
            elif choice == '8':
                self._command_movies_by_rating()
            else:
                print("\nInvalid choice. Please try again.")