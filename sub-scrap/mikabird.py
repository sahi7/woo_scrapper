import pandas as pd
from bs4 import BeautifulSoup
import undetected_chromedriver as uc

productData = []
productLinks = []
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'


# Initialize undetected Chrome driver
options = uc.ChromeOptions()
options.add_argument('--headless') 
driver = uc.Chrome(options=options)
driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent":user_agent})

# Get product links
for x in range(1, 3):
    url = f'https://liveparrots.com/shop/page/{x}/'
    driver.get(url)

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    productList = soup.find_all("div", {"class": "type-product"})

    for product in productList:
        link = product.find("a").get('href')
        productLinks.append(link)
    print('Product Links: ', len(productLinks))

# Scrape product data
for link in productLinks:
    driver.get(link)

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    print(f'Scraping {link}')
    
    # Extracting Product Information from Single product Pages
    try:
        name = soup.find("h1", {"class": "product_title"}).text.strip()
    except:
        name = ""

    try:
        short_description = soup.find("div", {"class": "product-short-description"})
    except:
        short_description = ""

    try:
        extract_des = soup.find("div", {"id": "tab-description"})
        [h2.decompose() for h2 in [extract_des.find("h2")] if h2]
        children = extract_des.find_all(recursive=False)
        description = ''.join(str(child) for child in children)
    except:
        if name:
            description = name
        else:
            description = ""

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

    product = {
        "Name": name,
        "Description": description,
        "Short Description": short_description,
        "Categories": categories,
        "Images": images
    }

    productData.append(product)

# Close the browser
driver.quit()

# Save data to CSV
df = pd.DataFrame(productData)
df.to_csv('Liveb.csv', index=False)
