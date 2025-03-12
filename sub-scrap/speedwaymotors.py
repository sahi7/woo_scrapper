import re
import time
import pandas as pd
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlunparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')  

# Use the Service class to specify the ChromeDriver path
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

productData = []
productLinks = []

baseurl = "https://speedwaymotors.com"
ua = UserAgent(browsers=['edge', 'chrome'])
user_agent = ua.random

driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent":user_agent})

for x in range(1, 2):
    url = baseurl + '/shop/crate-engines~14-10-344-15341?page={}&sorttype=pricehighlow'.format(x)
    print("Spider warming up .. .. .")
    driver.get(url)

    # Parsing the page using BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    productList = soup.find_all("article", {"class": "productCard"})

    for product in productList:
        # elements = soup.select_one('[class^="BrandSkuWrapper_brandWrapper"]')

        # # Initialize a dictionary to store product data
        # product_info = {}

        # if elements:
        #     # Get category 
        #     p_tag = elements.find('p', class_='p-subtle')
        #     category = p_tag.get_text(strip=True).replace('|', '').strip()
        #     product_info["Category"] = category
        #     print("category: ", category)

        #     # Get sku 
        #     p_tag = elements.find('p', class_='p-color-subtle')
        #     sku = p_tag.get_text(strip=True).replace('#', '')
        #     product_info["SKU"] = sku
        #     print("sku: ", sku)

        # # Get Price 
        # p_tag = soup.find('p', attrs={'data-testid': lambda x: x and 'regular_price' in x})
        # price = p_tag.get_text(strip=True).replace('$', '').replace(',', '')
        # product_info["Price"] = price
        # print("Price: ", price)

        # s_tag = soup.select('span.HorizontalProductCard_specs__2_at_ > *')
        # for index, tag in enumerate(s_tag, start=1):
        #     tag.attrs = {}
        #     if tag.name == 'p' and index % 2 == 0:
        #         tag.name = 'b'

        # shortD = soup.select_one('span.HorizontalProductCard_specs__2_at_').prettify()
        # product_info["Short Description"] = shortD
        # print("shortD: ", shortD)

        link = product.find("a").get('href')
        full_link = baseurl + link
        productLinks.append(full_link)

        # Append product info to productData
        # productData.append(product_info)

    print('Product Links: ', len(productLinks))

for i, link in enumerate(productLinks):
    """Getting Product links to extract product single page data"""
    driver.get(link)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    print(f'Scraping {link}')

    try:
        name = soup.select_one(".h1").text.strip()
        # productData[i]["Name"] = name
    except:
        name = ""

    # print("Updated Product Data: ", productData[i])

    try:
        extract_des = soup.select_one(".pm-details-list")
        address = extract_des.select_one(".p-address")
        last_c = extract_des.select_one("li:not(.border-btm)")
        if address:
            address.decompose()
        if last_c:
            last_c.decompose()
        description = str(extract_des)
    except:
        description = ""

    try:
        # Initialize a list to store clean image URLs
        clean_image_urls = []

        # Find all thumbnail containers
        thumbnail_containers = soup.find_all('div', class_=lambda x: x and 'gallery_image_thumbnail' in x)

        # Loop through each container
        for container in thumbnail_containers:
            # Skip containers that are part of a video (e.g., parent has 'gallery_video_dimensions')
            if container.find_parent('div', class_=lambda x: x and 'gallery_video_dimensions' in x):
                continue  # Skip this container

            # Find the <img> tag inside the container
            img_tag = container.find('img')
            if img_tag:
                # Extract the src attribute
                src = img_tag.get('src')

                # Clean the src attribute to remove query parameters
                parsed_url = urlparse(src)
                clean_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, '', '', ''))

                # Add the clean URL to the list
                clean_image_urls.append(clean_url)

        # Join the list of clean image URLs into a comma-separated string
        images = ', '.join(clean_image_urls)
        print("Images: ", images)
        # productData[i]["Images"] = images
    except Exception as e:
        images = ""
        print(f"An error occurred: {e}")

driver.quit()

df = pd.DataFrame(productData)
df.to_csv('engines-.csv', index=False)