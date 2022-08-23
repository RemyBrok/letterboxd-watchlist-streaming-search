from flask import Flask, render_template, request

from Controllers import MainController
import json
from config import DefaultCountry
from MovieDatabase import TMDB

app = Flask(__name__)
app.config.update(
    DEBUG=True,
    TEMPLATES_AUTO_RELOAD=True
)

@app.context_processor
def availableCountries():
    with open('data/countries.json', 'r') as file:
        return dict(countries=json.load(file), DefaultCountry=DefaultCountry, providers=TMDB.getProviders(DefaultCountry))

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def process():    
    # If there is nothing filled in
    if not request.form['URL']:
        return render_template('index.html', message="Nothing filled in")
    if not request.form.getlist('selectedProviders'):
        return render_template('index.html', message="No providers selected")
    # If the url does not match letterboxd
    if(request.form['URL'][0:23] != 'https://letterboxd.com/' 
       and request.form['URL'][0:26] != 'https://www.letterboxd.com/'
       and request.form['URL'][0:18] != 'www.letterboxd.com/'):
        return render_template('index.html', message = "Invalid input")

    return render_template('index.html', movies = MainController().yieldFilms(
            url = request.form['URL'], 
            country = request.form['country'], 
            selectedProviders = request.form.getlist('selectedProviders'),
        )
    )

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)