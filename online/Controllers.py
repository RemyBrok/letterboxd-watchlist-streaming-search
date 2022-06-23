from MovieDatabase import TMDB
import requests as curl
from bs4 import BeautifulSoup, SoupStrainer

class MainController:
    def __init__(self):
        self.moviesStrainer = SoupStrainer('li', attrs={'class': 'poster-container'})
        self.paginationStrainer = SoupStrainer('li', attrs={'class': 'paginate-page'})
        self.MovieDatabase = TMDB()
        self.storage = []

    def yieldFilms(self, url, country, recursive = False):
        """Yield films with their providers"""
        # Get first request
        response = curl.get(url)

        # Return first batch
        soup = BeautifulSoup(response.text, 'html.parser', parse_only=self.moviesStrainer)
        # Loop through soup
        for data in soup:
            film = data.find("div").get("data-film-slug")
            if film:
                # Trim film and retrieve from Movie Database
                film = self.MovieDatabase.getMovie(film[6:-1].replace('-', ' '))

                if film:
                    providers = self.MovieDatabase.getWatchProviders(film, country)
                    if providers:
                        self.storage.append({
                            'name': film['original_title'],
                            'id': film['id'],
                            'providers': providers
                        })

        # Check if function is called recursive
        if not recursive:
            pagination = BeautifulSoup(response.text, 'html.parser', parse_only=self.paginationStrainer)
            totalPages = int(pagination.find_all('li')[-1].get_text())

            for i in range(2, totalPages):
                self.storage.append(
                    self.yieldFilms(
                        url = f"{url}/page/{i}", 
                        country = country, 
                        recursive = True
                    )
                )

        return self.storage

if __name__ == "__main__":
    main = MainController()
    main.yieldFilms('https://letterboxd.com/Holymoose/watchlist/')