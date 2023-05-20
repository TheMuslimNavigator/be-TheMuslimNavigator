import scrapy
from scrapy import Request
from TheMuslimNavigator.items import MasjidRahmaEventsItem, MasjidRahmaPrayerItem
from scrapy.loader import ItemLoader

# use crawker process to run spider from script
from scrapy.crawler import CrawlerProcess
import re


class RahmaSpider(scrapy.Spider):
    name = "masjidrahma"
    allowed_domains = ["mymasjid.ca"]
    start_urls = ["https://www.mymasjid.ca/events",
                  "https://app.mymasjid.ca/protected/public/timetable"]
    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'masjidrahma.json',
    }

    def parse(self, response):
        events_item = MasjidRahmaEventsItem()
        prayer_item = MasjidRahmaPrayerItem()

        if "events" in response.url:
            # yield self.parse_events(response, events_item)
            for row in response.xpath('//*[@id="tablepress-4"]//tbody/tr'):
                l = ItemLoader(item=MasjidRahmaEventsItem(), selector=row)

                l.add_xpath('event_name', 'td[1]')
                l.add_xpath('event_link', 'td[2]//a/@href')

                if "events" in row.xpath('td[2]//a/@href').get():
                    yield Request(row.xpath('td[2]//a/@href').get(), callback=self.parse_each_event, cb_kwargs=dict(l=l))

                # yield l.load_item()
        elif "timetable" in response.url:
            # yield self.parse_prayer(response, prayer_item)
            for row in response.xpath('//*[@class="table table-sm"]//tbody/tr'):
                l = ItemLoader(item=MasjidRahmaPrayerItem(), selector=row)

                l.add_xpath('prayer_eng', 'td[1]/text()')
                l.add_xpath('athan_time', 'td[2]/text()')
                l.add_xpath('iqama_time', 'td[3]/text()')
                l.add_xpath('prayer_ar', 'td[4]/text()')

                yield l.load_item()

    def parse_each_event(self, response, l):
        event_description = []
        for p in response.xpath('//div[@class="content event_details"]/p'):
            text = ''.join(p.xpath('.//text()').getall())

            # handle nested a tags
            for a in p.xpath('.//a'):
                a_text = ' '.join(a.xpath('.//text()').getall())
                a_href = a.xpath('.//@href').get()
                text = text.replace(a_text, f'[{a_text}]({a_href})')

            event_description.append(text)

        # event_description.append(response.xpath(
        #     '//div[@class="content event_details"]/ul/li/text()').getall())

        for li in response.xpath('//div[@class="content event_details"]/ul/li'):
            li_start = ", point: "
            li_text = ''.join(li.xpath('.//text()').get())
            event_description.append(li_start + li_text)

        event_img = response.xpath(
            '//div[@class="content event_poster"]//img/@src').get()

        if event_img is not None:
            event_img = "https://events.mymasjid.ca" + event_img
            l.add_value('event_image', event_img)

        for i in range(len(event_description)):
            event_description[i] = re.sub(
                r'[\xa0\xae\xa7\u2060]', '', event_description[i])

        l.add_value('event_description', event_description)

        yield l.load_item()


# main driver
if __name__ == "__main__":
    # run scraper
    process = CrawlerProcess()
    process.crawl(RahmaSpider)
    process.start()
