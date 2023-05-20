from flask import Flask, jsonify
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor, defer

app = Flask(__name__)
runner = CrawlerRunner()


@app.route('/masjidrahma')
def scrape_spider1():
    @defer.inlineCallbacks
    def crawl():
        # Replace with your Spider 1 class name
        spider_output = yield runner.crawl("masjidrahma")
        scraped_data = spider_output.get('items', [])
        data_dict = [dict(item) for item in scraped_data]
        response = jsonify(data_dict)
        defer.returnValue(response)

    task = crawl()
    task.addCallback(lambda result: result)
    return task


if __name__ == '__main__':
    app.run()
    reactor.stop()
