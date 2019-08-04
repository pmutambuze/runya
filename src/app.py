from flask import Flask, jsonify, render_template
from spellchecker import SpellChecker

luganda_checker = None
runyankole_checker = None

app = Flask(__name__)


def setup():
    global luganda_checker, runyankole_checker
    if not luganda_checker:
        luganda_checker = SpellChecker(language=None, case_sensitive=False)
        luganda_checker.word_frequency.load_dictionary('luganda.json')

    if not runyankole_checker:
        runyankole_checker = SpellChecker(language=None, case_sensitive=False)
        runyankole_checker.word_frequency.load_dictionary('runya.json')


@app.route("/suggest/luganda/<string:word>")
def suggestions_luganda(word):
    setup()
    candidates = luganda_checker.candidates(word)
    candidates = list(candidates)
    return jsonify(candidates)


@app.route("/suggest/runyankole/<string:word>")
def suggestions_runyankole(word):
    setup()
    candidates = runyankole_checker.candidates(word)
    candidates = list(candidates)
    return jsonify(candidates)


@app.route("/is-known/luganda/<string:word>")
def is_known_luganda(word):
    setup()
    return jsonify(len(luganda_checker.known([word.lower()])) > 0)


@app.route("/is-known/runyankole/<string:word>")
def is_known_runyankole(word):
    setup()
    return jsonify({'isKnown': len(runyankole_checker.known([word.lower()])) > 0})


@app.route('/')
def home():
    setup()
    return render_template("speller.html")


@app.route('/luganda')
def luganda():
    setup()
    return render_template("luganda.html")


@app.route('/runyankole')
def runyankole():
    setup()
    return render_template("runyankole.html")


if __name__ == '__main__':
    app.run(debug=True)
