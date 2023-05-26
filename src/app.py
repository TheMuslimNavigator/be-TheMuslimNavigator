from flask import Flask, jsonify
from urllib import request
import json

from rahmaScraper import RahmaSpider
from snmcScraper import SnmcSpider

app = Flask(__name__)

rahma = RahmaSpider()
snmc = SnmcSpider()


@app.route('/masjidrahma/events')
def get_rahma_events():
    events = rahma.get_events()
    return jsonify(events)


@app.route('/masjidrahma/prayer')
def get_rahma_prayer():
    prayerTimes = rahma.get_prayerTimes()
    return jsonify(prayerTimes)


@app.route('/snmc/events')
def get_snmc_events():
    events = snmc.get_events()
    return jsonify(events)


if __name__ == '__main__':
    app.run()
