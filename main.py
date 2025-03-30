import asyncio
import requests
import time
import json
import os
from telegram import _bot
import logging
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configuration
WORDPRESS_API_URL = "https://conscordoba.esteri.it/wp-json/wp/v2/posts"
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_USER_ID = os.getenv("TELEGRAM_USER_ID")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "600"))
DATA_FILE = os.getenv("DATA_FILE", "last_post_data.json")


class WordPressMonitor:
    def __init__(self, wp_api_url, telegram_token, user_id, check_interval):
        self.wp_api_url = wp_api_url
        self.bot = _bot.Bot(token=telegram_token)
        self.user_id = user_id
        self.check_interval = check_interval
        self.last_post_id = None
        self.load_last_post_data()

    def load_last_post_data(self):
        """Load previously saved data or initialize if not exists"""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r') as f:
                    data = json.load(f)
                    self.last_post_id = data.get('last_post_id')
                    logger.info(f"Loaded last post ID: {self.last_post_id}")
            except Exception as e:
                logger.error(f"Error loading data file: {e}")
        else:
            # Initialize with current latest post
            self.get_latest_post_id()
            self.save_last_post_data()

    def save_last_post_data(self):
        """Save current state to file"""
        try:
            with open(DATA_FILE, 'w') as f:
                json.dump({'last_post_id': self.last_post_id}, f)
        except Exception as e:
            logger.error(f"Error saving data file: {e}")

    def get_latest_post_id(self):
        """Get the ID of the most recent post"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(f"{self.wp_api_url}?per_page=1", headers=headers)
            if response.status_code == 200:
                posts = response.json()
                if posts:
                    self.last_post_id = posts[0]['id']
                    logger.info(f"Latest post ID: {self.last_post_id}")
                    return True
                else:
                    logger.warning("No posts found")
            else:
                logger.error(f"API request failed with status code {response.status_code}")
            return False
        except Exception as e:
            logger.error(f"Error fetching posts: {e}")
            return False

    async def check_for_new_posts(self):
        """Check for new posts and send notification if found"""
        try:
            # Get latest posts
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(f"{self.wp_api_url}?per_page=5", headers=headers)
            if response.status_code != 200:
                logger.error(f"Failed to get posts: HTTP {response.status_code}")
                return

            posts = response.json()
            if not posts:
                logger.info("No posts found")
                return

            new_posts = []
            latest_id = None

            # Find posts newer than the last one we processed
            for post in posts:
                post_id = post['id']

                # Track the latest ID we've seen
                if latest_id is None or post_id > latest_id:
                    latest_id = post_id

                # If we haven't seen any posts yet or this post is newer than our last seen
                if self.last_post_id is None or post_id > self.last_post_id:
                    new_posts.append(post)

            # Update latest post ID if needed
            if latest_id and latest_id != self.last_post_id:
                self.last_post_id = latest_id
                self.save_last_post_data()

            # Process new posts (newest first)
            for post in sorted(new_posts, key=lambda x: x['id'], reverse=True):
                await self.notify_new_post(post)

        except Exception as e:
            logger.error(f"Error checking for new posts: {e}")

    async def notify_new_post(self, post):
        """Send notification about new post to Telegram"""
        try:
            # Extract post details
            title = post.get('title', {}).get('rendered', 'New post')
            link = post.get('link', '')

            # Create message
            message = f"🔔 *New Post Published!*\n\n*{title}*\n\n🔗 [Read more]({link})"

            # Send to Telegram
            await self.bot.send_message(
                chat_id=self.user_id,
                text=message,
                parse_mode='Markdown',
                disable_web_page_preview=False
            )
            logger.info(f"Notification sent for post ID: {post['id']}")
        except Exception as e:
            logger.error(f"Error sending notification: {e}")

    async def run(self):
        """Main loop to monitor WordPress site"""
        logger.info("Starting WordPress post monitor")
        while True:
            try:
                await self.check_for_new_posts()
                time.sleep(self.check_interval)
            except KeyboardInterrupt:
                logger.info("Monitor stopped by user")
                break
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                time.sleep(self.check_interval)


if __name__ == "__main__":
    logger.info("Initializing WordPress to Telegram notifier")

    # Validate configuration
    if (TELEGRAM_BOT_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN" or
            TELEGRAM_USER_ID == "YOUR_TELEGRAM_USER_ID"):
        logger.error("Please configure your Telegram bot token and user ID before running")
        exit(1)

    monitor = WordPressMonitor(
        WORDPRESS_API_URL,
        TELEGRAM_BOT_TOKEN,
        TELEGRAM_USER_ID,
        CHECK_INTERVAL
    )
    asyncio.run(monitor.run())
