from discord.ext import commands
from utils.message_fetcher import fetch_user_messages
from utils.pagination import paginate_messages

class BotCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def track(self, ctx, user_id: int, *channel_ids: int):
        if not channel_ids:
            await ctx.send("Please provide at least one channel ID.")
            return

        try:
            messages = await fetch_user_messages(self.bot, user_id, channel_ids)
            pages = paginate_messages(messages)

            for page in pages:
                await ctx.send(page)
        except Exception as e:
            await ctx.send(f"An error occurred: {str(e)}")

async def setup(bot):
    await bot.add_cog(BotCommands(bot))
