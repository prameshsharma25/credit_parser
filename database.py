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

# Store in order of most popular articles
sorted_articles = [list(article.values()) for article in collection.find().sort("score", -1)]

# Write data to a file
with open("email.txt", 'w') as f:
    for article in sorted_articles[:3]:
        f.write(article[1] + "\n" + article[2] + "\n\n")
