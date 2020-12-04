import discord
import os
import time 
import aiohttp
import json
import random
from discord.ext import commands, tasks
from discord.voice_client import VoiceClient
from discord.ext import commands
number = 0
userInput = 0
Money = 0
token1 = 'NzU1NDAzMDYxMTczNjgyMTc2.X2Cx7A.mfLL3ONN5hgchjihjeNLdg8RSAY'
client = commands.Bot(command_prefix = ".")
client.remove_command('help')
status = ['prefix is .']
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="prefix is ."))
    print('bot is ready!')
@client.event
async def on_member_join(member):
    print('ok')
#help
@client.command()
async def help(ctx):
    embed = discord.Embed(title="help")
    embed.add_field(name='.kitty', value='shows a cat image!', inline=True)
    embed.add_field(name='.doggo', value='shows a dog image!', inline=True)
    embed.add_field(name='.epikTrailer', value='shows the best and epic trailer in the world', inline=True)
    embed.add_field(name='.kick', value='kicks a member', inline=True)
    embed.add_field(name='.ban', value='bans a member', inline=True)
    embed.add_field(name='.unban', value='unbans a banned member', inline=True)
    embed.add_field(name='.mute', value='mutes a member', inline=True)
    embed.add_field(name='.unmute', value='unmutes a member', inline=True)
    embed.add_field(name='.good_boi', value='I smile :)', inline=True)
    embed.add_field(name='.Test', value='to see if something works', inline=True)
    embed.add_field(name='.hello', value='I greet you', inline=True)
    embed.add_field(name='.you_dumb', value='how dare you', inline=True)
    embed.add_field(name='.info', value='Shows your or the member you ping info', inline=True)
    embed.add_field(name='.reapet', value='repeats what you said', inline=True)
    embed.add_field(name='.warn', value='warns a member', inline=True)
    embed.add_field(name='.comment', value='shows a comment like you wrote it', inline=True)
    embed.add_field(name='.beg', value='get some money!', inline=True)
    embed.add_field(name='.balance', value='to see your money', inline=True)
    embed.add_field(name='.AddToWallet', value='Add money from the bank to your wallet', inline=True)
    embed.add_field(name='.AddToBank', value='Add money from your wallet to the bank', inline=True)
    embed.add_field(name='.GiveMoney <member> <money>', value='give to someone money', inline=True)
    embed.add_field(name='.Serverinfo', value='gives info about the server', inline=True)
    embed.add_field(name='.rob <member> <money>', value='rob someones moeny', inline=True)
    embed.add_field(name='.Buy <item> <money > 100', value='buys an item and adds it into your inventory', inline=True)
    embed.add_field(name='.Items', value='Shows the items you bougth from .Buy', inline=True)
    embed.add_field(name='.buyRoles <name of the role you want to create> (pays 1000 money)', value='creates a role you want with the name you choosed (no permissions)', inline=True)
    embed.add_field(name='.Foyu', value='link to download the beta for foyu(the game im working on)', inline=True)
    embed.add_field(name='.purge <number>', value='deletes messages', inline=True)
    embed.add_field(name='.poll <Title> <answer 1> <answer 2>', value='creates a poll', inline=True)
    embed.add_field(name='.rickRoll', value='??????????', inline=True)
    await ctx.send(embed=embed)
@client.command()
async def balance(ctx):
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
async def Items(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()
    items_amt = users[str(user.id)]["items"]
    em = discord.Embed(title = f"{ctx.author.name}'s balance", color = discord.Color.red())
    for i in range(0, len(items_amt)):
        em.add_field(name='items', value = items_amt[i])
    await ctx.send(embed = em)
@client.command()
async def beg(ctx):
    await open_account(ctx.author)
    users = await get_bank_data()
    user = ctx.author
    earnings = random.randrange(101)
    await ctx.send(f"Someone gave you {earnings} coins!!")
    users[str(user.id)]["wallet"] += earnings
    with open("mainbank.json", "w") as f:
        users = json.dump(users,f)
async def open_account(user):
    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id) ] = {}
        users[str(user.id) ]["wallet"] = 0
        users[str(user.id) ]["bank"] = 0
        users[str(user.id) ]["items"] = [{}]
    with open("mainbank.json", "w") as f:
        users = json.dump(users,f)
    return True
