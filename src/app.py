from flask import Flask, jsonify, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("speller.html")


@app.route("/suggest/<string:word>")
def suggestions(word):
    from spellchecker import SpellChecker

    checker = SpellChecker(language="", local_dictionary="runya.json.gz")
    candidates = checker.candidates(word)
    candidates = list(candidates)

    return jsonify(candidates)


if __name__ == '__main__':
    app.run(debug=True)
