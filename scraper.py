import requests
from bs4 import BeautifulSoup


URL = 'http://www.free-sudoku.com/sudoku.php'


class Scraper:
    pass


r = requests.get(URL)
soup = BeautifulSoup(r.content, "lxml")
print(soup.find_all('div'))
#div = body.find_all('div', {'class': 'pred2'})
