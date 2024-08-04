from dotenv import load_dotenv
import os
import streamlit as st
import feedparser
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackContext, filters
import threading

# Load environment variables from .env file
load_dotenv()
BOT_API_KEY = os.getenv("BOT_API_KEY")

# Function to fetch news from NDTV RSS feed
def fetch_news(query=None):
    feed_url = "https://feeds.feedburner.com/ndtvnews-latest"
    feed = feedparser.parse(feed_url)
    news_items = []
    
    for entry in feed.entries:
        if query is None or query.lower() in entry.title.lower():
            news_items.append(f"{entry.title}\n{entry.link}")
        if len(news_items) >= 5:  # Limit to the latest 5 news items
            break
            
    if not news_items:
        return "No news found for your query."
        
    return "\n\n".join(news_items)

# Telegram bot handlers
def start(update: Update, context: CallbackContext):
    update.message.reply_text('Hi! I can provide you with the latest news from NDTV. Type any keyword to get related news.')

def handle_message(update: Update, context: CallbackContext):
    query = update.message.text
    news = fetch_news(query)
    update.message.reply_text(news)

def main():
    # Create the bot application
    app = ApplicationBuilder().token(BOT_API_KEY).build()
    
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    app.run_polling()

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
