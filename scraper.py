from bs4 import BeautifulSoup
import requests

# Grab html data from url
url = "https://news.ycombinator.com/"
page = requests.get(url)

# Create BeautifulSoup object using html file
soup = BeautifulSoup(page.text, "lxml")

# Grab article titles
def scrape_article_titles():
    titles = [title.next_element for title in soup.find_all("a", "storylink")]
    return titles

# Grab article links
def scrape_article_links():
    links  = [link['href'] for link in soup.find_all("a", "storylink")]
    return links

# Grab article scores
def scrape_article_scores():
    scores = []
    temp_num = ""
    for score in soup.find_all("span", "score"):
        temp_score = score.next_element
        for char in temp_score:
            if char.isdigit():
                temp_num += char
            else:
                scores.append(int(temp_num))
                temp_num = ""
                break

    return scores