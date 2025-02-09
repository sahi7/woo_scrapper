import requests
import pandas as pd
import itertools
from bs4 import BeautifulSoup


productData = []
productLinks = []

baseurl = "https://bridgeviewmarine.com/"
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
headers = {'User-Agent': user_agent}

for x in range(2, 9):
    url = f'https://bridgeviewmarine.com/product-category/boat-engines-outboards/page/{x}/'
    response = requests.get(url, headers=headers)


    #Parsing Selenium page to requests for extraction
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        productList = soup.find_all("li",{"class":"type-product"})

        for product in productList:
            link = product.find("a").get('href')
            productLinks.append(link)
        # print('Product Links: ', len(productLinks), '\n', productLinks)

product_id_counter = itertools.count(start=27)

for link in productLinks:
    """Getting Product links to extract product single page data"""
    singleProductPage = requests.get(link, timeout=100, headers=headers)
    if singleProductPage.status_code == 200:
        soup = BeautifulSoup(singleProductPage.content, 'html.parser')
        print(f'Scraping {link}')
        """Extracting Product Information from Single product Pages"""

        try:
            name = soup.find("h1",{"class":"product_title"}).text.strip()
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
            elif len(prices) == 2:
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

        try:
            # Find the short description element
            short_description = soup.find("div", {"class": "woocommerce-product-details__short-description"})
            
            if short_description:
                # Find all <b> and <strong> tags except the first one
                bold_tags = short_description.find_all(['b', 'strong', 'span'])

                # Iterate over all <b> and <strong> tags except the first one
                for tag in bold_tags[1:]:
                    # Find the parent tag of the <b> or <strong> tag
                    parent = tag.find_parent()

                    # Remove the parent only if it is a <p> tag
                    if parent:
                        parent.decompose()

                # Remove empty tags after processing
                for empty_tag in short_description.find_all():
                    if empty_tag.name in ["p", "div", "span"] and not empty_tag.text.strip():
                        empty_tag.decompose()

        except Exception as e:
            print(f"An error occurred: {e}")
            short_description = ""

        # print(f'short description: ', short_description)

        try:
            extract_des = soup.find("div",{"class":"woocommerce-Tabs-panel--description"})
            if extract_des:
                for h2_tag in extract_des.find_all("h2"):
                    h2_tag.decompose()
                # Find all <b> and <strong> tags except the first one
                bold_tags = extract_des.find_all(['b', 'strong', 'span'])

                # Iterate over all <b> and <strong> tags except the first one
                for tag in bold_tags[1:]:
                    # Find the parent tag of the <b> or <strong> tag
                    parent = tag.find_parent()

                    # Remove the parent only if it is a <p> tag
                    if parent:
                        parent.decompose()

                # Remove empty tags after processing
                for empty_tag in extract_des.find_all():
                    if empty_tag.name in ["p", "div", "span"] and not empty_tag.text.strip():
                        empty_tag.decompose()

                # Extract the cleaned content without the outer div tag
                description_content = extract_des.decode_contents()
        except:
            if name:
                description_content = name
            else:
                description_content = ""

        # print('Description: ', description_content)

        # try:
        #     categories = [i.text for i in soup.select("span.posted_in a")]
        #     categories = ','.join(categories).capitalize()
        # except:
        #     categories = "Mercury"

        # print(f'Categories: ',categories )

        # try:
        #     tags = [i.text for i in soup.select("span.tagged_as a")]
        #     tags = ','.join(categories).capitalize()
        # except:
        #     tags = ""

        try:
            gallery = soup.select('.woocommerce-product-gallery__image a')
            images = [image['href'] for image in gallery]
            images = ','.join(images)
        except:
            images = ""

        def generate_product_id(first_two_digits):
            # Get the next value from the counter and format it as a three-digit number
            incrementing_part = f"{next(product_id_counter):04}"
            
            # Combine the first two digits with the incrementing part
            product_id = f"{first_two_digits}{incrementing_part}"
            
            return int(product_id)

        # Example usage
        first_two_digits = "1234"
        product_id = generate_product_id(first_two_digits)
        print(f'Product ID: ', product_id)

        product = {"Product ID": product_id, "Name":name, "Regular Price":regular_price, "Sale Price":sale_price, "Description":description_content, "Short Description":short_description, "Categories":"Mercury", "Images":images, "ts_product_brand": "Mercury"}
        attributes = []

        try:
            # Find all attribute rows
            attribute_rows = soup.find_all('tr', class_='woocommerce-product-attributes-item')

            if attribute_rows:
                for row in attribute_rows:
                    label = row.find('th', class_='woocommerce-product-attributes-item__label')
                    value = row.find('td', class_='woocommerce-product-attributes-item__value')

                    if label and value:
                        attributes.append({
                            "name": label.text.strip(),
                            "value": value.text.strip(),
                            "visible": "1",
                            "global": "1"
                        })

        except Exception as e:
            print(f"An error occurred while extracting attributes: {e}")

        # Add attributes dynamically to product dictionary
        for i, attr in enumerate(attributes):
            product[f"Attribute {i+1} name"] = attr["name"]
            product[f"Attribute {i+1} value(s)"] = attr["value"]
            product[f"Attribute {i+1} visible"] = attr["visible"]
            product[f"Attribute {i+1} global"] = attr["global"]

        productData.append(product)

    else:
        print(f"Failed to retrieve product page {link}")


df = pd.DataFrame(productData)
df.to_csv('Out-b.csv', index=False)
