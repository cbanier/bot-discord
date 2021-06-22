import os, json
from random import choice
from requests import Session

import discord
from discord.ext import commands, tasks
from discord.ext.commands import context
from dotenv import load_dotenv
from itertools import cycle

from coinmarketcap import new_dict

bot = commands.Bot(command_prefix='!')
status = cycle(['Boulie Manitas', "Type '!help' for help", 'Valorant', '', 'Boulie Baptiste', 'soloQ ARAM', '1vs1 Yasuo-Diana'])

@bot.event
async def on_ready():
    change_status.start()
    print(f'Bot connected as {bot.user}')

@bot.event
async def on_message(message):
	#if message.content == 'test':
	#	await message.channel.send('Testing 1 2 3!')
    await bot.process_commands(message)

@bot.command(name='8ball')
async def _8ball(ctx,*,question):
    responses_fr = ["Essaye plus tard", "Essaye encore", "Pas d'avis",
    "C'est ton destin", "Le sort en est jeté", "Une chance sur deux",
    "Repose ta question", "D'après moi oui", "C'est certain", 
    "Oui absolument", "Tu peux compter dessus", "Sans aucun doute",
    "Très probable", "Oui", "C'est bien parti", "C'est non", "Peu probable",
    "Faut pas rêver", "N'y compte pas", "Impossible"]
    await ctx.send(f'Question de {ctx.author.mention}: {question}\nRéponse: {choice(responses_fr)}')

@bot.command(name='del')
async def delete(ctx,nb_of_messages: int):
    messages = await ctx.channel.history(limit=nb_of_messages + 1).flatten()
    for m in messages:
        await m.delete()

@bot.command()
async def ban(ctx,member: discord.Member,*,reason=None):
    if ctx.author.top_role.permissions.administrator:
        await member.ban(reason=reason)
        await ctx.send(f"Banned {member.mention}.")
    else:
        await ctx.send('Non Non Non' + ctx.author.mention + '.')

@bot.command()
async def kick(ctx,member: discord.Member,*,reason=None):
    if ctx.author.top_role.permissions.administrator:
        await member.kick(reason=reason)
        await ctx.send('Rip ' + member.mention + '.')
    else:
        await ctx.send(f'Laisse le bro {member.mention} tranquille tarba de ' + ctx.author.mention + '.')

@bot.command()
async def unban(ctx,*,member):
    if ctx.author.top_role.permissions.administrator:
        banned_users = await ctx.guild.ban()
        member_name , member_tag = member.split('#')
        for banned_u in banned_users:
            user = banned_u.user
            if (user.name, user.discriminator) == (member_name, member_tag):
                await ctx.guild.unban(user)
                await ctx.send(f"Unbanned {user.mention}.")
                return
    else:
        await ctx.send('Fait pas le malin' + ctx.author.mention + '.')

@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency*1000)}ms')

@bot.command()
async def mute(ctx, member: discord.Member):
    await member.edit(mute = True)

@bot.command()
async def unmute(ctx, member: discord.Member):
    await member.edit(mute = False)

@bot.command()
async def info_chan(ctx):
    await ctx.send("`id de Salon: 757990916530372840 \n id de BTREE: 757990916530372841 \n id de Goulag: 760054336604209153 \n id de Ban: 813345671016611891`")

@bot.command()
async def price(ctx, coin):
    d = new_dict(str(coin))
    embed = discord.Embed(title=coin, url='https://coinmarketcap.com/', description="This is an embed that will show a cryptocurrency's price changes.", color=discord.Color.gold())
    embed.set_author(name=ctx.author.display_name, url="https://github.com/cbanier", icon_url="https://avatars.githubusercontent.com/u/60900707?v=4")
    embed.set_thumbnail(url='https://cryptonaute.fr/wp-content/uploads/2021/03/CRYPTOMONNAIES-.jpg')
    embed.add_field(name="Price of 1 " + coin, value=d['price'] + ' $')
    embed.add_field(name="Change after 24h", value=d['change_24h'] + ' $', inline=False)
    embed.add_field(name="Change after 7d", value=d['change_7d'] + ' $', inline=False)
    embed.add_field(name="Change after 30d", value=d['change_30d'] + ' $', inline=False)
    embed.add_field(name="Change after 90d", value=d['change_90d'] + ' $', inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def convert(ctx, number, currency_target):
    session = Session()
    url = 'https://api.exchangerate-api.com/v4/latest/USD'
    response = session.get(url)
    target_coef = float(json.loads(response.text)['rates'][currency_target])
    await ctx.send(f'{number} USD = {float(number)*target_coef} {currency_target}')

@bot.command()
async def move(ctx, member: discord.Member, channel: discord.VoiceChannel):
    await member.move_to(channel)

@tasks.loop(seconds=10)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status)))

#@bot.command(name='server')
#async def fetchServerInfo(ctx):
#	await ctx.send(f'Server Name: {ctx.guild.name}')
#	await ctx.send(f'Server Size: {len(ctx.guild.members)}')
#	await ctx.send(f'Server Owner: {ctx.guild.owner}')

load_dotenv(dotenv_path="config")

bot.run(os.getenv("TOKEN"))
