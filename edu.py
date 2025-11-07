import requests
import schedule
import time
from telegram import Bot
import openai

# ====== CONFIG ======
TELEGRAM_TOKEN = "8549345538:AAE4tMbvhKeidaFB2g2KGSmwX84EFu3FNDg"
CHAT_ID = "@EduContentBot2025_bot"
OPENAI_API_KEY = "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"

# Set RSS feed URL directly
RSS_FEED_URL = "https://rsshub.app/instagram/user/mr.wiz73"  # <-- change to your feed URL

# Initialize Telegram and OpenAI
bot = Bot(token=TELEGRAM_TOKEN)
openai.api_key = OPENAI_API_KEY

# ====== HELPER FUNCTIONS ======

def fetch_rss_content(url):
    """Fetch content from RSS feed (returns first 500 chars for demo)."""
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        return resp.text[:500]
    except Exception as e:
        print(f"Error fetching RSS content: {e}")
        return "No content available."

def rewrite_with_chatgpt(text):
    """Use ChatGPT to rewrite content in a clean, educational format for Telegram."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Rewrite this as clean, educational content for Telegram."},
                {"role": "user", "content": text}
            ],
            temperature=0.7,
            max_tokens=300
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error with OpenAI API: {e}")
        return "Unable to process content at this time."

def post_to_telegram(message):
    """Post message to Telegram group."""
    try:
        bot.send_message(chat_id=CHAT_ID, text=message)
    except Exception as e:
        print(f"Error posting to Telegram: {e}")

# ====== MAIN JOB ======
def job():
    print("Fetching content...")
    content = fetch_rss_content(RSS_FEED_URL)
    formatted_content = rewrite_with_chatgpt(content)
    post_to_telegram(formatted_content)
    print("Posted successfully!")

# ====== SCHEDULER ======
schedule.every(1).hours.do(job)  # Run every 1 hour

if __name__ == "__main__":
    print("Bot is running...")
    while True:
        schedule.run_pending()
        time.sleep(10)
