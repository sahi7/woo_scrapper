import re
import time
import pandas as pd
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

productData = []
productLinks = []

baseurl = "https://speedwaymotors.com"
ua = UserAgent(browsers=['edge', 'chrome'])
user_agent = ua.random

# Use the Service class to specify the ChromeDriver path
def switch_ua(user_agent):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')  
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent":user_agent})
    return driver

driver = switch_ua(user_agent)
for x in range(1, 2):
    url = baseurl + '/shop/crate-engines~14-10-344-15341?page={}&sorttype=pricehighlow'.format(x)
    print("Spider warming up .. .. .")
    driver.get(url)

    # Parsing the page using BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    productList = soup.find_all("article", {"class": "productCard"})

    for product in productList:
        elements = soup.select_one('[class^="BrandSkuWrapper_brandWrapper"]')

        # Initialize a dictionary to store product data
        product_info = {}

        if elements:
            # Get category 
            p_tag = elements.find('p', class_='p-subtle')
            category = p_tag.get_text(strip=True).replace('|', '').strip()
            product_info["Category"] = category
            # print("category: ", category)

            # Get sku 
            p_tag = elements.find('p', class_='p-color-subtle')
            sku = p_tag.get_text(strip=True).replace('#', '')
            product_info["SKU"] = sku
            # print("sku: ", sku)

        # Get Price 
        p_tag = soup.find('p', attrs={'data-testid': lambda x: x and 'regular_price' in x})
        price = p_tag.get_text(strip=True).replace('$', '').replace(',', '')
        product_info["Price"] = price
        # print("Price: ", price)

        s_tag = soup.select('span.HorizontalProductCard_specs__2_at_ > *')
        for index, tag in enumerate(s_tag, start=1):
            tag.attrs = {}
            if tag.name == 'p' and index % 2 == 0:
                tag.name = 'b'

        shortD = soup.select_one('span.HorizontalProductCard_specs__2_at_').prettify()
        product_info["Short Description"] = shortD
        # print("shortD: ", shortD)

        link = product.find("a").get('href')
        full_link = baseurl + link
        productLinks.append(full_link)

        # Append product info to productData
        productData.append(product_info)

    print('Product Links: ', len(productLinks))
driver.quit()


from urllib.parse import urlparse, parse_qs, unquote
import random

driver = switch_ua(user_agent)
for i, link in enumerate(productLinks[:2]):
    """Getting Product links to extract product single page data"""
    driver.get(link)
    time.sleep(random.uniform(5, 10)) 

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    print(f'Scraping {link}')

    try:
        name = soup.find("h1").text.strip()
        # print("Product Name: ", name)
        productData[i]["Name"] = name
    except:
        name = ""

    try:
        cleaned_description = ""
        tech_desc = ""

        description_container = soup.select_one('div[data-key="detailsOpenInView"] > :first-child')
        table = soup.select_one('details table')
        if description_container:
            # Find all <a> tags inside the description
            links = description_container.find_all('a')

            # Replace each <a> tag with its text content
            for link in links:
                link.replace_with(link.get_text())
            
            cleaned_description = description_container.prettify()
            # print("cleaned_description: ", cleaned_description)
        if table:
            first_thead, first_tbody = table.find('thead'), table.find('tbody')
            # Create and populate new table
            new_table = soup.new_tag('table')
            [first_thead and new_table.append(first_thead), first_tbody and new_table.append(first_tbody)]
            tech_desc = new_table.prettify()
            # print("tech_desc: ", tech_desc)

        description = f"{cleaned_description}\n\n{tech_desc}"
        productData[i]["Description"] = description

    except:
        description = ""

    try:
        # Initialize a list to store clean image URLs
        clean_image_urls = []

        # Find all thumbnail containers
        thumbnail_containers = soup.find_all('div', class_=lambda x: x and 'gallery_image_thumbnail__' in x)

        # Loop through each container
        for container in thumbnail_containers:
            # Skip containers that are part of a video
            if container.find('div', class_=lambda x: x and 'gallery_video_dimensions' in x):
                continue  # Skip this container

            # Find the <img> tag inside the container
            img_tag = container.find('img')
            if img_tag:
                # Extract the src attribute
                src = img_tag.get('src')

                # Parse the src attribute to extract the 'url' parameter
                parsed_src = urlparse(src)
                query_params = parse_qs(parsed_src.query)
                image_url = query_params.get('url', [None])[0]  # Get the 'url' parameter

                if image_url:
                    # Decode the URL (e.g., convert %3A to : and %2F to /)
                    decoded_image_url = unquote(image_url)

                    # Add the clean URL to the list
                    clean_image_urls.append(decoded_image_url)

        # Join the list of clean image URLs into a comma-separated string
        images = ', '.join(clean_image_urls)
        # print("Images: ", images)
        productData[i]["Images"] = images
    except Exception as e:
        images = ""
        print(f"An error occurred: {e}")

    # print("Updated Product Data: ", productData[i])

driver.quit()

df = pd.DataFrame(productData)
df.to_csv('engines-.csv', index=False)