import os
import discord
from discord.ext import commands
import requests
import datetime

DISCORD_BOT_TOKEN=os.environ.get('DISCORD_BOT_TOKEN')

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

bot = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    while True:
        if datetime.datetime.now().second in [0,30]:
            res = requests.get('https://weazel-subscriptions.herokuapp.com/discord_roles').json()
            guild = client.get_guild(829100503022960650)
            role = discord.utils.get(guild.roles,name="Subscriber")
            members = []
            async for member in guild.fetch_members(limit=None):
                members.append((member, f'{member.name}#{member.discriminator}'))
            for member in members:
                if member[1] not in res:
                    await removerole(ctx=client, user=member[0], role=role)
                else:
                    await giverole(ctx=client, user=member[0], role=role)

@bot.command(pass_context=True)
async def giverole(ctx, user: discord.Member, role: discord.Role):
    await user.add_roles(role)

@bot.command(pass_context=True)
async def removerole(ctx, user: discord.Member, role: discord.Role):
    await user.remove_roles(role)

client.run(DISCORD_BOT_TOKEN)