import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

productData = []
productLinks = []

baseurl = "https://www.praxisdienst.com/"
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.28.3 (KHTML, like Gecko) Version/3.2.3 ChromePlus/4.0.222.3 Chrome/4.0.222.3 Safari/525.28.3'
headers = {'User-Agent': user_agent}
medURL = 'https://www.praxisdienst.com/en/Infusion+Injection/Infusions+Transfusions/Infusion+Sets+Accessories/?pgNr={}'

for x in range(0, 5):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options, executable_path='C:\webapp\zDrivers\chromedriver')
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent":user_agent})
    driver.get(medURL.format(x))
    #driver.find_element_by_xpath('//*[@id="wcj_products_per_page"]/option[4]').click()


    #Parsing Selenium page to requests for extraction
    page_link = driver.page_source
    driver.close()
    soup = BeautifulSoup(page_link, "html.parser")
    #productList = soup.find_all("li",{"class":"type-product"})
    productList = soup.find_all("div",{"class":"c-productlist__item"})

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
        price = [i.text.strip() for i in soup.select('#productPrice')][0]
        price = int(''.join(i for i in price if i.isdigit()))
        regular_price = price
    except:
        price = None

    try:
        sku = soup.find("div",{"class":"is--artnum"}).text
        sku = sku.split(':')[1].strip()
    except:
        sku = ""

    try:
        name = soup.find("div",{"class":"c-detail__title"}).text.strip()
    except:
        name = ""

    try:
        short_description = soup.find("div",{"id":"detailShortFacts"}).text.strip()
    except:
        short_description = ""

    try:
        description = soup.find("div",{"id":"Description"})
    except:
        description = ""

    try:
        categories = soup.find("span", itemprop="category").text
        categories = str.replace(categories, "/", ",")
    except:
        categories = ""

    try:
        images = soup.select('article.c-imgslider__item a')
        images = images[0]['href']
    except:
        images = ""

    product = { "Regular price":regular_price, """"Sale price":sale_price,""" "SKU":sku, "Name":name, "Description":description, "Short Description":short_description, "Categories":categories, "Images":images }

    productData.append(product)

df = pd.DataFrame(productData)
df.to_csv('Infusion+Sets+Accessories.csv', index=False)
