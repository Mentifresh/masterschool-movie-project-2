import random
import requests
import os
import datetime
from dotenv import load_dotenv
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
        # Load environment variables from .env file
        load_dotenv()
        self._api_key = os.getenv('API_KEY')

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
        Adds a new movie to the database by fetching information from OMDb API.
        User only needs to enter the movie title.
        """
        title = input("Enter new movie name: ").strip()
        if not title:
            print("Error: Movie title cannot be empty.")
            return
            
        movies = self._storage.list_movies()
        if title in movies:
            print(f"Movie '{title}' already exists!")
            return

        # Fetch movie information from OMDb API
        try:
            movie_data = self._fetch_movie_from_api(title)
            
            if not movie_data:
                print(f"Movie '{title}' not found in OMDb database.")
                return
                
            # Extract movie details from API response
            api_title = movie_data.get('Title', title)
            
            # Handle the year data - it might be just a year or have additional info
            year_str = movie_data.get('Year', '0')
            # Extract just the digits from the beginning
            year = 0
            for i in range(len(year_str)):
                if year_str[i].isdigit():
                    year = int(year_str[0:i+1])
                else:
                    break
            if year == 0:
                year = 2000  # Default value if year can't be parsed
            
            # Handle the rating
            imdb_rating = movie_data.get('imdbRating', 'N/A')
            rating = 0.0
            if imdb_rating != 'N/A':
                try:
                    rating = float(imdb_rating)
                except ValueError:
                    # If we can't convert to float, use default
                    rating = 0.0
            
            # Get poster URL
            poster = None
            if 'Poster' in movie_data and movie_data['Poster'] != 'N/A':
                poster = movie_data['Poster']
            
            # Add movie to storage
            self._storage.add_movie(api_title, year, rating, poster)
            print(f"Movie '{api_title}' successfully added with data from OMDb API.")
            
        except requests.exceptions.ConnectionError:
            print("Error: Could not connect to OMDb API. Please check your internet connection.")
        except requests.exceptions.Timeout:
            print("Error: Request to OMDb API timed out. Please try again later.")
        except requests.exceptions.RequestException as e:
            print(f"Error: An error occurred when accessing OMDb API: {str(e)}")
        except Exception as e:
            print(f"Error: An unexpected error occurred: {str(e)}")
            # Print more detailed debug information
            import traceback
            traceback.print_exc()

    def _fetch_movie_from_api(self, title):
        """
        Fetches movie information from OMDb API.
        
        Args:
            title (str): The title of the movie to search for.
            
        Returns:
            dict: Movie data if found, None otherwise.
        
        Raises:
            requests.exceptions.RequestException: If an error occurs during the API request.
        """
        if not self._api_key:
            raise ValueError("API key is missing. Please check your .env file.")
            
        # URL encode the movie title to handle spaces and special characters
        encoded_title = requests.utils.quote(title)
        url = f"http://www.omdbapi.com/?apikey={self._api_key}&t={encoded_title}"
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise exception for HTTP errors
        
        data = response.json()
        
        if data.get('Response') == 'False':
            return None
            
        return data

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
        
        # Show poster URL if available
        if 'poster' in details and details['poster']:
            print(f"Poster: {details['poster']}\n")

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
                if 'poster' in details and details['poster']:
                    print(f"Poster: {details['poster']}")
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
        
    def _command_generate_website(self):
        """
        Generates an HTML website to display the movie collection.
        """
        movies = self._storage.list_movies()
        
        if not movies:
            print("No movies in the database. Website not generated.")
            return
            
        try:
            # Read the template files
            with open("index-template.html", "r") as f:
                template = f.read()
                
            with open("movie-card-template.html", "r") as f:
                movie_card_template = f.read()
                
            # Generate movie grid HTML
            movie_grid = ""
            for title, details in movies.items():
                # Create a copy of the movie card template for each movie
                movie_card = movie_card_template
                
                # Replace placeholders with actual movie data
                movie_card = movie_card.replace("__TEMPLATE_MOVIE_TITLE__", title)
                movie_card = movie_card.replace("__TEMPLATE_MOVIE_YEAR__", str(details['year']))
                movie_card = movie_card.replace("__TEMPLATE_MOVIE_RATING__", f"{details['rating']:.1f}/10")
                
                # Handle poster image
                if 'poster' in details and details['poster']:
                    poster_html = f'<img src="{details["poster"]}" alt="{title}" class="object-cover w-full h-full">'
                else:
                    poster_html = '<div class="flex items-center justify-center h-full text-gray-400">No poster available</div>'
                
                movie_card = movie_card.replace("__TEMPLATE_MOVIE_POSTER__", poster_html)
                
                # Add the movie card to the grid
                movie_grid += movie_card
                
            # Replace placeholders in the main template
            current_year = datetime.datetime.now().year
            html_content = template.replace("__TEMPLATE_TITLE__", "My Movie Collection")
            html_content = html_content.replace("__TEMPLATE_MOVIE_GRID__", movie_grid)
            html_content = html_content.replace("__TEMPLATE_YEAR__", str(current_year))
            
            # Write the final HTML to a file
            output_file = "index.html"
            with open(output_file, "w") as f:
                f.write(html_content)
            
            # Get the absolute path to the HTML file to display to the user
            abs_path = os.path.abspath(output_file)
            
            print("\nWebsite generated successfully!")
            print(f"Your collection with {len(movies)} movies is now available at: {abs_path}")
            
            # Ask if the user wants to open the website in the browser
            if input("Would you like to open it in your browser? (y/n): ").lower() == 'y':
                try:
                    import webbrowser
                    webbrowser.open('file://' + abs_path)
                    print("Website opened in your browser.")
                except Exception as e:
                    print(f"Could not open browser: {str(e)}")
            
        except FileNotFoundError as e:
            print(f"Error: Template file not found. {str(e)}")
        except Exception as e:
            print(f"Error generating website: {str(e)}")
            import traceback
            traceback.print_exc()

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
            print("9. Generate website")

            choice = input("Enter choice (0-9): ")

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
            elif choice == '9':
                self._command_generate_website()
            else:
                print("\nInvalid choice. Please try again.")