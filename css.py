import requests, re, time
from bs4 import BeautifulSoup
from selenium import webdriver
productLinks = []
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.28.3 (KHTML, like Gecko) Version/3.2.3 ChromePlus/4.0.222.3 Chrome/4.0.222.3 Safari/525.28.3'
headers = {'User-Agent': user_agent}
Dlist = requests.get('https://uptownspirits.com/product/liquor/bonpas-luberon-750ml/', headers=headers).text
soup = BeautifulSoup(Dlist, "html.parser")

#description = soup.find("div",{"id":"tab-1"}).text
#split = ' '.join([i for i in description.split() if '@' not in i])
#description = split.replace("[email protected]", "us")
#print(description)
# PRODUCT VARIATIONS
"""
labels = soup.find_all("td", {"class":"label"})
labels = [label.text for label in labels]

select = soup.find_all('td', attrs={'class' : 'value'})
for option in select:
    select = soup.find_all('option')
    sec=[i.text for i in select]
"""
categories = [i.text.strip() for i in soup.select("tr.woocommerce-product-attributes-item--attribute_pa_alcohol-type td")][0]

#categories = ','.join(categories).capitalize()
print(categories)
