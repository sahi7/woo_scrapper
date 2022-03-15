import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

productData = []
productLinks = []

baseurl = "https://www.osisi.fr/"
user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'
headers = {'User-Agent': user_agent}
medURL = 'https://www.osisi.fr/categorie/125/escalier-quart-tournant.html?page={}'

for x in range(1, 2):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options, executable_path='C:\webapp\zDrivers\chromedriver')
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent":user_agent})
    driver.get(medURL.format(x))
    driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_drpdnMaxItemsPerPage"]/option[2]').click() 
    time.sleep(5)

    #Parsing Selenium page to requests for extraction
    page_link = driver.page_source
    driver.close()
    soup = BeautifulSoup(page_link, "html.parser")
    productList = soup.find_all("div",{"class":"productlistholder"})

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
        product_price = [i.text.strip("$") for i in soup.select('.product-price-amount')][0]
        regular_price0 = product_price.replace('.', '')
        regular_price = regular_price0.replace(',', '.')
    except:
        regular_price = None

    try:
        name = soup.find("h1",{"id":"pageheadertitle"}).text
    except:
        name = ""

    try:
        description = soup.find("div",{"id":"pdetailInfoText"})

    except:
        description = ""

    try:
        short_description = soup.find("div",{"class":"pdetail-specsholder"})
        replace_a = short_description.find("a")
        replace_a.replace_with(replace_a.text)
    except:
        short_description = ""

    try:
        cat = soup.find("div", attrs={"id":"pdetailTableSpecs"})
        p_cat = cat.find("a").text
    except:
        p_cat = "Staircase"

    try:
        images = soup.select('a.pdetail-fullscreen')
        images = images[0]['href']
    except:
        images = ""

    product = { "Regular price":regular_price, "Product Cat":p_cat, "Name":name, "Description":description, "Short Description":short_description, "Images":images }

    productData.append(product)

df = pd.DataFrame(productData)
df.to_csv('data.csv', index=False)
