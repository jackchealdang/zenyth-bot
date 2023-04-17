import discord
from discord.ext import commands
import json
import os
import random
import config

os.chdir(config.dir_to_source)

TOKEN = config.token

#client = discord.Client()
client = commands.Bot(command_prefix = "zen ")



@client.event
async def on_ready():
    """_summary_
    """
    print('We have logged in as {0.user}'.format(client))

def meow_this():
    """_summary_
    """
    print('meow!')

@client.command()
async def balance(ctx):
    """This will check the balance.
    """

    await open_account(ctx.author)
    user = ctx.author

    users = await get_bank_data()

    wallet_amt = users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]["bank"]

    em = discord.Embed(title = f"{ctx.author.name}'s balance", color = discord.Color.red())
    em.add_field(name = "Wallet", value = wallet_amt)
    em.add_field(name = "Bank", value = bank_amt)
    await ctx.send(embed = em)


@client.command()
async def beg(ctx):
    await open_account(ctx.author)

    users = await get_bank_data()
    user = ctx.author

    earnings = random.randrange(101)

    await ctx.send(f"Someone gave you {earnings} coins!!")


    users[str(user.id)]["wallet"] += earnings

    with open("mainbank.json","w") as f:
        json.dump(users,f)




async def open_account(user):
    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0

    with open("mainbank.json","w") as f:
        json.dump(users,f)
    return True


async def get_bank_data():
    with open("mainbank.json","r") as f:
        users = json.load(f)

    return users

# @client.event
# async def on_message(message):
#     username = str(message.author).split('#')[0]
#     user_message = str(message.content)
#     channel = str(message.channel.name)
#     print(f'{username}: {user_message} (#{channel})')

#     if message.author == client.user:
#         return
    
#     if message.channel.name == 'discord-bot-tutorial':
#         if user_message.lower() == 'hello':
#             await message.channel.send(f'Hello {username}!')
#             return
#         elif user_message.lower() == 'bye':
#             await message.channel.send(f'See you later {username}!')
#             return
#         elif user_message.lower() == '!random':
#             response = f'This is your random number: {random.randrange(1000000)}'
#             await message.channel.send(response)
#             return

#     if user_message.lower() == '!anywhere':
#         await message.channel.send('This can be used anywhere!')
#         return

client.run(TOKEN)