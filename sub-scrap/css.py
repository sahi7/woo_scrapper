import requests, re
from bs4 import BeautifulSoup
from selenium import webdriver

productLinks = []
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.28.3 (KHTML, like Gecko) Version/3.2.3 ChromePlus/4.0.222.3 Chrome/4.0.222.3 Safari/525.28.3'
headers = {'User-Agent': user_agent}
shopURL = "https://www.speedwaymotors.com/BluePrint-BP454CT-B-B-Chevy-454-Cruiser-Crate-Engine-Longblock,507450.html"

singleProductPage = requests.get(shopURL, headers=headers).text
soup = BeautifulSoup(singleProductPage, 'html.parser')

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


# from deep_translator import GoogleTranslator
# translated = GoogleTranslator(source='french', target='english').translate_file('QUARTER-TURN1.csv')
