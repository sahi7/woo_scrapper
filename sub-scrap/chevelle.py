import requests, re
import pandas as pd
from bs4 import BeautifulSoup


productData = []
productLinks = []

baseurl = "https://classiccars.com"
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
headers = {'User-Agent': user_agent}

for x in range(1, 2):
    url = f'https://classiccars.com/listings/find/1964-1972/chevrolet/chevelle?ps=60&p={x}/'
    # url = f'https://classiccars.com/listings/find/all-years/subaru?ps=60&p={x}/'
    response = requests.get(url, headers=headers)
    # driver.get('https://classiccars.com/listings/find/1964-1972/chevrolet/chevelle?ps={}/'.format(x))


    #Parsing Selenium page to requests for extraction
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        productList = soup.find_all("div", {"class": "search-result-item"})

        for product in productList:
            link = product.find("a").get('href')
            image = product.find("img")
            if image and 'default-thumb' not in image.get('src', ''):
                full_link = baseurl + link
                productLinks.append(full_link)
        print('Product Links: ', len(productLinks))


for link in productLinks:
    """Getting Product links to extract product single page data"""
    singleProductPage = requests.get(link, timeout=100, headers=headers)
    if singleProductPage.status_code == 200:
        soup = BeautifulSoup(singleProductPage.content, 'html.parser')
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

        # category = "1964 to 1972 Chevrolet"
        category = "Subaru/Wrx/Stil"
        # category = "Mini Cooper"

        try:
            gallery = soup.select('.gallery-top .swiper-slide[data-jumbo]')
            images = [image['data-jumbo'] for image in gallery if 'youtube' not in image['data-jumbo']]
            images = ','.join(images)
        except:
            images = ""
        
        product = { 
            "Name": name, 
            "Price": price, 
            "Description": description, 
            "Short Description": short_description, 
            "Category": category, 
            "Images": images 
        }

        productData.append(product)

    else:
        print(f"Failed to retrieve product page {link}")

df = pd.DataFrame(productData)
df.to_csv('subaru classic_cars 2.csv', index=False)
