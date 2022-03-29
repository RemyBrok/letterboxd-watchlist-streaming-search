from flask import Flask, render_template, request

from Controllers import MainController

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

    return render_template('index.html', movies=MainController().yieldFilms(request.form['URL']))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)