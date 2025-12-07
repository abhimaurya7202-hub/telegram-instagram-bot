# 🤖 Telegram Instagram Video Downloader Bot

**100% Cloud-based** Telegram bot that scrapes Instagram videos and sends them directly to you!

## ✨ Features

- 📱 Send Instagram username to Telegram bot
- 🎥 Automatically downloads last 5 videos
- 📤 Sends videos directly to your Telegram chat
- ☁️ Fully cloud-based - no local setup needed
- 🆓 Free to use with GitHub Actions

## 🚀 Quick Setup (3 Steps)

### Step 1: Create Telegram Bot

1. Open Telegram and search for [@BotFather](https://t.me/BotFather)
2. Send `/newbot` command
3. Follow instructions to create your bot
4. **Copy the bot token** (looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)
5. Start a chat with your new bot and send any message
6. Get your chat ID by visiting: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
7. Look for `"chat":{"id":123456789}` and **copy the chat ID**

### Step 2: Add Secrets to GitHub

Go to: https://github.com/abhimaurya7202-hub/telegram-instagram-bot/settings/secrets/actions

Add these 3 secrets:

| Secret Name | Value | Where to Get |
|-------------|-------|--------------|
| `TELEGRAM_BOT_TOKEN` | Your bot token from BotFather | Step 1 above |
| `TELEGRAM_CHAT_ID` | Your chat ID | Step 1 above |
| `BHINDI_API_KEY` | Your Bhindi API key | [Bhindi Dashboard](https://bhindi.io) |

### Step 3: Enable GitHub Actions

1. Go to: https://github.com/abhimaurya7202-hub/telegram-instagram-bot/actions
2. Click **"I understand my workflows, go ahead and enable them"**

## 📱 How to Use

### Method 1: Manual Trigger (Easiest)

1. Go to [Actions](https://github.com/abhimaurya7202-hub/telegram-instagram-bot/actions)
2. Click **"Instagram Video Scraper"** workflow
3. Click **"Run workflow"**
4. Enter Instagram username (e.g., `cristiano`)
5. Enter your Telegram chat ID
6. Click **"Run workflow"**
7. Wait 1-2 minutes, videos will be sent to your Telegram!

### Method 2: Automated Bot (Advanced)

For fully automated bot that responds to messages, you need to deploy the webhook:

**Option A: Deploy to Railway (Recommended)**

1. Fork this repository
2. Go to [Railway.app](https://railway.app)
3. Create new project from GitHub repo
4. Add environment variables:
   - `TELEGRAM_BOT_TOKEN`
   - `GITHUB_TOKEN` (create at GitHub Settings → Developer settings → Personal access tokens)
   - `GITHUB_REPO` = `abhimaurya7202-hub/telegram-instagram-bot`
5. Deploy `webhook.py`
6. Copy the Railway URL
7. Run `setup_webhook.py` with `WEBHOOK_URL` set to your Railway URL

**Option B: Deploy to Render**

Similar steps as Railway, deploy to [Render.com](https://render.com)

## 🎯 Usage Examples

Send to your Telegram bot:

```
cristiano
```

Bot will reply:
```
✅ Request received for @cristiano!
⏳ Processing... This may take 1-2 minutes.

🔄 Scraping Instagram profile: @cristiano
Please wait...

✅ Found 5 videos from @cristiano!
Sending them now...

📹 Video 1/5 from @cristiano
❤️ 2.5M likes | 💬 15K comments
...
```

## 🔧 Customization

### Change Number of Videos

Edit `bot.py`, line 73:

```python
return videos[:5]  # Change 5 to any number
```

### Add More Features

Edit `bot.py` to add:
- Download photos
- Get profile stats
- Download stories
- And more!

## 📊 How It Works

```
You → Telegram Bot → GitHub Actions → Instagram Scraper → Videos → Telegram
```

1. You send Instagram username to Telegram bot
2. Bot triggers GitHub Actions workflow
3. Workflow scrapes Instagram using Bhindi API
4. Videos are sent back to your Telegram chat
5. All processing happens in the cloud!

## 🛠️ Troubleshooting

**Bot not responding?**
- Check if all 3 secrets are set correctly
- Verify bot token is valid
- Make sure you started a chat with the bot

**No videos received?**
- Check GitHub Actions logs for errors
- Verify Instagram username is correct
- Account might be private or have no videos

**Workflow failed?**
- Check if BHINDI_API_KEY is valid
- Verify you have API credits remaining

## 💡 Tips

- Bot works best with public Instagram accounts
- Videos are sent directly from Instagram CDN
- No storage needed - everything streams through
- Free tier: ~2000 minutes/month on GitHub Actions

## 🆘 Need Help?

- Check [GitHub Actions logs](https://github.com/abhimaurya7202-hub/telegram-instagram-bot/actions)
- Open an issue on this repository
- Contact Bhindi support

---

Built with ❤️ using [Bhindi](https://bhindi.io) | Powered by GitHub Actions
