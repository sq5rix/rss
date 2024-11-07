import feedparser
import sqlite3

# List of RSS feeds
rss_feeds = [
    "https://www.ft.com/news-feed?format=rss",
    "https://www.forbes.com/most-popular/feed/",
    "https://www.cnbc.com/id/10001147/device/rss/rss.html",
    # (Add the rest of your 50 RSS feed links here)
]

# Connect to SQLite database
conn = sqlite3.connect('finance_news.db')
cursor = conn.cursor()

# Create or modify the table to include a status column if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT UNIQUE,
        content TEXT,
        image_url TEXT,
        status TEXT DEFAULT 'new'
    )
''')
conn.commit()

# Function to check if a title exists in the database
def is_new_title(title):
    cursor.execute('SELECT 1 FROM articles WHERE title = ?', (title,))
    return cursor.fetchone() is None

# Function to extract the latest 10 posts from an RSS feed
def extract_posts(feed_url):
    feed = feedparser.parse(feed_url)
    articles = []
    for entry in feed.entries[:10]:  # Limit to 10 entries per feed
        title = entry.get("title", "No Title")
        
        # Skip if title already exists in the database
        if not is_new_title(title):
            continue
        
        content = entry.get("description", "No Content")
        image_url = None
        # Attempt to retrieve image from media content or summary
        if 'media_content' in entry:
            image_url = entry.media_content[0]['url']
        elif 'summary' in entry:
            image_url = extract_image_from_summary(entry.summary)
        
        # Insert article with default status 'new'
        articles.append((title, content, image_url, 'new'))
    return articles

# Function to extract image URL from entry summary
def extract_image_from_summary(summary):
    # A simple way to extract image URLs could be with regex, but you may need a more robust HTML parser.
    import re
    match = re.search(r'src="(.*?)"', summary)
    return match.group(1) if match else None

# Function to update the status of an article by title
def update_status(title, new_status):
    cursor.execute('UPDATE articles SET status = ? WHERE title = ?', (new_status, title))
    conn.commit()

# Process each feed and store articles in SQLite
for feed_url in rss_feeds:
    print(f"Processing feed: {feed_url}")
    articles = extract_posts(feed_url)
    cursor.executemany('INSERT INTO articles (title, content, image_url, status) VALUES (?, ?, ?, ?)', articles)

# Commit initial insertions
conn.commit()

# Example usage of update_status function
update_status("Sample Article Title", "reviewed")  # Replace "Sample Article Title" with an actual title

# Close connection
conn.close()

print("Data extraction complete.")
