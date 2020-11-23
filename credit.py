from bs4 import BeautifulSoup
import requests

# Grab html data from url
url = "http://chase.com"
page = requests.get(url)

# Create BeautifulSoup object using html file
soup = BeautifulSoup(page.text, "lxml")

# Write html data into file.txt
with open("file.txt", 'w') as f:
    f.writelines(soup.prettify())
