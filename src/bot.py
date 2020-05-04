from private_token import token
from random import randrange
import discord
import requests
import json

codeforces_problems = requests.get("https://codeforces.com/api/problemset.problems").json()
codeforces_ids = codeforces_problems["result"]["problems"]

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
    
    if message.content.startswith('!problem codeforces'):
        choice = randrange(len(codeforces_ids))
        link = "https://codeforces.com/problemset/problem/" + str(codeforces_ids[choice]["contestId"]) + "/" + codeforces_ids[choice]["index"]
        await message.channel.send("<:codeforces:704170636049645639> " + codeforces_ids[choice]["name"] + " - " + link)

client.run(token)