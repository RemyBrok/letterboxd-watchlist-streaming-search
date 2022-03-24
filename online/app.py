from flask import Flask, render_template, request
import requests as curl
from bs4 import BeautifulSoup, SoupStrainer

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
    if not request.form['URL']:
        return render_template('index.html')
    if(request.form['URL'][0:23] != 'https://letterboxd.com/' 
       and request.form['URL'][0:26] != 'https://www.letterboxd.com/'
       and request.form['URL'][0:18] != 'www.letterboxd.com/'):
        return render_template('index.html')

    response = curl.get(request.form['URL'])
    strainer = SoupStrainer('li', attrs={'class': 'poster-container'})
    soup = BeautifulSoup(response.text, 'html.parser', parse_only=strainer)
    return f'<span>{list(soup)}</span>'

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)