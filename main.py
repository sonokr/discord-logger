import datetime
import os
from os import environ

import discord
from discord.ext import commands
from dislash import slash_commands
from dotenv import load_dotenv

load_dotenv(".env")
TOKEN = environ.get("TOKEN", "")
channel_id = int(environ.get("DEFAULT_CHANNEL_ID", 0))
default_guild_id = int(environ.get("DEFAULT_GUILD_ID", ""))

intents = discord.Intents.all()
client = commands.Bot(command_prefix="/")
slash = slash_commands.SlashClient(client)

# TODO: make channel_id changeable
channel = client.get_channel(channel_id)

guild_ids = [default_guild_id]


@client.event
async def on_ready() -> None:
    print("Logged in.")
    global channel
    channel = client.get_channel(channel_id)


@slash.command(name="neko", description="ねこだよ", guild_ids=guild_ids)
async def neko(ctx):
    await ctx.reply("にゃ〜ん")


@client.event
async def on_voice_state_update(member, before, after):
    if before.channel == after.channel:
        return

    if before.channel != None:  # When member left.
        voice_channel = before.channel
        status = "left"
    elif after.channel != None:  # When member joined.
        voice_channel = after.channel
        status = "joined"
    embed = discord.Embed(title="")
    embed.set_author(name=member, icon_url=member.avatar_url)
    embed.add_field(
        name="Voice channel status update",
        value=f"\
{member.mention} {status} {voice_channel.mention}\n\
```text\nuser = {member.id}\nchannel = {voice_channel.id}```",
        inline=False,
    )
    now = datetime.datetime.now()
    now_str = f"{now.year}/{now.month}/{now.day} {now.hour}:{now.minute}:{now.second}"
    embed.set_footer(text=f"{client.user} • {now_str}", icon_url=client.user.avatar_url)

    await channel.send(embed=embed)


client.run(TOKEN)
