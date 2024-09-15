import discord
from discord.ext import commands
from discord import app_commands
from utils.message_fetcher import fetch_user_messages
from utils.pagination import paginate_messages

class BotCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Logged in as {self.bot.user.name}')

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
         print(f'Joined guild: {guild.name}')

    @app_commands.command(name="track", description="Find member messages on channels")
    async def track(self, interaction: discord.Interaction, member: discord.Member, channels: str):
        channel_ids = [int(id.strip()) for id in channels.split(",")]
        if not channels:
            await interaction.response.send_message("Please provide at least one channel.")
            return

        try:
            print(f'Getting data for user: {member.display_name}')
            messages = await fetch_user_messages(self.bot, member.id, channel_ids)
            pages = paginate_messages(messages)

            for page in pages:
                await interaction.response.send_message(page)
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {str(e)}")

async def setup(bot):
    await bot.add_cog(BotCommands(bot))
