import discord
import asyncio
from discord.errors import HTTPException

async def fetch_user_messages(bot, user_id, channel_ids):
    all_messages = []
    user = await bot.fetch_user(user_id)

    for channel_id in channel_ids:
        channel = bot.get_channel(channel_id)
        if not channel:
            print(f"Channel {channel_id} not found.")
            continue

        try:
            async for message in channel.history(limit=None):
                if message.author.id == user_id:
                    all_messages.append(f"[{channel.name}] {message.content}")

        except HTTPException as e:
            if e.status == 429:  # Rate limit error
                retry_after = e.retry_after
                print(f"Rate limited. Waiting for {retry_after} seconds.")
                await asyncio.sleep(retry_after)
            else:
                print(f"HTTP error occurred: {e}")

        await asyncio.sleep(1)  # Add a small delay between requests to avoid rate limits

    return all_messages
