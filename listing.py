import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

productData = []
productLinks = []

baseurl = "https://buywinesonline.com/"
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.28.3 (KHTML, like Gecko) Version/3.2.3 ChromePlus/4.0.222.3 Chrome/4.0.222.3 Safari/525.28.3'
headers = {'User-Agent': user_agent}

for x in range(1, 2):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_experimental_option("prefs",{'profile.managed_default_content_settings.javascript': 2})
    driver = webdriver.Chrome(options=options, executable_path='C:\webapp\zDrivers\chromedriver')
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent":user_agent})
    driver.get('https://uptownspirits.com/shop/liquor/page/{}/?per_page=144'.format(x))
    #driver.find_element_by_xpath('//*[@id="th-view-options-per-page"]/option[3]').click()


    #Parsing Selenium page to requests for extraction
    page_link = driver.page_source
    driver.close()
    soup = BeautifulSoup(page_link, "html.parser")
    #productList = soup.find_all("li",{"class":"type-product"})
    productList = soup.find_all("div",{"class":"product-item"})

    for product in productList:
        #link = product.find("a",{"class":"woocommerce-LoopProduct-link"}).get('href')
        link = product.find("a").get('href')
        print(baseurl + link)
        productLinks.append(baseurl + link)


for link in productLinks:
    """Getting Product links to extract product single page data"""
    singleProductPage = requests.get(link, headers=headers).text
    soup = BeautifulSoup(singleProductPage, 'html.parser')
    """Extracting Product Information from Single product Pages"""
    try:
        price = [i.text.strip("£") for i in soup.select('.price bdi:first-child')]
        regular_price = price[0]
        sale_price = price[1]
    except:
        price = None

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
        images = soup.select('div.woocommerce-product-gallery a')
        #images = soup.select('figure.image-item a')
        images = images[0]['href']
    except:
        images = ""

    product = { "Regular price":regular_price, """"Sale price":sale_price,""" "SKU":sku, "Name":name, "Description":description, "Short Description":short_description, "Categories":categories, "Images":images }

    productData.append(product)

df = pd.DataFrame(productData)
df.to_csv('thc-spirits.csv', index=False)
