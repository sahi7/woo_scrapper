import random
import pandas as pd
from bs4 import BeautifulSoup
import undetected_chromedriver as uc

productData = []
productLinks = []

baseurl = "https://www.fiatpapers.com/"
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
headers = {'User-Agent': user_agent}
shopURL = 'https://fiatpapers.com/shop/page/{}/'

# Initialize undetected Chrome driver
options = uc.ChromeOptions()
options.add_argument('--headless') 
driver = uc.Chrome(options=options)
driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent":user_agent})

for x in range(2,5):
    driver.get(shopURL.format(x))
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    productList = soup.find_all("li",{"class":"type-product"})
    #productlist = soup.find_all("div",{"class":"product-item-container"})

    for product in productList:
        link = product.find("a").get('href')
        productLinks.append(link)



for link in productLinks:
    """Getting Product links to extract product single page data"""
    driver.get(link)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    """Extracting Product Information from Single product Pages"""

    try:
        sku = random.randint(1001,3001)
    except:
        sku = ""

    try:
        name = soup.find("h1",{"class":"product_title"}).text
    except:
        name = ""

    try:
        description = soup.find("div",{"id":"tab-description"})
    except:
        description = ""

    try:
        short_description = soup.find("div",{"class":"woocommerce-product-details__short-description"})
    except:
        short_description = ""

    try:
        categories = [i.text for i in soup.select("span.posted_in a")]
        categories = ','.join(categories).capitalize()
    except:
        categories = ""

    try:
        gallery = soup.select('.woocommerce-product-gallery__image a')
        images = [image['href'] for image in gallery]
        images = ','.join(images)
    except:
        images = ""

    product = {"SKU":sku, "Name":name, "Description":description, "Short Description":short_description, "Categories":categories, "Images":images }

    productData.append(product)

df = pd.DataFrame(productData)
df.to_csv('bills1.csv', index=False)
