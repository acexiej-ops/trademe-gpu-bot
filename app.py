import os
import time
import threading
import requests
from bs4 import BeautifulSoup
from flask import Flask, request, render_template_string, redirect, url_for

app = Flask(__name__)

# Configuration
CONFIG = {
    "keywords": ["RTX 3070", "RTX 3080", "RTX 3060 Ti", "RTX 4070", "RTX 4080", "RTX 4090"],
    "webhook_url": "https://discordapp.com/api/webhooks/1473576797038972948/UvHkKVEt5CNqlqRzYbOx6WYdPj8ySJN_JftKKrQQ7EafnhH4GHi5BbXcvJ9MIugxI7xZ",
    "interval": 300,
    "seen_ids": set()
}

def send_discord_notification(listing):
    if not CONFIG["webhook_url"]: return
    data = {
        "content": f"🚀 **New GPU Listing Found!**\
**Title:** {listing['title']}\
**Price:** {listing['price']}\
**Link:** {listing['link']}"
    }
    try: requests.post(CONFIG["webhook_url"], json=data)
    except Exception as e: print(f"Error sending to Discord: {e}")

def scrape_trademe():
    print("Scraper started...")
    while True:
        for keyword in CONFIG["keywords"]:
            url = f"https://www.trademe.co.nz/a/marketplace/computers/search?search_string={keyword.replace(' ', '%20')}&sort_order=expirydesc"
            try:
                headers = {'User-Agent': 'Mozilla/5.0'}
                resp = requests.get(url, headers=headers)
                soup = BeautifulSoup(resp.text, 'html.parser')
                listings = soup.find_all('tg-listing-card-v2') # Example selector
                for l in listings:
                    # Simplified extraction logic
                    title = l.get('title') or "Unknown GPU"
                    link = "https://www.trademe.co.nz" + l.find('a')['href']
                    listing_id = link.split('/')[-1]
                    if listing_id not in CONFIG["seen_ids"]:
                        CONFIG["seen_ids"].add(listing_id)
                        send_discord_notification({'title': title, 'price': 'Check link', 'link': link})
            except Exception as e: print(f"Scrape error: {e}")
        time.sleep(CONFIG["interval"])

@app.route('/')
def index():
    return "<h1>TradeMe GPU Bot is Running</h1><p>Monitoring for: " + ", ".join(CONFIG['keywords']) + "</p>"

if __name__ == '__main__':
    threading.Thread(target=scrape_trademe, daemon=True).start()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
