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

        year = None

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

        # Loop through results if we have a year
        if year:
            for result in results:
                # Same year: so we go ahead and assume it's this release
                if result['release_date'][0:4] == year:
                    return result
        elif len(results) > 0:
            # If we don't have a year we get the first result and hope for the best
            return results[0]

        # Nothing found
        return None

    def getWatchProviders(self, movie: dict, country = 'NL') :
        "Get watch providers. Provided by JustWatch.com"
        
        # Send request to MovieDatabase
        response = curl.get(f"https://api.themoviedb.org/3/movie/{movie['id']}/watch/providers?api_key={config.TheMovieDatabase['apikey']}")

        # Retrieve results
        results = response.json().get('results')

        # Check if country is in the results
        if country in results:
            # Check if there is a flatrate streaming service
            if "flatrate" in results[country]:
                return results[country]['flatrate']

        return None

    def validYear(self, year) -> bool:
        """Checks if its a valid year"""
        try:
            if int(year) >= 1888 and int(year) <= (self.today.year + 2):
                return True
            else:
                return False
        except:
            return False
