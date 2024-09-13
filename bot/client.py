import discord
from discord.ext import commands

class DiscordBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='!', intents=intents)

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        await self.load_extension('bot.commands')

bot = DiscordBot()
