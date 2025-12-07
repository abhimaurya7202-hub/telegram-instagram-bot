import os
import json
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
GITHUB_REPO = os.environ.get('GITHUB_REPO', 'abhimaurya7202-hub/telegram-instagram-bot')

TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        update = json.loads(post_data.decode('utf-8'))
        
        # Process Telegram update
        if 'message' in update:
            message = update['message']
            chat_id = message['chat']['id']
            text = message.get('text', '')
            
            if text.startswith('/start'):
                self.send_response_message(chat_id, 
                    "👋 Welcome to Instagram Video Downloader Bot!\n\n"
                    "📝 Send me an Instagram username (without @) and I'll send you their last 5 videos!\n\n"
                    "Example: <code>cristiano</code>")
            
            elif text.startswith('/'):
                pass  # Ignore other commands
            
            else:
                # Treat as Instagram username
                username = text.strip().replace('@', '')
                
                # Trigger GitHub Actions workflow
                self.trigger_scraping(username, chat_id)
                self.send_response_message(chat_id, 
                    f"✅ Request received for @{username}!\n"
                    f"⏳ Processing... This may take 1-2 minutes.")
        
        self.send_response(200)
        self.end_headers()
    
    def send_response_message(self, chat_id, text):
        url = f"{TELEGRAM_API}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': 'HTML'
        }
        requests.post(url, json=payload)
    
    def trigger_scraping(self, username, chat_id):
        """Trigger GitHub Actions workflow with username"""
        # Create pending request file via GitHub API
        url = f"https://api.github.com/repos/{GITHUB_REPO}/dispatches"
        headers = {
            'Authorization': f'token {GITHUB_TOKEN}',
            'Accept': 'application/vnd.github.v3+json'
        }
        payload = {
            'event_type': 'scrape_request',
            'client_payload': {
                'username': username,
                'chat_id': str(chat_id)
            }
        }
        requests.post(url, headers=headers, json=payload)

def run_server(port=8080):
    server = HTTPServer(('', port), WebhookHandler)
    print(f'🚀 Webhook server running on port {port}')
    server.serve_forever()

if __name__ == '__main__':
    run_server()
