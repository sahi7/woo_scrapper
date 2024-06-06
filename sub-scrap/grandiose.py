import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import undetected_chromedriver as uc


productData = []
productLinks = []

baseurl = "https://grandiosegroupltd.com/"
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
headers = {'User-Agent': user_agent}

for x in range(2, 6):
    # user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
    url = f'https://grandiosegroupltd.com/shop/page/{x}/'
    response = requests.get(url, headers=headers)
    # driver.get('https://grandiosegroupltd.com/shop/page/{}/'.format(x))


    #Parsing Selenium page to requests for extraction
    if response.status_code == 200:
        print('Correct')
        soup = BeautifulSoup(response.content, 'html.parser')
        productList = soup.find_all("li",{"class":"type-product"})

        for product in productList:
            link = product.find("a",{"class":"woocommerce-LoopProduct-link"}).get('href')
            productLinks.append(link)
        print('Product Links: ', len(productLinks))


for link in productLinks:
    """Getting Product links to extract product single page data"""
    singleProductPage = requests.get(link, headers=headers)
    if singleProductPage.status_code == 200:
        soup = BeautifulSoup(singleProductPage.content, 'html.parser')
        print('Correct 2')
        """Extracting Product Information from Single product Pages"""

        try:
            name = soup.find("h1",{"class":"product_title"}).text.strip()
        except:
            name = ""

        try:
            short_description = soup.find("div",{"class":"woocommerce-product-details__short-description"}).text.strip()
        except:
            short_description = ""

        try:
            extract_des = soup.find("div",{"class":"woocommerce-Tabs-panel--description"})
            [h2.decompose() for h2 in extract_des('h2')]
            description = extract_des
        except:
            description = ""

        try:
            categories = [i.text for i in soup.select("span.posted_in a")]
            categories = ','.join(categories).capitalize()
        except:
            categories = ""

        try:
            tags = [i.text for i in soup.select("span.tagged_as a")]
            tags = ','.join(categories).capitalize()
        except:
            tags = ""

        try:
            gallery = soup.select('.woocommerce-product-gallery__image a')
            images = [image['href'] for image in gallery]
            images = ','.join(images)
        except:
            images = ""
        
        product = { "Name":name, "Description":description, "Short Description":short_description, "Categories":categories, "Images":images }

        productData.append(product)

    else:
        print(f"Failed to retrieve product page {link}")


df = pd.DataFrame(productData)
df.to_csv('Grandiose 2.csv', index=False)
