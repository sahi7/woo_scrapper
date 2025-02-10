import requests
import itertools
import pandas as pd
import undetected_chromedriver as uc

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


productData = []
productLinks = []

baseurl = "https://outboarddirect.com/"
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
headers = {'User-Agent': user_agent}

for x in range(1, 2):
    url = f'{baseurl}product-category/all-outboard-motors/?product-page={x}/'
    response = requests.get(url, headers=headers)


    #Parsing Selenium page to requests for extraction
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        productList = soup.find_all("li",{"class":"type-product"})

        for product in productList:
            link = product.find("a").get('href')
            productLinks.append(link)
        # print('Product Links: ', len(productLinks), '\n', productLinks)

product_id_counter = itertools.count(start=200)

def select_brand(name):
    brands = ["Honda", "Mercury", "Suzuki", "Tohatsu", "Yamaha"]
    for brand in brands:
        if brand.lower() in name.lower():  # Case-insensitive match
            return brand
    return "Unknown"

options = uc.ChromeOptions()
options.add_argument('--headless') 
driver = uc.Chrome(options=options)
driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent":user_agent})
wait = WebDriverWait(driver, timeout=10)

for link in productLinks:
    """Getting Product links to extract product single page data"""
    driver.get(link)
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".woocommerce-product-gallery__image a")))
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    print(f'Scraping {link}')
    """Extracting Product Information from Single product Pages"""

    try:
    # Find all gallery images
        gallery = driver.find_elements(By.CSS_SELECTOR, ".woocommerce-product-gallery__image a")
        images = [image.get_attribute("href") for image in gallery]
        images = ",".join(images) if images else ""  # Join URLs into a single string
    except Exception as e:
        images = ""
        print("Error:", e)
    # print("Extracted Images:", images)

    try:
        # Find all tag elements
        tag_elements = driver.find_elements(By.CSS_SELECTOR, "span.tagged_as a")
        
        # Extract text from each tag
        tags = [tag.text for tag in tag_elements]
        
        # Join the tags and capitalize
        tags = ",".join(tags).capitalize() if tags else ""
    except Exception as e:
        tags = ""
        print(f"An error occurred: {e}")

    # print("Extracted Tags:", tags)

    try:
        name = soup.find("h1").text.strip()
    except:
        name = ""

    print(f'Product title: ', name)

    try:
        # Find all price elements
        price_elements = soup.select('.price bdi')

        # Extract price values
        prices = [p.get_text(strip=True).replace("$", "") for p in price_elements]

        if len(prices) == 1:
            regular_price = prices[0]
            sale_price = None
        elif len(prices) >= 2:
            sale_price = prices[1]  # Sale price usually appears first
            regular_price = prices[0]  # Regular price appears second (crossed-out)
        else:
            regular_price = None
            sale_price = None

    except Exception as e:
        print(f"Error extracting prices: {e}")
        regular_price = None
        sale_price = None

    # print(f"Regular Price: {regular_price}, Sale Price: {sale_price}")

    for tag in soup.find_all(string=lambda text: text and "outboarddirect.com" in text.lower()):
        tag.parent.decompose()  # Remove the parent tag

    # Remove tags where "outboarddirect.com" appears in attributes (e.g., href, src, etc.)
    for tag in soup.find_all():
        if tag.attrs:  # Ensure tag has attributes
            for attr, value in tag.attrs.items():
                if isinstance(value, str) and "outboarddirect.com" in value.lower():
                    tag.decompose()
                    break
    
    try:
        short_description = soup.find("div", class_="et_pb_wc_description_0").find("div", class_="et_pb_module_inner")
        if short_description:
            inner_contents = short_description.decode_contents()
    except Exception as e:
        short_description = ""
        print(f"An error occurred: {e}")

    print(f'Short Description: ', inner_contents)

    try:
        tab_controls = soup.select(".et_pb_all_tabs > div")

        # Ensure there are at least one tab
        extracted_tabs = {}
        combined_data = ""

        # Iterate over all tabs and extract their content
        for index, tab in enumerate(tab_controls[:-1], start=1): 
            tab_content = tab.decode_contents()
            extracted_tabs[f"tab-{index}"] = tab_content  
            combined_data += tab_content  
            if index > 1: 
                combined_data += "<br>" 
    except:
        combined_data = ""
    
    # print("Individual Tab Data:")
    # print('Desc Len: ', len(extracted_tabs), '\n', extracted_tabs)
    # print('Desc 1: ', extracted_tabs["tab-1"])
    # print('Desc 2: ', extracted_tabs["tab-2"])
    # print('Desc 3: ', extracted_tabs["tab-3"])
    print(f'all data\n', combined_data)

    # try:
    #     categories = [i.text for i in soup.select("span.posted_in a")]
    #     categories = ','.join(categories).capitalize()
    # except:
    #     categories = ""

    try:
        sku = soup.find("span",{"class":"sku"}).text
    except:
        sku = ""

    # try:
    #     tags = [i.text for i in soup.select("span.tagged_as a")]
    #     tags = ','.join(categories).capitalize()
    # except Exception as e:
    #     tags = ""
    #     print(f"An error occurred: {e}")

    # try:
    #     gallery = soup.select('.woocommerce-product-gallery__image a')
    #     images = [image['href'] for image in gallery]
    #     images = ','.join(images)
    # except:
    #     images = ""

    product_brand = select_brand(name)

    def generate_product_id(first_two_digits):
        # Get the next value from the counter and format it as a three-digit number
        incrementing_part = f"{next(product_id_counter):04}"
        
        # Combine the first two digits with the incrementing part
        product_id = f"{first_two_digits}{incrementing_part}"
        
        return int(product_id)

    # Example usage
    first_two_digits = "1204"
    product_id = generate_product_id(first_two_digits)
    # print(f'Product ID: ', product_id)
    # print(f'SKU: ', sku, '\nTags: ', tags)

    product = {"Product ID": product_id, "Name":name, "Regular Price":regular_price, "Sale Price":sale_price, "Description":combined_data, "Short Description":inner_contents, "SKU":sku, "Tags":tags, "Categories":product_brand, "Images":images, "ts_product_brand": product_brand}
    productData.append(product)

df = pd.DataFrame(productData)
df.to_csv('direct-b.csv', index=False)        
