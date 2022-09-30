from bs4 import BeautifulSoup
import requests

response = requests.get('https://bg.wikipedia.org/wiki/%D0%93%D1%80%D0%B0%D0%B4%D0%BE%D0%B2%D0%B5_%D0%B2_%D0%91%D1%8A%D0%BB%D0%B3%D0%B0%D1%80%D0%B8%D1%8F')

soup = BeautifulSoup()