async def get_bank_data():
    with open("mainbank.json", "r") as f:
        users = json.load(f)
    return users
@client.command()
async def buyRoles(ctx, RoleName='new Role', reason=None):
    await open_account(ctx.author)
    users = await get_bank_data()
    user = ctx.author
    earnings = random.randrange(101)
    if(users[str(user.id)]["wallet"] < 1000):
        moneyYouNeed = 1000 - users[str(user.id)]["wallet"] 
        await ctx.send(f'not enough money you need {moneyYouNeed} bucks, it costs 1000 bucks')
        return
    newRole = await ctx.guild.create_role(name=RoleName)
    await ctx.message.author.add_roles(newRole, reason=reason)
    await ctx.send(f"You bought a new Role {RoleName}, you paid 1000 bucks")
    users[str(user.id)]["wallet"] -= 1000
    with open("mainbank.json", "w") as f:
        users = json.dump(users,f)
    return True
@client.command()
async def AddToBank(ctx, money = 20):
    await open_account(ctx.author)
    users = await get_bank_data()
    user = ctx.author
    if(users[str(user.id)]["wallet"] < money):
        await ctx.send("not enough money on your wallet")
        return
    await ctx.send(f'You transfered {money} bucks to the bank')
    users[str(user.id)]["wallet"] -= money
    users[str(user.id)]["bank"] += money
    with open("mainbank.json", "w") as f:
        users = json.dump(users,f)
@client.command()
async def GiveMoney(ctx, member : discord.Member , money = 20):
    await open_account(ctx.author)
    users = await get_bank_data()
    user = ctx.author
    if(users[str(user.id)]["wallet"] < money):
        if users[str(user.id)]["bank"] > money:
            users[str(member.id)]["bank"] += money
            users[str(user.id)]["bank"] -= money 
            with open("mainbank.json", "w") as f:
                users = json.dump(users,f)
            await ctx.send(f'{ctx.author.name} send {money} bucks to {member.name} (no money found on wallet so from the bank)')
            return
        if users[str(user.id)]["wallet"] < money:
            await ctx.send('not enough money')
            return
    await ctx.send(f'{ctx.author.name} send {money} bucks to {member.name}')
    users[str(member.id)]["wallet"] += money
    users[str(user.id)]["wallet"] -= money
    with open("mainbank.json", "w") as f:
        users = json.dump(users,f)
@client.command()
async def rob(ctx, member : discord.Member , money = 20):
    await open_account(ctx.author)
    users = await get_bank_data()
    user = ctx.author
    if(money > 1000):
        await ctx.send('man you arent so good at robbing chill out')
        return
    if(users[str(member.id)]["wallet"] < money):
        await ctx.send("he doesnt have so much money xD")
        return
    await ctx.send(f'{ctx.author.name} robbed {money} bucks from {member.name}')
    users[str(member.id)]["wallet"] -= money
    users[str(user.id)]["wallet"] += money
    with open("mainbank.json", "w") as f:
        users = json.dump(users,f)
@client.command()
async def AddToWallet(ctx, money = 20):
    await open_account(ctx.author)
    users = await get_bank_data()
    user = ctx.author
    if(users[str(user.id)]["bank"] < money):
        await ctx.send("not enough money on the bank")
        return
    await ctx.send(f'You transfered {money} bucks to your wallet')
    users[str(user.id)]["wallet"] += money
    users[str(user.id)]["bank"] -= money
    with open("mainbank.json", "w") as f:
        users = json.dump(users,f)
@client.command()
async def Buy(ctx, stuff='something...', money=20):
    if(money < 100):
        await ctx.send('pay more money...')
        return
    await open_account(ctx.author)
    users = await get_bank_data()
    user = ctx.author
    earnings = random.randrange(101)
    if(users[str(user.id)]["wallet"] < money):
        moneyYouNeed = money - users[str(user.id)]["wallet"]
        await ctx.send(f'not enough money you need {moneyYouNeed} bucks, it costs {money} bucks')
        return
    await ctx.send(f"You bought a {stuff}, you paid {money} bucks")
    users[str(user.id)]["wallet"] -= money
    users[str(user.id)]["items"].append(stuff)
    with open("mainbank.json", "w") as f:
        users = json.dump(users,f)
    return True
