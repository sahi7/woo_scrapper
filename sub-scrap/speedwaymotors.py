import re
import time
import pandas as pd
import undetected_chromedriver as uc

from bs4 import BeautifulSoup


options = uc.ChromeOptions()
# options.add_argument('--headless') 
driver = uc.Chrome(options=options)

productData = []
productLinks = []

baseurl = "https://speedwaymotors.com"
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
headers = {'User-Agent': user_agent}
driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent":user_agent})

for x in range(1, 2):
    url = baseurl + '/shop/crate-engines~14-10-344-15341?page={}'.format(x)
    driver.get(url)
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    productList = soup.find_all("article", {"class": "productCard"})

    for product in productList:
        link = product.find("a").get('href')
        full_link = baseurl + link
        productLinks.append(full_link)
    print('Product Links: ', len(productLinks))

for link in productLinks:
    """Getting Product links to extract product single page data"""
    # driver.get(link)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    print(f'Scraping {link}')
    """Extracting Product Information from Single product Pages"""

    try:
        name = soup.select_one(".pm-details-list .p-name span").text.strip()
    except:
        name = ""

    try:
        price = soup.select(".pm-details-list .p-price span")[-1].text.strip()
        price = re.sub(r'[^\d.]', '', price)
    except:
        price = ""

    try:
        short_description = soup.select_one(".vehicle-description p").text.strip()
    except:
        short_description = ""

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

    # category = "Mercedes-Benz"
    # category = "Subaru/Wrx/Stil"
    category = "Honda|Honda > Civic"

    try:
        gallery = soup.select('.gallery-top .swiper-slide[data-jumbo]')
        images = [image['data-jumbo'] for image in gallery if 'youtube' not in image['data-jumbo']]
        images = images[:10]
        images = ','.join(images)
    except Exception as e:
        images = ""
        print(f"An error occurred: {e}")

    product = {
        "Name": name,
        "Price": price,
        "Description": description,
        "Short Description": short_description,
        "Category": category,
        "Images": images
    }

    productData.append(product)

# driver.quit()

# df = pd.DataFrame(productData)
# df.to_csv('Honda-civic.csv', index=False)