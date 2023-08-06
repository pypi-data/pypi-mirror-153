from requests import get
from bs4 import BeautifulSoup


class Parse:
    def __init__(self):
        self.headers = {'User-agent': 'Mozilla/5.0'}
        self.proxies = {'http': [], 'https': ''}

    def parse_proxies(self):
        req = get('https://hidemy.name/ru/proxy-list/', headers=self.headers)
        soup = BeautifulSoup(req.text, 'lxml')
        quotes = soup.find_all('td')
        del quotes[0:7]
        quote = [[quotes[i].text, quotes[i + 1].text, quotes[i + 4].text] for i in range(0, len(quotes), 7) if quotes[i + 4].text == 'HTTP' or quotes[i + 4].text == 'HTTPS']
        for i in quote:
            self.proxies[i[2].lower()].append(f'{i[2].lower()}://{i[0]}:{i[1]}')
        return set(self.proxies['http'])
