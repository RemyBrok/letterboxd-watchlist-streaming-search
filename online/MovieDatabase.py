import urllib.parse
import config
import requests as curl
from datetime import date

class TMDB:
    def __init__(self):
        self.today = date.today()
        self.baseURL = "https://api.themoviedb.org/3/"
    
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
        url = f"{self.baseURL}search/movie?api_key={config.TheMovieDatabase['apikey']}&query={filmURL}"

        # Search with TMDB
        response = curl.get(url)
        results = response.json().get('results')

        # Loop through results if we have a year
        if year:
            for result in results:
                # If we have a year but no year in the result we gonna return none for now (NEED WIP)
                if 'release_date' not in result:
                    return None
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
        response = curl.get(f"{self.baseURL}movie/{movie['id']}/watch/providers?api_key={config.TheMovieDatabase['apikey']}")

        # Retrieve results
        results = response.json().get('results')

        # Check if country is in the results
        if country in results:
            # Check if there is a flatrate streaming service
            if "flatrate" in results[country]:
                return results[country]['flatrate']

        return None

    def getProviders(country: str) -> dict :
        "Get all the providers available in a country"

        response = curl.get(f"https://api.themoviedb.org/3/watch/providers/tv?api_key={config.TheMovieDatabase['apikey']}&watch_region={country}")

        results = response.json().get('results')

        # Sometimes we get multiple watch provider names so we're gonna make it unique
        return list({v['provider_name']:v for v in results}.values())

    def validYear(self, year) -> bool:
        """Checks if its a valid year"""
        try:
            if int(year) >= 1888 and int(year) <= (self.today.year + 2):
                return True
            else:
                return False
        except:
            return False

if __name__ == "__main__":
    TMDB.getProviders('NL')
