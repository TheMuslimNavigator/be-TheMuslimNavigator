from flask import Flask, jsonify
from flask_cors import CORS
from urllib import request
import json
from datetime import datetime
# from imageOcr import filterText

from rahmaScraper import RahmaSpider
from snmcScraper import SnmcSpider

app = Flask(__name__)
CORS(app)

rahma = RahmaSpider()
snmc = SnmcSpider()

rahmaEvents = rahma.get_events()
rahmaEventCallTime = datetime.now()

rahmaPrayerTimes = rahma.get_prayerTimes()
rahmaPrayerCallTime = datetime.now()

snmcEvents = snmc.get_events()
# for event in snmcEvents:
#             img = event[1].split("img: ")[1]
#             img_desc = ''.join(map(str, imageOcr(img)))
#             event.append(["img_desc: " + img_desc])

snmcEventCallTime = datetime.now()

snmcPrayerTimes = snmc.get_prayerTimes()
snmcPrayerCallTime = datetime.now()


@app.route('/masjidrahma/events')
def get_rahma_events():
    global rahmaEvents, rahmaEventCallTime
    if (datetime.now() - rahmaEventCallTime).total_seconds() > 21600:
        events = rahma.get_events()
        rahmaEvents = events
        rahmaEventCallTime = datetime.now()
    else:
        events = rahmaEvents
    return jsonify(events)


@app.route('/masjidrahma/prayer')
def get_rahma_prayer():
    global rahmaPrayerTimes, rahmaPrayerCallTime
    if (datetime.now() - rahmaPrayerCallTime).total_seconds() > 21600:
        prayerTimes = rahma.get_prayerTimes()
        rahmaPrayerTimes = prayerTimes
        rahmaPrayerCallTime = datetime.now()
    else:
        prayerTimes = rahmaPrayerTimes
    return jsonify(prayerTimes)


@app.route('/snmc/events')
def get_snmc_events():
    global snmcEvents, snmcEventCallTime
    if (datetime.now() - snmcEventCallTime).total_seconds() > 21600:
        events = snmc.get_events()
        # events = filterText(snmc.get_events())
        snmcEvents = events
        snmcEventCallTime = datetime.now()
    else:
        events = snmcEvents
    return jsonify(events)


@app.route('/snmc/prayer')
def get_snmc_prayer():
    global snmcPrayerTimes, snmcPrayerCallTime
    if (datetime.now() - snmcPrayerCallTime).total_seconds() > 21600:
        prayers = snmc.get_prayerTimes()
        snmcPrayerTimes = prayers
        snmcPrayerCallTime = datetime.now()
    else:
        prayers = snmcPrayerTimes
    return jsonify(prayers)


if __name__ == '__main__':
    app.run()
