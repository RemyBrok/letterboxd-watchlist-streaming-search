from flask import Flask, render_template, request
import requests as curl
from bs4 import BeautifulSoup, SoupStrainer
from MovieDatabase import TMDB

app = Flask(__name__)
app.config.update(
    DEBUG=True,
    TEMPLATES_AUTO_RELOAD=True
)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def process():
    # If there is nothing filled in
    if not request.form['URL']:
        return render_template('index.html')
    # If the url does not match letterboxd
    if(request.form['URL'][0:23] != 'https://letterboxd.com/' 
       and request.form['URL'][0:26] != 'https://www.letterboxd.com/'
       and request.form['URL'][0:18] != 'www.letterboxd.com/'):
        return render_template('index.html')


    response = curl.get(request.form['URL'])
    strainer = SoupStrainer('li', attrs={'class': 'poster-container'})
    soup = BeautifulSoup(response.text, 'html.parser', parse_only=strainer)

    MovieDatabase = TMDB()

    # Loop through soup
    for data in soup:
        film = data.find("div").get("data-film-slug")
        if film:
            # Trim the film
            film = MovieDatabase.getMovie(film[6:-1].replace('-', ' '))

            if film:
                providers = MovieDatabase.getWatchProviders(film)
                return providers

            return 'NOTHING FOUND'

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)