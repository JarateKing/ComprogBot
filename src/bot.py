from private_token import token
import discord

client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
    
    if message.content.startswith('!kattis'):
        await message.channel.send("<:kattis:704169451163222128> https://open.kattis.com/")
    
    if message.content.startswith('!codeforces'):
        await message.channel.send("<:codeforces:704170636049645639> https://codeforces.com/")

client.run(token)