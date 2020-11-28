from bs4 import BeautifulSoup
import requests

class Scraper:
    # Set up connection between BeautifulSoup and Ycombinator
    def __init__(self):
        self.url = "https://news.ycombinator.com/"
        self.page = requests.get(self.url)       
        self.soup = BeautifulSoup(self.page.text, "lxml")

    # Grab article titles
    def scrape_article_titles(self):
        titles = [title.next_element for title in self.soup.find_all("a", "storylink")]
        return titles

    # Grab article links
    def scrape_article_links(self):
        links  = [link['href'] for link in self.soup.find_all("a", "storylink")]
        return links

    # Grab article scores
    def scrape_article_scores(self):
        scores = []
        temp_num = ""
        for score in self.soup.find_all("span", "score"):
            temp_score = score.next_element
            for char in temp_score:
                if char.isdigit():
                    temp_num += char
                else:
                    scores.append(int(temp_num))
                    temp_num = ""
                    break

        return scores
