import requests
import re
from bs4 import BeautifulSoup, ResultSet
import pickle

UFGO_BASE_URL = "https://ufgo.org"
UFGO_RATING_LIST_URL = UFGO_BASE_URL + '/rating-list/'
RATING_LIST_REGEX = re.compile(r"/rating-list/(\d{4})-(\d{2})-(\d{2})/")

response = requests.get(UFGO_BASE_URL + '/rating-list/')
soup = BeautifulSoup(response.text, 'html.parser')

ACTUAL_RATING_LIST_SUFFIX = soup.find("a", href=RATING_LIST_REGEX)['href']
response = requests.get(UFGO_BASE_URL + ACTUAL_RATING_LIST_SUFFIX)

soup = BeautifulSoup(response.text, 'html.parser')
players = []


class Player:
    def __init__(self, player_data: ResultSet):
        self.ufgo_place = int(player_data[0].text)
        self.full_name = player_data[1].text
        self.city = player_data[2].text
        self.rank = player_data[3].text
        self.rating = float(player_data[4].text)
        self.degree = player_data[5].text

    def __str__(self):
        return '{} {}'.format(self.full_name, int(self.rating))

    def __repr__(self):
        return 'Player {}'.format(self.full_name)


for person in soup.table.find_all('tr'):
    player_data = person.find_all('td')
    players.append(Player(player_data))


with open('ufgo_ratings', 'wb') as file:
    pickle.dump(players, file)
