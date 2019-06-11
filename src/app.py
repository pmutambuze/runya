from flask import Flask, jsonify, render_template
from spellchecker import SpellChecker

app = Flask(__name__)

luganda_checker = None
runya_checker = None


@app.route('/')
def home():
    return render_template("speller.html")

@app.route('/luganda')
def luganda():
    return render_template("luganda.html")

@app.route('/runyankole')
def runyankole():
    return render_template("runyankole.html")


@app.route("/suggest/luganda/<string:word>")
def suggestions_luganda(word):
    global luganda_checker

    luganda_checker = luganda_checker if luganda_checker else SpellChecker(language="", local_dictionary="luganda.json")
    candidates = luganda_checker.candidates(word)
    candidates = list(candidates)

    return jsonify(candidates)


@app.route("/suggest/runyankole/<string:word>")
def suggestions_runyankole(word):
    global runya_checker

    runya_checker = runya_checker if runya_checker else SpellChecker(language="", local_dictionary="runya.json")
    candidates = runya_checker.candidates(word)
    candidates = list(candidates)

    return jsonify(candidates)


if __name__ == '__main__':
    app.run(debug=True)
