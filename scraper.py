from bs4 import BeautifulSoup
import requests

# Grab html data from url
url = "https://news.ycombinator.com/"
page = requests.get(url)

# Create BeautifulSoup object using html file
soup = BeautifulSoup(page.text, "lxml")

# Grab all article titles
titles = [title.next_element for title in soup.find_all("a", "storylink")]
scores = [score.next_element for score in soup.find_all("span", "score")]
links  = [link['href'] for link in soup.find_all("a", "storylink")]
