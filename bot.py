"""
Tempo Smart Contract Security Analyzer Bot
Main entry point for the Discord bot
"""
import discord
from discord.ext import commands
import asyncio
import logging
import sys
import io
from config import DISCORD_TOKEN, DISCORD_GUILD_ID

# Fix Windows console encoding for Unicode characters
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TempoAnalyzerBot(commands.Bot):
    """Main bot class for Tempo Contract Analyzer"""
    
    def __init__(self):
        # Use minimal intents - only what's needed for slash commands
        intents = discord.Intents.default()
        intents.message_content = False  # Not needed for slash commands
        
        super().__init__(
            command_prefix='!',
            intents=intents,
            help_command=None
        )
        
    async def setup_hook(self):
        """Load cogs and sync commands"""
        logger.info("Loading cogs...")
        
        try:
            await self.load_extension('cogs.contract_analysis')
            logger.info("✓ Loaded contract_analysis cog")
        except Exception as e:
            logger.error(f"✗ Failed to load contract_analysis cog: {e}")
            raise
        
        # Sync commands globally or to specific guild for testing
        if DISCORD_GUILD_ID:
            guild = discord.Object(id=int(DISCORD_GUILD_ID))
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
            logger.info(f"✓ Synced commands to guild {DISCORD_GUILD_ID}")
        else:
            await self.tree.sync()
            logger.info("✓ Synced commands globally")
    
    async def on_ready(self):
        """Called when bot is ready"""
        logger.info(f'✓ Logged in as {self.user} (ID: {self.user.id})')
        logger.info(f'✓ Connected to {len(self.guilds)} guild(s)')
        
        # Set activity status
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="Tempo contracts | /analyze-contract"
            )
        )
        logger.info('✓ Bot is ready!')
    
    async def on_error(self, event_method, *args, **kwargs):
        """Handle errors"""
        logger.error(f"Error in {event_method}", exc_info=True)

def main():
    """Main entry point"""
    bot = TempoAnalyzerBot()
    
    try:
        bot.run(DISCORD_TOKEN, log_handler=None)
    except KeyboardInterrupt:
        logger.info("Bot shutdown requested by user")
    except Exception as e:
        logger.critical(f"Fatal error: {e}", exc_info=True)

if __name__ == '__main__':
    main()
