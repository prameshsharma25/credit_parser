from bs4 import BeautifulSoup
from pymongo import MongoClient
import requests
import smtplib
import ssl
import getpass

url = "https://news.ycombinator.com/"
page = requests.get(url)       
soup = BeautifulSoup(page.text, "lxml")

def scrape_article_titles():
    """Scrapes articles from ycombinator

    """
    titles = [title.next_element for title in soup.find_all("a", "storylink")]
    return titles

def scrape_article_links():
    links  = [link['href'] for link in soup.find_all("a", "storylink")]
    return links

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

def store_articles_in_database():
    client = MongoClient()
    db = client.scraped_database

    #Store scraped data
    titles = scrape_article_titles()
    links  = scrape_article_links()
    scores = scrape_article_scores()

    # Create collection
    collection = db.articles

    # Delete collection data
    if collection.count_documents({}) > 0:
        collection.delete_many({})

    # Save scraped data in db
    for item in range(len(titles)-1):
        data = {
        "title": titles[item],
        "link": links[item],
        "score": scores[item]
        }

        collection.insert_one(data)
    
    return collection

def sort_articles_by_score(collection):
    return [list(article.values()) for article in collection.find().sort("score", -1)]

def write_articles_to_file(sorted_articles):
    # Write data to a file
    with open("email.txt", 'w') as f:
        for article in sorted_articles[:3]:
            f.write(f"{article[1]} \n {article[2]} \n Points: {article[3]} \n\n")

def send_articles_in_email():
    port = 587
    smtp_server = "smtp.gmail.com"
    sender_email = "prameshsharma256@gmail.com"
    receiver_email = "prameshsharma256@gmail.com"
    password = getpass.getpass(prompt="Password: ")
    
    with open("email.txt", "r") as f:
        message = f.read()

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls(context=context)
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.encode("utf-8"))

def main():
    current_collection = store_articles_in_database()
    sorted_articles = sort_articles_by_score(current_collection)
    write_articles_to_file(sorted_articles)
    send_articles_in_email()

if __name__ == "__main__":
    main()
