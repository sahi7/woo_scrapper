import requests
import pandas as pd
import itertools
from bs4 import BeautifulSoup
import undetected_chromedriver as uc

productData = []
productLinks = []

baseurl = "https://www.thepinballcompany.com/"
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.28.3 (KHTML, like Gecko) Version/3.2.3 ChromePlus/4.0.222.3 Chrome/4.0.222.3 Safari/525.28.3'
headers = {'User-Agent': user_agent}




options = uc.ChromeOptions()
options.add_argument('--headless') 
driver = uc.Chrome(options=options)
driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent":user_agent})

for x in range(1, 4):
    url = 'https://www.thepinballcompany.com/product-category/more/page/{}/'.format(x)
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print("Request Passed")
    # # driver.get('https://www.thepinballcompany.com/product-category/pinball-machines/page/{}/'.format(x))
    # #driver.find_element_by_xpath('//*[@id="th-view-options-per-page"]/option[3]').click()


        #Parsing Selenium page to requests for extraction
        # page_link = driver.page_source
        # driver.close()
        # soup = BeautifulSoup(page_link, "html.parser")
        soup = BeautifulSoup(response.content, 'html.parser')                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
        #productList = soup.find_all("li",{"class":"type-product"})
        productList = soup.find_all("div",{"class":"type-product"})

        for product in productList:
            #link = product.find("a",{"class":"woocommerce-LoopProduct-link"}).get('href')
            link = product.find("a").get('href')
            productLinks.append(link)
        print("productLinks: ", productLinks)

product_id_counter = itertools.count(start=27)

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
        categories = '|'.join(categories).capitalize()
    except:
        categories = ""

    try:
        gallery = soup.select('.woocommerce-product-gallery__image a')
        images = [image['href'] for image in gallery]
        images = '|'.join(images)
    except:
        images = ""

    def generate_product_id(first_two_digits):
        # Get the next value from the counter and format it as a three-digit number
        incrementing_part = f"{next(product_id_counter):04}"
        
        # Combine the first two digits with the incrementing part
        product_id = f"{first_two_digits}{incrementing_part}"
        
        return int(product_id)

    # Example usage
    # first_two_digits = "1234" # 1-2 
    # first_two_digits = "1235" # 2-5 
    # first_two_digits = "1236" # 5-10 
    # first_two_digits = "1237" # 10-15
    first_two_digits = "1342" 
    product_id = generate_product_id(first_two_digits)
    print(f'Product ID: ', product_id)

    combined_description = f"{(short_description or '')}\n{(description or '')}"

    product = {"Product ID": product_id, "Regular price":regular_price, "Name":name, "Short Description":short_description, "Description":combined_description, "Categories":categories, "Images":images }

    productData.append(product)

df = pd.DataFrame(productData)
df.to_csv('pinball_38.csv', index=False)
