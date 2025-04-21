import feedparser
import json
import time  # Import the time module
import re  # Importing regex for HTML parsing
# Rappler RSS Feed URL
rss_url = "https://factcheck.thecable.ng/feed/"
# Parse RSS Feed
feed = feedparser.parse(rss_url)
# Initialize the articles dictionary
articles = {"articles": {}}
# Function to remove HTML tags from text
def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)
# Loop through RSS entries and store in the dictionary
for index, entry in enumerate(feed.entries):
    # Extract full text from content or description
    full_text = entry.content[0].value if 'content' in entry else entry.description
    full_text = remove_html_tags(full_text)  # Clean HTML tags
    lang = "en"
    categories = [t for t in entry.tags]
    #print(categories)
    #exit()
    
    dfs = entry.published_parsed
    date = f'{dfs[0]}-{"{:02d}".format(dfs[1])}-{"{:02d}".format(dfs[2])} {"{:02d}".format(dfs[3])}:{"{:02d}".format(dfs[4])}:{"{:02d}".format(dfs[5])}'
    
    if {'term': 'News in Yorùbá', 'scheme': None, 'label': None} in categories:
        lang = "yo"
    elif {'term': 'News in Hausa', 'scheme': None, 'label': None} in categories:
        lang = "ha"
    elif {'term': 'News in pidgin', 'scheme': None, 'label': None} in categories:
        lang = "pcm"
    elif {'term': 'News in Igbo', 'scheme': None, 'label': None} in categories:
        lang = "ig"
    
    articles["articles"][str(index)] = {
        "title": entry.title,
        "text": full_text.strip(),  # Use full text if available and strip whitespace
        "author": entry.author,
        "date_published": date,
        "unix_date_published": time.mktime(entry.published_parsed) if entry.published_parsed else None,  # Corrected to use time.mktime
        "organization_country": "Nigeria",  # Assuming the organization is based in the Philippines
        "site_name": "CableCheck",
        "url": entry.link,
        "language": lang,  # Assuming English for all articles
    }
# Save articles to a local JSON file
with open("CableCheck.json", "w", encoding='utf-8') as json_file:
    json.dump(articles, json_file, indent=4, ensure_ascii=False)