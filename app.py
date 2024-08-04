from dotenv import load_dotenv
load_dotenv()
import os
import streamlit as st
import feedparser
from telegram import Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, filters
import threading

# Function to fetch news from NDTV RSS feed
def fetch_news():
    feed_url = "https://feeds.feedburner.com/ndtvnews-latest"
    feed = feedparser.parse(feed_url)
    news_items = []
    for entry in feed.entries[:5]:  # Get the latest 5 news items
        news_items.append(f"{entry.title}\n{entry.link}")
    return "\n\n".join(news_items)
# Telegram bot handlers
def start(update, context):
    update.message.reply_text('Hi! I can provide you with the latest news from NDTV. Type /news to get the latest news.')

def news(update, context):
    news = fetch_news()
    update.message.reply_text(news)

def main():
    # Replace 'YOUR_BOT_TOKEN_HERE' with your actual bot token
    token = os.getenv("BOT_API_KEY")
    
    updater = Updater(token)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('news', news))

    updater.start_polling()
    updater.idle()

# Function to start the bot in a separate thread
def start_bot():
    bot_thread = threading.Thread(target=main)
    bot_thread.start()
    return bot_thread

# Streamlit interface
st.title("NDTV News Telegram Bot")
st.write("This app allows you to manage a Telegram bot that fetches the latest news from NDTV.")

if st.button('Start Bot'):
    bot_thread = start_bot()
    st.write("Bot started!")

if st.button('Fetch Latest News'):
    news = fetch_news()
    st.write(news)
