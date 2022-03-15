import requests, re
from bs4 import BeautifulSoup
from selenium import webdriver
"""
productLinks = []
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.28.3 (KHTML, like Gecko) Version/3.2.3 ChromePlus/4.0.222.3 Chrome/4.0.222.3 Safari/525.28.3'
headers = {'User-Agent': user_agent}
shopURL = "https://www.osisi.fr/produit/179075/escalier-kalea-quart-de-tour-a-gauche-en-bas-chene-massif-apache-grey.html"

singleProductPage = requests.get(shopURL, headers=headers).text
soup = BeautifulSoup(singleProductPage, 'html.parser')

"""
from deep_translator import GoogleTranslator
translated = GoogleTranslator(source='french', target='english').translate_file('QUARTER-TURN1.csv')
