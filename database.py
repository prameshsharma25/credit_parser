from pymongo import MongoClient
from scraper import titles, links, scores

# Database to store scraped data
client = MongoClient()
db = client.scraped_database

# Create collection
collection = db.articles

# Save scraped data in db
for item in range(0, len(titles)-1):
    data = {
    "title": titles[item],
    "link": links[item],
    "score": scores[item]
    }

    collection.insert_one(data)