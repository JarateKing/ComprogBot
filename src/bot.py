from private_token import token
from collections import defaultdict
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import random
import discord
import requests
import json

# setup kattis problems
kattis_problems = requests.get("https://chrismac.dev/kattis/problems").json()['problems']
kattis_bydifficulty = defaultdict(list)
for i in range(len(kattis_problems)):
	kattis_bydifficulty[kattis_problems[i]["difficulty"]].append(i)

# setup codeforces problems
codeforces_problems = requests.get("https://codeforces.com/api/problemset.problems").json()
codeforces_ids = codeforces_problems["result"]["problems"]
codeforces_bydifficulty = defaultdict(list)
for i in range(len(codeforces_ids)):
	if "rating" in codeforces_ids[i]:
		codeforces_bydifficulty[codeforces_ids[i]["rating"]].append(i)
		
# setup uva problems
uva_problems = requests.get("https://uhunt.onlinejudge.org/api/p").json()

# setup atcoder problems
atcoder_problems = requests.get("https://kenkoooo.com/atcoder/resources/problems.json").json()

client = discord.Client()

print("bot ready")

@client.event
async def on_message(message):
	# we do not want the bot to reply to itself
	if message.author == client.user:
		return
	
	if message.content.startswith('!kattis'):
		await message.channel.send("<:kattis:704169451163222128> <https://open.kattis.com/>")
	
	if message.content.startswith('!codeforces'):
		await message.channel.send("<:codeforces:704170636049645639> <https://codeforces.com/>")
		
	if message.content.startswith('!euler') or message.content.startswith('!projecteuler'):
		await message.channel.send("<:euler:706923688942895104> <https://projecteuler.net/>")
		
	if message.content.startswith('!uva'):
		await message.channel.send("<:uva:707075805418749983> <https://uhunt.onlinejudge.org/>")
		
	if message.content.startswith('!atcoder'):
		await message.channel.send("<:atcoder:708137443035185172> <https://kenkoooo.com/atcoder/>")
		
	if message.content.startswith('!problem'):
		vals = message.content.split()
		num_probs = 1
		output_message = ""
		
		random_type = -1
		if (len(vals) is 1):
			random_type = random.randrange(5)
		
		if ((random_type is 0) or (len(vals) > 1 and (vals[1] == 'euler' or vals[1] == 'projecteuler'))):
			if (len(vals) is 3):
				num_probs = min(20, max(1, int(vals[2])))
		
			for iteration in range(num_probs):
				choice = random.randrange(700)
				link = "https://projecteuler.net/problem=" + str(choice)
				prev_message = output_message
				output_message += "<:euler:706923688942895104> <" + link + ">\n"
				if (len(output_message) > 2000):
					output_message = prev_message
					
		if ((random_type is 1) or (len(vals) > 1 and vals[1] == 'uva')):
			if (len(vals) is 3):
				num_probs = min(20, max(1, int(vals[2])))
		
			for iteration in range(num_probs):
				choice = random.randrange(len(uva_problems))
				link = "https://onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&category=3&page=show_problem&problem=" + str(uva_problems[choice][0])
				prev_message = output_message
				output_message += "<:uva:707075805418749983> " + uva_problems[choice][2] + " - <" + link + ">\n"
				if (len(output_message) > 2000):
					output_message = prev_message
		
		if ((random_type is 2) or (len(vals) > 1 and vals[1] == 'atcoder')):
			if (len(vals) is 3):
				num_probs = min(20, max(1, int(vals[2])))
		
			for iteration in range(num_probs):
				choice = random.randrange(len(atcoder_problems))
				link = "https://atcoder.jp/contests/" + str(atcoder_problems[choice]['contest_id']) + "/tasks/" + str(atcoder_problems[choice]['id'])
				prev_message = output_message
				output_message += "<:atcoder:708137443035185172> <" + link + ">\n"
				if (len(output_message) > 2000):
					output_message = prev_message
		
		if ((random_type is 3) or (len(vals) > 1 and vals[1] == 'kattis')):
			if (len(vals) is 5):
				num_probs = min(20, max(1, int(vals[4])))
				vals.pop()
			
			for iteration in range(num_probs):
				choice = random.randrange(len(kattis_problems))
				
				if (len(vals) is 4):
					lower = float(vals[2])
					upper = float(vals[3])
					ids = []
					for i in range(int(lower * 10), int((upper + 0.1) * 10)):
						ids.extend(kattis_bydifficulty[str(i / 10)])
					choice = random.choice(ids)
				
				if (len(vals) is 3):
					if (len(kattis_bydifficulty[vals[2]]) > 0):
						choice = random.choice(kattis_bydifficulty[vals[2]])
				
				link = "https://open.kattis.com/problems/" + kattis_problems[choice]["_id"]
				prev_message = output_message
				output_message += "<:kattis:704169451163222128> " + kattis_problems[choice]["name"] + " - <" + link + ">\n"
				if (len(output_message) > 2000):
					output_message = prev_message
							
					
		if ((random_type is 4) or (len(vals) > 1 and vals[1] == 'codeforces')):
			if (len(vals) is 5):
				num_probs = min(20, max(1, int(vals[4])))
				vals.pop()
		
			for iteration in range(num_probs):
				choice = random.randrange(len(codeforces_ids))
				
				if (len(vals) is 4):
					lower = int(vals[2])
					upper = int(vals[3])
					ids = []
					for i in range(lower - (lower % 100), upper+1, 100):
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