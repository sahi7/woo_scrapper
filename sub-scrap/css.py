import requests, re
from bs4 import BeautifulSoup
from selenium import webdriver

productLinks = []
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.28.3 (KHTML, like Gecko) Version/3.2.3 ChromePlus/4.0.222.3 Chrome/4.0.222.3 Safari/525.28.3'
headers = {'User-Agent': user_agent}
shopURL = "https://grandiosegroupltd.com/product/soybean-oil/"

singleProductPage = requests.get(shopURL, headers=headers).text
soup = BeautifulSoup(singleProductPage, 'html.parser')

extract_des = soup.find("div", {"class": "woocommerce-Tabs-panel--description"})

# Check if the element was found
if extract_des:
    # Extract and print all children of this element excluding the element tag itself
    [h2.decompose() for h2 in [extract_des.find("h2")] if h2]
    children = extract_des.find_all(recursive=False)
    description = ''.join(str(child) for child in children)
    print('Children', description)

# from deep_translator import GoogleTranslator
# translated = GoogleTranslator(source='french', target='english').translate_file('QUARTER-TURN1.csv')