@client.command()
async def comment(ctx , member: discord.Member = None):
    if member == None:
        member = ctx.message.author

    def is_author(m : discord.Message):
        return ctx.author == m.author

    await ctx.send(f"what should the Username be?")

    name = await client.wait_for("message", check=is_author, timeout=30)

    
    await ctx.send(f"Ok,what should the comment be?")

    comment = await client.wait_for("message", check=is_author, timeout=30)

    

    await ctx.send(
        f"https://some-random-api.ml/canvas/youtube-comment?avatar={member.avatar_url}"[:-14]+
        f"png?size=1024&comment={comment.content}".replace(" ", "+")+f"&username={name.content}".replace(" ", "+"))
#cat-dog images
@client.command()
async def kitty(ctx):
    async with aiohttp.ClientSession() as cs:
        async with cs.get("http://aws.random.cat/meow") as r:
            data = await r.json()

            embed = discord.Embed(title="Meow")
            embed.set_image(url=data['file'])

            await ctx.send(embed=embed)
@client.command()
async def doggo(ctx):
    async with aiohttp.ClientSession() as cs:
        async with cs.get("https://random.dog/woof.json") as r:
            data = await r.json()

            embed = discord.Embed(title="woof")
            embed.set_image(url=data['url'])

            await ctx.send(embed=embed)#cat-dog images
@client.command()
async def cat(ctx):
    async with aiohttp.ClientSession() as cs:
        async with cs.get("http://aws.random.cat/meow") as r:
            data = await r.json()

            embed = discord.Embed(title="Meow")
            embed.set_image(url=data['file'])

            await ctx.send(embed=embed)
@client.command()
async def dog(ctx):
    async with aiohttp.ClientSession() as cs:
        async with cs.get("https://random.dog/woof.json") as r:
            data = await r.json()

            embed = discord.Embed(title="woof")
            embed.set_image(url=data['url'])

            await ctx.send(embed=embed)
@client.command()
async def fox(ctx):
    async with aiohttp.ClientSession() as cs:
        async with cs.get("https://randomfox.ca/floof") as r:
            data = await r.json()

            embed = discord.Embed(title="fox!")
            embed.set_image(url=data['url'])

            await ctx.send(embed=embed)
#kick
@client.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx, member : discord.Member, * , reason=None):
 await member.kick(reason=reason)
 await ctx.send(f'{member} has been kicked {reason}')
#add roles
@client.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    if message_id == 764576754483855360:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)
        if payload.emoji.name == 'kitty':
            role = discord.utils.get(guild.roles, name='programmer')
            await payload.member.add_roles(role, reason = 'programmer role')
        if payload.emoji.name == 'Max':
            role = discord.utils.get(guild.roles, name='artist')
            await payload.member.add_roles(role, reason = 'artist role')
        if payload.emoji.name == 'Doggo':
            role = discord.utils.get(guild.roles, name='designer')
            await payload.member.add_roles(role, reason = 'designer role')
        if payload.emoji.name == 'excitedkitten':
            role = discord.utils.get(guild.roles, name='ping me')
            await payload.member.add_roles(role, reason = 'ping me role')
        if payload.emoji.name == 'beemad':
            role = discord.utils.get(guild.roles, name='ping me for among us')
            await payload.member.add_roles(role, reason = 'ping me for among us role')
        if payload.emoji.name == 'cringe':
            role = discord.utils.get(guild.roles, name='Ping me for le dude')
            await payload.member.add_roles(role, reason = 'ping me for le dude')
    if message_id == 772812274054201355:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)
        if payload.emoji.name == 'kitty':
            role = discord.utils.get(guild.roles, name='GameDev')
            await payload.member.add_roles(role, reason = 'GameDev role')
#mute
#@client.command()
#@commands.has_permissions(kick_members = True)
#async def mute(ctx, member : discord.Member, * , reason=None):
    #guild = ctx.guild
    #mutedRole = discord.utils.get(guild.roles, name="Muted")

    #if not mutedRole:
        #mutedRole = discord.utils.get(guild.roles, name="Muted")

        #for channel in guild.channels:
            #await channel.set_permissions(mutedRole, speak=False, send_messages=False)
        
    #await member.add_roles(mutedRole, reason=reason)
    #await ctx.send(f'{member} has been muted for reason {reason}')
    #await mmember.send(f'You were muted in the server {guild.name} for {reason}')
