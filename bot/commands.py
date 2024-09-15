import traceback
import discord
import asyncio
import logging
from discord.ext import commands
from discord import HTTPException, app_commands

# Reuse the logger that was configured in main.py
logger = logging.getLogger(__name__)

class BotCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f'Logged in as {self.bot.user.name}')

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
         logger.info(f'Joined guild: {guild.name}')

    @app_commands.command(name="track", description="Find member messages on channels")
    async def track(self, interaction: discord.Interaction, member: discord.Member, channels: str):

        channel_ids = [int(id.strip()) for id in channels.split(",")]
        if not channels:
            await interaction.response.send_message("Please provide at least one channel.")
            return

        try:
            messages = {}
            invalid_channels = []
            logger.info(f'Getting data for user: {member.display_name}')
            for channel_id in channel_ids:
                channel = self.bot.get_channel(channel_id)
                if not channel:
                    invalid_channels.append(channel_id)
                    continue
                channel_name, count = await fetch_user_messages(self.bot, member.id, channel)
                messages[channel_name] = count
            
            
            if messages:
                response_message = "The following channels have messages: \n"    
                response_message += "\n".join(f"{channel}: {count} messages" for channel, count in messages.items())
                response_message += "\n-------------------------------\n" 
            # Send summary of valid and invalid channels
            if invalid_channels:
                response_message += f"Some channels were not found: {', '.join(map(str, invalid_channels))}\n"
            await interaction.response.send_message(response_message)
   
        except Exception as e:
            # Log the full stack trace for debugging purposes
            logger.error("An error occurred: %s", e)
            traceback.print_exc()
            await interaction.response.send_message("An error occurred while processing your request. Please try again later.")


async def fetch_user_messages(bot, user_id, channel):
    count = 0
    try:
        async for message in channel.history(limit=None):
            if message.author.id == user_id:
                count += 1

    except HTTPException as e:
        if e.status == 429:  # Rate limit error
            retry_after = e.retry_after
            logger.warn(f"Rate limited. Waiting for {retry_after} seconds.")
            await asyncio.sleep(retry_after)
        else:
            logger.error(f"HTTP error occurred: {e}")

    return (channel.name, count)


    return message_counts

async def setup(bot):
    await bot.add_cog(BotCommands(bot))
