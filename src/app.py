from flask import Flask, jsonify, render_template
from spellchecker import SpellChecker

luganda_checker = None
runyankole_checker = None
app = Flask(__name__)


@app.route("/suggest/luganda/<string:word>")
def suggestions_luganda(word):
    candidates = luganda_checker.candidates(word)
    candidates = list(candidates)
    return jsonify(candidates)


@app.route("/suggest/runyankole/<string:word>")
def suggestions_runyankole(word):
    candidates = runyankole_checker.candidates(word)
    candidates = list(candidates)
    return jsonify(candidates)


@app.route("/is-known/luganda/<string:word>")
def is_known_luganda(word):
    return jsonify(len(luganda_checker.known([word.lower()])) > 0)


@app.route("/is-known/runyankole/<string:word>")
def is_known_runyankole(word):
    return jsonify({'isKnown': len(runyankole_checker.known([word.lower()])) > 0})


@app.route('/')
def home():
    return render_template("speller.html")


@app.route('/luganda')
def luganda():
    return render_template("luganda.html")


@app.route('/runyankole')
def runyankole():
    return render_template("runyankole.html")


if __name__ == '__main__':
    luganda_checker = SpellChecker(language=None, case_sensitive=False)
    luganda_checker.word_frequency.load_dictionary('./data/luganda.json')

    runyankole_checker = SpellChecker(language=None, case_sensitive=False)
    runyankole_checker.word_frequency.load_dictionary('./data/runya.json')

    app.run(debug=True)
