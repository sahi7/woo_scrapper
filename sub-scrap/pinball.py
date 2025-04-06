import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

productData = []
productLinks = []

baseurl = "https://www.thepinballcompany.com/"
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.28.3 (KHTML, like Gecko) Version/3.2.3 ChromePlus/4.0.222.3 Chrome/4.0.222.3 Safari/525.28.3'
headers = {'User-Agent': user_agent}

for x in range(2, 8):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_experimental_option("prefs",{'profile.managed_default_content_settings.javascript': 2})
    driver = webdriver.Chrome(options=options, executable_path='C:\webapp\zDrivers\chromedriver')
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent":user_agent})
    driver.get('https://www.thepinballcompany.com/product-category/pinball-machines/page/{}/'.format(x))
    #driver.find_element_by_xpath('//*[@id="th-view-options-per-page"]/option[3]').click()


    #Parsing Selenium page to requests for extraction
    page_link = driver.page_source
    driver.close()
    soup = BeautifulSoup(page_link, "html.parser")
    #productList = soup.find_all("li",{"class":"type-product"})
    productList = soup.find_all("div",{"class":"type-product"})

    for product in productList:
        #link = product.find("a",{"class":"woocommerce-LoopProduct-link"}).get('href')
        link = product.find("a").get('href')
        productLinks.append(link)


for link in productLinks:
    """Getting Product links to extract product single page data"""
    singleProductPage = requests.get(link, headers=headers).text
    soup = BeautifulSoup(singleProductPage, 'html.parser')
    """Extracting Product Information from Single product Pages"""
    try:
        price = [i.text.strip("$") for i in soup.select('.woocommerce-Price-amount bdi')]
        regular_price = price[15]
    except:
        price = None

    try:
        name = soup.find("h1",{"class":"product-title"}).text.strip()
    except:
        name = ""

    try:
        short_description = soup.find("div",{"itemprop":"description"})
    except:
        short_description = ""

    try:
        description = soup.find("div",{"id":"tab-description"})
    except:
        description = ""

    try:
        categories = [i.text for i in soup.select("span.posted_in a")]
        categories = ','.join(categories).capitalize()
    except:
        categories = ""

    try:
        images = soup.find("a",{"itemprop":"image"}).get('href')
    except:
        images = ""

    product = { "Regular price":regular_price, "Name":name, "Short Description":short_description, "Description":description, "Categories":categories, "Images":images }

    productData.append(product)

df = pd.DataFrame(productData)
df.to_csv('pinball_2.csv', index=False)
