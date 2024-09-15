import discord
from discord.ext import commands
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

    @commands.slash_command(name="track", description="Find member messages on channels")
    async def track(self, ctx: discord.ApplicationContext, member: discord.Member, *channels: discord.TextChannel):
        if not channels:
            await ctx.send("Please provide at least one channel.")
            return

        try:
            print(f'Getting data for user: {member.display_name}')
            channel_ids = [channel.id for channel in channels]
            messages = await fetch_user_messages(self.bot, member.id, channel_ids)
            pages = paginate_messages(messages)

            for page in pages:
                await ctx.send(page)
        except Exception as e:
            await ctx.send(f"An error occurred: {str(e)}")

async def setup(bot):
    await bot.add_cog(BotCommands(bot))
