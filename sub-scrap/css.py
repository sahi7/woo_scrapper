import requests, re
from bs4 import BeautifulSoup
from selenium import webdriver

productLinks = []
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.28.3 (KHTML, like Gecko) Version/3.2.3 ChromePlus/4.0.222.3 Chrome/4.0.222.3 Safari/525.28.3'
headers = {'User-Agent': user_agent}
shopURL = "https://classiccars.com/listings/view/1861952/1969-chevrolet-chevelle-ss-for-sale-in-kansas-city-missouri-64112"

singleProductPage = requests.get(shopURL, headers=headers).text
soup = BeautifulSoup(singleProductPage, 'html.parser')

gallery = soup.select('.gallery-top .swiper-slide[data-jumbo]')
images = [image['data-jumbo'] for image in gallery if 'youtube' not in image['data-jumbo']]


# from deep_translator import GoogleTranslator
# translated = GoogleTranslator(source='french', target='english').translate_file('QUARTER-TURN1.csv')
