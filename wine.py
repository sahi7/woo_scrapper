import requests, re
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

productData = []
productLinks = []

baseurl = "https://buywinesonline.com"
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.28.3 (KHTML, like Gecko) Version/3.2.3 ChromePlus/4.0.222.3 Chrome/4.0.222.3 Safari/525.28.3'
headers = {'User-Agent': user_agent}

for x in range(10, 18):  

    Dlist = requests.get('https://buywinesonline.com/collections/all-available-wines?page={}'.format(x)).text
    soup = BeautifulSoup(Dlist, "html.parser")
    #productList = soup.find_all("li",{"class":"type-product"})
    productList = soup.find_all("div",{"class":"product-item"})

    for product in productList:
        #link = product.find("a",{"class":"woocommerce-LoopProduct-link"}).get('href')
        link = product.find("a").get('href')
        productLinks.append(baseurl + link)


for link in productLinks:
    """Getting Product links to extract product single page data"""
    singleProductPage = requests.get(link, headers=headers).text
    soup = BeautifulSoup(singleProductPage, 'html.parser')
    """Extracting Product Information from Single product Pages"""
    try:
        price = [i.text.strip("$") for i in soup.select('span.price')][0]
        price = re.findall(r"[-+]?\d*\.\d+|\d+", price)
        regular_price = price[0]
        sale_price = price[1]
    except:
        price = None

    try:
        name = soup.find("h1",{"class":"product-meta__title"}).text.strip()
    except:
        name = ""

    try:
        short_description = [i.text.strip() for i in soup.select('div.pipWineNotes')]
        short_description = short_description[0]
    except:
        short_description = ""

    try:
        extract_des = [i.text.strip() for i in soup.select('div.product-attribute')]
        description = extract_des[0]
    except:
        description = ""

    try:
        categories = [i.text for i in soup.select("a.product-meta__vendor")]
        categories = ','.join(categories).capitalize()
    except:
        categories = ""

    try:
        images = [i.get('data-zoom') for i in soup.select('img.product-gallery__image', srcset=True)]
        #images = soup.select('figure.image-item a')
        images = "https:" + images[0]
    except:
        images = ""

    product = { "Regular price":regular_price, "Name":name, "Description":description, "Short Description":short_description, "Categories":categories, "Images":images }

    productData.append(product)

df = pd.DataFrame(productData)
df.to_csv('wine-2.csv', index=False)
