from flask import Flask, jsonify

from src.moonwalk.api import MoonwalkAPI
from src.transform import CreateNew

app = Flask(__name__)


@app.route('/updates')
def updates():
    raw_serials = MoonwalkAPI().updates_serials()
    raw_movies = MoonwalkAPI().updates_movies()
    animes = CreateNew(raw_serials + raw_movies)

    return jsonify([i.to_dict() for i in animes.storage.values()])


@app.route('/fetch')
def fetch():
    raw_serials = MoonwalkAPI().get_serials()
    raw_movies = MoonwalkAPI().get_movies()
    animes = CreateNew(raw_serials + raw_movies)

    return jsonify([i.to_dict() for i in animes.storage.values()])


app.run(port=8080)
