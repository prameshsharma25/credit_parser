from pymongo import MongoClient
from scraper import Scraper

# Create Mongo Database
client = MongoClient()
db = client.scraped_database

# Call Scraper Object
web_scraper = Scraper()

#Store scraped data
titles = web_scraper.scrape_article_titles()
links = web_scraper.scrape_article_links()
scores = web_scraper.scrape_article_scores()

# Create collection
collection = db.articles

# Delete collection data
if collection.count_documents({}) > 0:
    collection.delete_many({})

# Save scraped data in db
for item in range(0, len(titles)-1):
    data = {
    "title": titles[item],
    "link": links[item],
    "score": scores[item]
    }

    collection.insert_one(data)

# Sort articles by scores in descending order
sorted_articles = collection.find().sort("score", -1)
