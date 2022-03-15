import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

productData = []
productLinks = []

baseurl = "https://toyotadirectparts.co.uk/"
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
headers = {'User-Agent': user_agent}

for x in range(1, 2):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options, executable_path='C:\webapp\zDrivers\chromedriver')
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent":user_agent})
    driver.get('https://tsco-ltd.com/shop/page/{}/'.format(x))
    #driver.find_element_by_xpath('//*[@id="wcj_products_per_page"]/option[4]').click()


    #Parsing Selenium page to requests for extraction
    page_link = driver.page_source
    driver.close()
    soup = BeautifulSoup(page_link, "html.parser")
    productList = soup.find_all("li",{"class":"type-product"})

    for product in productList:
        link = product.find("a",{"class":"woocommerce-LoopProduct-link"}).get('href')
        productLinks.append(link)


for link in productLinks:
    """Getting Product links to extract product single page data"""
    singleProductPage = requests.get(link, headers=headers).text
    soup = BeautifulSoup(singleProductPage, 'html.parser')
    """Extracting Product Information from Single product Pages"""
    try:
        price = [i.text.strip("£") for i in soup.select('.price bdi:first-child')]
        regular_price = price[0]
        sale_price = price[1]
    except IndexError:
        return 'Price Not Found'

    try:
        sku = soup.find("span",{"class":"sku"}).text
    except:
        sku = ""

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
        description = extract_des.text.strip()
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

    product = { "SKU":sku, "Name":name, "Description":description, "Short Description":short_description, "Categories":categories, "Images":images }

    productData.append(product)

df = pd.DataFrame(productData)
df.to_csv('sugar.csv', index=False)
