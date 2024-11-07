import feedparser
import time

# List of RSS feeds
rss_feeds = [
    "https://www.ft.com/news-feed?format=rss",
    "https://www.forbes.com/most-popular/feed/",
    "https://www.cnbc.com/id/10001147/device/rss/rss.html",
    # (Add the rest of your 50 RSS feed links here)
]

# Function to extract the latest 10 posts from an RSS feed and yield each post
def extract_posts(feed_url):
    feed = feedparser.parse(feed_url)
    for entry in feed.entries[:10]:  # Limit to 10 entries per feed
        title = entry.get("title", "No Title")
        content = entry.get("description", "No Content")
        image_url = None
        # Attempt to retrieve image from media content or summary
        if 'media_content' in entry:
            image_url = entry.media_content[0]['url']
        elif 'summary' in entry:
            image_url = extract_image_from_summary(entry.summary)
        
        yield {"title": title, "content": content, "image_url": image_url}

# Function to extract image URL from entry summary
def extract_image_from_summary(summary):
    import re
    match = re.search(r'src="(.*?)"', summary)
    return match.group(1) if match else None

# Function to process each post
def process_post(post):
    # Simulate processing by waiting and printing the title
    print("Processing post:", post["title"])
    time.sleep(5)

# Main function to loop over feeds and process posts
def main():
    while True:
        for feed_url in rss_feeds:
            print(f"Fetching posts from: {feed_url}")
            for post in extract_posts(feed_url):
                process_post(post)

# Run the main function
if __name__ == "__main__":
    main()