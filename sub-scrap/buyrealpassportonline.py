import requests
import random
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

productData = []
productLinks = []

baseurl = "https://www.buyrealpassportonline.com/"
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
headers = {'User-Agent': user_agent}
shopURL = 'https://www.leclos.net/shop/product-category/all/wines/wine-portfolio/?sf_paged={}'

for x in range(1,7):
    Dlist = requests.get(shopURL.format(x)).text
    soup = BeautifulSoup(Dlist, "html.parser")
    productList = soup.find_all("li",{"class":"type-product"})
    #productlist = soup.find_all("div",{"class":"product-item-container"})

    for product in productList:
        link = product.select('div.caption a')[0]['href']
        productLinks.append(link)



for link in productLinks:
    """Getting Product links to extract product single page data"""
    singleProductPage = requests.get(link, headers=headers).text
    soup = BeautifulSoup(singleProductPage, 'html.parser')
    """Extracting Product Information from Single product Pages"""
    try:
        price = [i.text.strip("$") for i in soup.select('#price-old')]
        regular_price = price[0]
    except:
        price = None

    try:
        sku = random.randint(1001,3001)
    except:
        sku = ""

    try:
        name = soup.find("div",{"class":"title-product"}).text
    except:
        name = ""

    try:
        extract_short_description = soup.find("div",{"class":"short_description"})
        [h3.decompose() for h3 in extract_short_description('h3')]
        short_description = extract_short_description.text.strip()

    except:
        short_description = ""

    try:
        description = soup.find("div",{"id":"tab-1"}).text
        split = ' '.join([i for i in description.split() if '@' not in i])
        description = split.replace("[email protected]", "us")
    except:
        description = ""

    try:
        categories = soup.find("div",{"class":"model"})
        [span.decompose() for span in categories('span')]
        categories = categories.text
    except:
        categories = ""

    try:
        images = soup.select('img.product-image-zoom')
        images = images[0]['src']
    except:
        images = ""

    product = {"Regular price":regular_price, "SKU":sku, "Name":name, "Short description":short_description, "Description":description, "Categories":categories, "Images":images }

    productData.append(product)

df = pd.DataFrame(productData)
df.to_csv('BuyRealPassport.csv', index=False)
