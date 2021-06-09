import os, random
import discord
from discord import channel
from discord.ext import commands
from discord.ext.commands import context
from dotenv import load_dotenv

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
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
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses_fr)}')

@bot.command(name='del')
async def delete(ctx,nb_of_messages: int):
    messages = await ctx.channel.history(limit=nb_of_messages + 1).flatten()
    for m in messages:
        await m.delete()

"""@bot.command
async def ban(ctx,member: discord.Member,*,reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"Banned {member.mention}")

@bot.command
async def kick(ctx,member: discord.Member,*,reason=None):
    await member.kick(reason=reason)

@bot.command
async def unban(ctx,*,member):
    banned_users = await ctx.guild.ban()
    member_name , member_tag = member.split('#')
    for banned_u in banned_users:
        user = banned_u.user
        if (user.name, user.discriminator) == (member_name, member_tag):
            await ctx.guild.unban(user)
            await ctx.send(f"Unbanned {user.mention}")
            return"""

@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency*1000)}ms')


#@bot.command(name='server')
#async def fetchServerInfo(ctx):
#	guild = ctx.guild
#	await ctx.send(f'Server Name: {guild.name}')
#	await cxt.send(f'Server Size: {len(guild.members)}')
#	await cxt.send(f'Server Name: {guild.owner.display_name}')

load_dotenv(dotenv_path="config")

bot.run(os.getenv("TOKEN"))