#mute
@client.command(description="Mutes the specified user.")
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")

    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False)

    await member.add_roles(mutedRole, reason=reason)
    await ctx.send(f"{member} has been muted for reason {reason}")
    await member.send(f"You were muted in the server {guild.name} for {reason}")

#unmute
@client.command(description="Unmutes a specified user.")
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
    mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

    await member.remove_roles(mutedRole)
    await ctx.send(f"{member} has been unmuted")
    await member.send(f"You were unmuted in the server {ctx.guild.name}")
#clear
@client.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount=5):
    await ctx.channel.purge(limit=amount + 1)
#ban
@client.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : discord.Member, * , reason=None):
 await member.ban(reason=reason)
 await ctx.send(f'{member} has been banned {reason}')
#unban
@client.command()
@commands.has_permissions(ban_members = True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.name}#{user.discriminator}')
#good boi
@client.command()
async def good_boi(ctx):
    await ctx.send(':)')
#warn
@client.command()
@commands.has_permissions(manage_messages = True)
async def warn(ctx, member : discord.Member, * , reason=None):
    guild = ctx.guild
    await member.send(f'You were warned on {guild.name} for reason {reason} dont do it again please')
    await ctx.send(f'{member} has been warned')
#hello
@client.command()
async def hello(ctx):
    await ctx.send('Hi kind sir!')
#avatar
@client.command()
async def info(ctx, member : discord.Member = None):
    if member == None:
        member = ctx.message.author
    embed = discord.Embed(title=f'{member}s info')
    embed.add_field(name='member id', value=f'{member.id}', inline=True)
    embed.set_image(url=f'{member.avatar_url}')
    embed.add_field(name='member roles', value=f'{member.top_role.mention}', inline=False)
    embed.add_field(name='account created', value=f'{member.created_at}', inline=False)
    embed.add_field(name='joined', value=f'{member.joined_at}', inline=False)

    await ctx.send(embed=embed)
#avatar
@client.command()
async def Serverinfo(ctx):
    guild = ctx.guild
    embed = discord.Embed(title=f'{guild.name}s info')
    embed.add_field(name='server id', value=f'{guild.id}', inline=True)
    embed.set_thumbnail(url=f'{guild.icon_url}')
    embed.add_field(name='server channels', value=f'{len(guild.channels)}', inline=False)
    embed.add_field(name='server voice channels', value=f'{len(guild.voice_channels)}', inline=False)
    embed.add_field(name='server text channels', value=f'{len(guild.text_channels)}', inline=False)

    await ctx.send(embed=embed)
#test
@client.command()
async def Test(ctx):
    await ctx.send('It works :)')
#rickRoll
@client.command()
async def rickRoll(ctx):
    await ctx.send('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
#epikTrailer
@client.command()
async def epikTrailer(ctx):
    await ctx.send('https://www.youtube.com/watch?v=XVuQdA2kdUQ')
#epikTrailer
@client.command()
async def repeat(ctx, repeat='repeat xD'):
    await ctx.send(repeat)
#Foyu
@client.command()
async def Foyu(ctx):
    embed = discord.Embed(title="Foyu Beta Download")
    embed.add_field(name='Android', value='https://play.google.com/store/apps/details?id=com.Gelis.Dsadafd2Dgame', inline=True)
    embed.add_field(name='PC', value='https://gelis07.itch.io/foyu-alpha', inline=True)
    await ctx.send(embed=embed)
@client.command()
async def poll(ctx, title='title', field1='something..', field2 = 'something'):
    embed = discord.Embed(title=title)
    embed.add_field(name='answer 1', value = f'🅰{field1}')
    embed.add_field(name='answer 2', value = f'🅱{field2}')
    message=await ctx.send(embed=embed)
    await message.add_reaction("🅰")
    await message.add_reaction("🅱")
@client.command()
async def you_dumb(ctx):
    await ctx.send(':O')
client.run(token1)





