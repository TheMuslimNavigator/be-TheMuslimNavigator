from bs4 import BeautifulSoup
from urllib.request import urlopen


class SnmcSpider:
    def __init__(self):
        self.events_page = urlopen("https://snmc.ca/").read()
        self.events_soup = BeautifulSoup(self.events_page, 'html.parser')

    def get_events(self):
        events_t = []
        events = self.events_soup.find_all('div', {'class': 'sbi_item'})
        for event in events:
            events_t.append(("desc: " + event.find('img')
                            ['alt'], "img: " + event.find('a')['data-full-res']))
        return events_t
