import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from django.conf import settings
from django.contrib.auth.models import User
from api.models import UserProfile, Post
from asgiref.sync import sync_to_async

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class DjangoTelegramBot:
    def __init__(self):
        self.application = None
        
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send a message when the command /start is issued."""
        user = update.effective_user
        welcome_message = f"""
🎉 Welcome to Django Bot, {user.first_name}!

I'm connected to a Django backend and can help you with:

🔹 /start - Show this welcome message
🔹 /help - Get help information
🔹 /stats - Get platform statistics
🔹 /profile - Link your Telegram account
🔹 /posts - Get latest posts from the platform

Type any message to get a response from the Django backend!
        """
        await update.message.reply_text(welcome_message)

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send a message when the command /help is issued."""
        help_text = """
🤖 Django Bot Help

Available Commands:
• /start - Welcome message and bot introduction
• /help - This help message
• /stats - Get platform statistics
• /profile - Link your Telegram account to Django user
• /posts - Get latest posts from the platform

Features:
✅ Connected to Django REST API
✅ Real-time data from Django backend
✅ User authentication integration
✅ Secure data handling

For more information, visit our platform or contact support.
        """
        await update.message.reply_text(help_text)

    @sync_to_async
    def get_platform_stats(self):
        """Get platform statistics from Django models."""
        try:
            total_users = User.objects.count()
            total_posts = Post.objects.count()
            published_posts = Post.objects.filter(is_published=True).count()
            profiles_with_telegram = UserProfile.objects.exclude(telegram_user_id__isnull=True).exclude(telegram_user_id__exact='').count()
            
            return {
                'total_users': total_users,
                'total_posts': total_posts,
                'published_posts': published_posts,
                'telegram_users': profiles_with_telegram,
            }
        except Exception as e:
            logger.error(f"Error getting platform stats: {e}")
            return None

    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Get platform statistics."""
        stats = await self.get_platform_stats()
        
        if stats:
            stats_message = f"""
📊 Platform Statistics

👥 Total Users: {stats['total_users']}
📝 Total Posts: {stats['total_posts']}
✅ Published Posts: {stats['published_posts']}
📱 Telegram Users: {stats['telegram_users']}

Data fetched from Django backend in real-time!
            """
        else:
            stats_message = "❌ Sorry, couldn't fetch statistics at the moment. Please try again later."
        
        await update.message.reply_text(stats_message)

    @sync_to_async
    def link_telegram_user(self, telegram_user_id, username):
        """Link Telegram user to Django user profile."""
        try:
            # Try to find existing user by username
            user = User.objects.filter(username=username).first()
            if user:
                profile, created = UserProfile.objects.get_or_create(user=user)
                profile.telegram_user_id = str(telegram_user_id)
                profile.save()
                return True, f"Successfully linked to user: {username}"
            else:
                return False, f"User '{username}' not found in the system."
        except Exception as e:
            logger.error(f"Error linking Telegram user: {e}")
            return False, "An error occurred while linking your account."

    async def profile_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Link Telegram account to Django user."""
        user = update.effective_user
        
        if context.args:
            username = context.args[0]
            success, message = await self.link_telegram_user(user.id, username)
            
            if success:
                response = f"✅ {message}\n\nYour Telegram account is now linked to the Django platform!"
            else:
                response = f"❌ {message}\n\nPlease make sure you have an account on the platform first."
        else:
            response = """
🔗 Link Your Account

To link your Telegram account to the Django platform, use:
/profile <your_username>

Example: /profile john_doe

This will connect your Telegram account to your Django user profile.
            """
        
        await update.message.reply_text(response)

    @sync_to_async
    def get_latest_posts(self, limit=5):
        """Get latest published posts from Django."""
        try:
            posts = Post.objects.filter(is_published=True).order_by('-created_at')[:limit]
            return [
                {
                    'title': post.title,
                    'author': post.author.username,
                    'created_at': post.created_at.strftime('%Y-%m-%d %H:%M'),
                    'content_preview': post.content[:100] + '...' if len(post.content) > 100 else post.content
                }
                for post in posts
            ]
        except Exception as e:
            logger.error(f"Error getting latest posts: {e}")
            return None

    async def posts_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Get latest posts from the platform."""
        posts = await self.get_latest_posts()
        
        if posts:
            if posts:
                message = "📝 Latest Posts from Django Platform:\n\n"
                for i, post in enumerate(posts, 1):
                    message += f"{i}. **{post['title']}**\n"
                    message += f"   👤 By: {post['author']}\n"
                    message += f"   📅 {post['created_at']}\n"
                    message += f"   📄 {post['content_preview']}\n\n"
            else:
                message = "📝 No posts available at the moment."
        else:
            message = "❌ Sorry, couldn't fetch posts at the moment. Please try again later."
        
        await update.message.reply_text(message, parse_mode='Markdown')

    async def echo(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Echo the user message with Django backend info."""
        user_message = update.message.text
        user = update.effective_user
        
        response = f"""
🤖 Django Bot Response

Your message: "{user_message}"

👤 Telegram User: {user.first_name} {user.last_name or ''}
🆔 User ID: {user.id}
🕐 Received at: {update.message.date}

This response is generated by the Django-connected Telegram bot!

Use /help to see available commands.
        """
        
        await update.message.reply_text(response)

    def setup_handlers(self):
        """Set up command and message handlers."""
        if not self.application:
            return
            
        # Command handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("stats", self.stats_command))
        self.application.add_handler(CommandHandler("profile", self.profile_command))
        self.application.add_handler(CommandHandler("posts", self.posts_command))
        
        # Message handler for non-command messages
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.echo))

    async def start_bot(self):
        """Start the Telegram bot."""
        if not settings.TELEGRAM_BOT_TOKEN:
            logger.error("TELEGRAM_BOT_TOKEN not found in settings")
            return
            
        # Create the Application
        self.application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()
        
        # Set up handlers
        self.setup_handlers()
        
        # Start the bot
        logger.info("Starting Telegram bot...")
        await self.application.initialize()
        await self.application.start()
        await self.application.updater.start_polling()
        
        # Keep the bot running
        try:
            await asyncio.Event().wait()
        except KeyboardInterrupt:
            logger.info("Stopping Telegram bot...")
        finally:
            await self.application.updater.stop()
            await self.application.stop()
            await self.application.shutdown()


# Global bot instance
telegram_bot = DjangoTelegramBot()


def run_bot():
    """Run the Telegram bot."""
    asyncio.run(telegram_bot.start_bot())