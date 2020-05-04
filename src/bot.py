from private_token import token
from collections import defaultdict
import random
import discord
import requests
import json

codeforces_problems = requests.get("https://codeforces.com/api/problemset.problems").json()
codeforces_ids = codeforces_problems["result"]["problems"]
codeforces_bydifficulty = defaultdict(list)
for i in range(len(codeforces_ids)):
	if "rating" in codeforces_ids[i]:
		codeforces_bydifficulty[codeforces_ids[i]["rating"]].append(i)

client = discord.Client()

@client.event
async def on_message(message):
	# we do not want the bot to reply to itself
	if message.author == client.user:
		return
	
	if message.content.startswith('!kattis'):
		await message.channel.send("<:kattis:704169451163222128> <https://open.kattis.com/>")
	
	if message.content.startswith('!codeforces'):
		await message.channel.send("<:codeforces:704170636049645639> <https://codeforces.com/>")
	
	if message.content.startswith('!problem codeforces'):
		vals = message.content.split()
		choice = random.randrange(len(codeforces_ids))
		num_probs = 1
		output_message = ""
		
		if (len(vals) is 5):
			num_probs = min(20, max(1, int(vals[4])))
			vals.pop()
		
		for iteration in range(num_probs):
			if (len(vals) is 4):
				lower = int(vals[2])
				upper = int(vals[3])
				ids = []
				for i in range(lower - (lower % 100), upper+1, 100):
					if (len(codeforces_bydifficulty[int(vals[2])]) > 0):
						ids.extend(codeforces_bydifficulty[i])
				choice = random.choice(ids)
			
			if (len(vals) is 3):
				if (len(codeforces_bydifficulty[int(vals[2])]) > 0):
					choice = random.choice(codeforces_bydifficulty[int(vals[2])])
			
			link = "https://codeforces.com/problemset/problem/" + str(codeforces_ids[choice]["contestId"]) + "/" + codeforces_ids[choice]["index"]
			prev_message = output_message
			output_message += "<:codeforces:704170636049645639> " + codeforces_ids[choice]["name"] + " - <" + link + ">\n"
			if (len(output_message) > 2000):
				output_message = prev_message
			
		await message.channel.send(output_message)

client.run(token)