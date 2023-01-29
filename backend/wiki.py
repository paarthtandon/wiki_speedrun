import requests
from bs4 import BeautifulSoup

from typing import Dict

class Wikipedia:

    def __init__(self, access_token: str, user_agent: str, language: str = 'en') -> None:
        self.headers: Dict[str, str] = {
            'Authorization': access_token,
            'User-Agent': user_agent
        }
        self.base_url: str = f'https://api.wikimedia.org/core/v1/wikipedia/{language}/'
    
    def page(self, title: str) -> str:
        response = requests.get(
            self.base_url + 'page/' + title + '/html',
            headers = self.headers
        )
        return response.text
    
    def page_links(self, title: str) -> list[str]:
        response = requests.get(
            self.base_url + 'page/' + title + '/html',
            headers = self.headers
        )
        soup = BeautifulSoup(response.text, 'html.parser')

        links = [link.get('href') for link in soup.find_all('a')]
        links = [link for link in links if link[0] == '.']
        links = [link for link in links if '#' not in link]
        links = [link for link in links if ':' not in link]
        links = [link for link in links if '?' not in link]
        links = [link[2:] for link in links]
        links = [link for link in links if '/' not in link]

        return list(set(links))
