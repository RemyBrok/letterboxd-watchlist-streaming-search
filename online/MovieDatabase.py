import urllib.parse
import config
import requests as curl
from datetime import date

class TMDB:
    def __init__(self):
        self.today = date.today()
        pass
    
    def getMovie(self, movie: str) -> dict:
        """Retrieves the right movie from The Movie Database"""

        # If there is a year at the end of the movie we chop it off and use it later for the response from TMDB
        if self.validYear(movie[-4:]):
            year = movie[-4:]
            movie = movie[0:-4]

        # Proper encode the URL
        filmURL = urllib.parse.quote_plus(movie)

        # Search the movie 
        url = f"https://api.themoviedb.org/3/search/movie?api_key={config.TheMovieDatabase['apikey']}&query={filmURL}"

        # Search with TMDB
        response = curl.get(url)
        results = response.json().get('results')

        # If we only have 1 result we return that result
        if len(results) == 1:
            return results[0]

        # Loop through results if we have a year
        if year:
            for result in results:
                # Same year so we go ahead and assume it's this release
                if result['release_date'][0:4] == year:
                    return result

        # Nothing found
        return None

    def getWatchProviders(self, movie: dict) :
        "Get watch providers. Provided by JustWatch.com"

        url = f"https://api.themoviedb.org/3/movie/{movie['id']}/watch/providers?api_key={config.TheMovieDatabase['apikey']}"

        response = curl.get(url)

        return response.json().get('results')['NL']

    def validYear(self, year) -> bool:
        """Checks if its a valid year"""
        if int(year) >= 1888 and int(year) <= (self.today.year + 2):
            return True
        else:
            return False
