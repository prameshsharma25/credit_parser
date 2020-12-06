from bs4 import BeautifulSoup
from pymongo import MongoClient
from typing import List, Dict
import requests
import smtplib
import ssl
import getpass

class Scraper:
    def __init__(self) -> None:
        self.url = "https://news.ycombinator.com/"
        self.page = requests.get(self.url)       
        self.soup = BeautifulSoup(self.page.text, "lxml")

    def scrape_article_data(self) -> List[Dict[str, str]]:
        articles = []
        links  = [link['href'] for link in self.soup.find_all("a", "storylink")]
        titles = [title.next_element for title in self.soup.find_all("a", "storylink")]
        temp_num = ""
        index = 0
        for score in self.soup.find_all("span", "score"):
            temp_score = score.next_element
            for char in temp_score:
                if char.isdigit():
                    temp_num += char
                else:
                    articles.append({
                        "title": titles[index],
                        "link": links[index],
                        "score": int(temp_num)
                    })
                    temp_num = ""
                    index += 1
                    break
        
        return articles

    def store_articles_in_database(self, articles: List[Dict[str, str]]) -> List[Dict[str, str]]:
        client = MongoClient()
        db = client.scraped_database

        # Create collection
        collection = db.articles

        # Delete any lingering data
        if collection.count_documents({}) > 0:
            collection.delete_many({})

        # Save scraped data in db
        for article in articles:
            collection.insert_one(article)
        
        return collection

    def sort_articles_by_score(self, collection: List[Dict[str, str]]) -> List[Dict[str, str]]:
        return [list(article.values()) for article in collection.find().sort("score", -1)]

    def write_articles_to_file(self, sorted_articles: List[Dict[str, str]]) -> None:
        # Write data to a file
        with open("email.txt", 'w') as f:
            for article in sorted_articles[0:4]:
                f.write(f"Title: {article[1]} \nLink: {article[2]} \nPoints: {article[3]} \n\n")

    def send_articles_in_email(self) -> None:
        port = 587
        smtp_server = "smtp.gmail.com"
        sender_email = "prameshsharma256@gmail.com"
        receiver_email = "prameshsharma25@gmail.com"
        password = "agQp3q\"H5JN`F>J*>}*~"

        #password = getpass.getpass(prompt="Password: ")
        
        with open("email.txt", "r") as f:
            message = f.read()

        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls(context=context)
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.encode("utf-8"))

def main() -> None:
    scraper = Scraper()
    data = scraper.scrape_article_data()
    current_collection = scraper.store_articles_in_database(data)
    sorted_articles = scraper.sort_articles_by_score(current_collection)
    scraper.write_articles_to_file(sorted_articles)
    scraper.send_articles_in_email()

if __name__ == "__main__":
    main()
