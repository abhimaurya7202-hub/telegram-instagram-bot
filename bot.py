import os
import json
import requests
import time
from datetime import datetime

# Configuration
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
BHINDI_API_KEY = os.environ.get('BHINDI_API_KEY')

TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

def send_telegram_message(text, chat_id=None):
    """Send text message to Telegram"""
    url = f"{TELEGRAM_API}/sendMessage"
    payload = {
        'chat_id': chat_id or TELEGRAM_CHAT_ID,
        'text': text,
        'parse_mode': 'HTML'
    }
    response = requests.post(url, json=payload)
    return response.json()

def send_telegram_video(video_url, caption, chat_id=None):
    """Send video to Telegram"""
    url = f"{TELEGRAM_API}/sendVideo"
    payload = {
        'chat_id': chat_id or TELEGRAM_CHAT_ID,
        'video': video_url,
        'caption': caption,
        'parse_mode': 'HTML'
    }
    response = requests.post(url, json=payload)
    return response.json()

def scrape_instagram_profile(username):
    """Scrape Instagram profile using Bhindi API"""
    url = "https://api.bhindi.io/instagram-scraper/scrapeInstagramPosts"
    
    headers = {
        'Authorization': f'Bearer {BHINDI_API_KEY}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        'search': username,
        'searchType': 'user',
        'resultsLimit': 5
    }
    
    print(f"🔍 Scraping Instagram profile: @{username}")
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")
        return None

def get_telegram_updates(offset=None):
    """Get new messages from Telegram"""
    url = f"{TELEGRAM_API}/getUpdates"
    params = {'offset': offset, 'timeout': 30}
    response = requests.get(url, params=params)
    return response.json()

def process_videos(data, username):
    """Extract and send videos from scraped data"""
    if not data or 'data' not in data:
        return []
    
    videos = []
    posts = data.get('data', [])
    
    for post in posts:
        if post.get('type') == 'video' or post.get('videoUrl'):
            video_url = post.get('videoUrl') or post.get('displayUrl')
            if video_url:
                videos.append({
                    'url': video_url,
                    'caption': post.get('caption', '')[:200],
                    'likes': post.get('likesCount', 0),
                    'comments': post.get('commentsCount', 0)
                })
    
    return videos[:5]  # Return max 5 videos

def main():
    """Main bot logic"""
    print("🤖 Telegram Instagram Bot Started!")
    
    # Check for pending requests file
    if os.path.exists('pending_requests.json'):
        with open('pending_requests.json', 'r') as f:
            requests_data = json.load(f)
            
        for request in requests_data.get('requests', []):
            username = request.get('username')
            chat_id = request.get('chat_id')
            
            print(f"\n📥 Processing request for: @{username}")
            send_telegram_message(f"🔄 Scraping Instagram profile: @{username}\nPlease wait...", chat_id)
            
            # Scrape Instagram
            data = scrape_instagram_profile(username)
            
            if data:
                videos = process_videos(data, username)
                
                if videos:
                    send_telegram_message(f"✅ Found {len(videos)} videos from @{username}!\nSending them now...", chat_id)
                    
                    for i, video in enumerate(videos, 1):
                        caption = f"📹 Video {i}/5 from @{username}\n"
                        caption += f"❤️ {video['likes']} likes | 💬 {video['comments']} comments\n\n"
                        caption += video['caption'][:100] + "..." if len(video['caption']) > 100 else video['caption']
                        
                        try:
                            send_telegram_video(video['url'], caption, chat_id)
                            time.sleep(2)  # Avoid rate limits
                        except Exception as e:
                            print(f"❌ Error sending video {i}: {e}")
                            send_telegram_message(f"⚠️ Could not send video {i}. URL: {video['url']}", chat_id)
                    
                    send_telegram_message(f"✅ All videos sent from @{username}!", chat_id)
                else:
                    send_telegram_message(f"❌ No videos found for @{username}. They might have only photos or private account.", chat_id)
            else:
                send_telegram_message(f"❌ Failed to scrape @{username}. Please check if the username is correct.", chat_id)
        
        # Clear processed requests
        os.remove('pending_requests.json')
        print("\n✅ All requests processed!")
    else:
        print("ℹ️ No pending requests found.")

if __name__ == '__main__':
    main()
