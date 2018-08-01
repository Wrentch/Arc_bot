import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import random
import requests
import io
import safygiphy
import traceback
import sys

bot = commands.Bot(command_prefix=".")
bot.remove_command('help')
g = safygiphy.Giphy()
bypass_list = []

#events

@bot.event
async def on_ready():
    print("bot started")
    print("name = " + bot.user.name)
    print("id = " + bot.user.id)
    await bot.change_presence(game=discord.Game(name='.help'))

@bot.event
async def on_member_join(member):
    serverchannel = discord.Object("421720136693841921")
    msg = "Welcome {0} to {1}".format(member.mention, member.server.name)
    await bot.send_message(serverchannel, msg)

@bot.event
async def on_member_remove(member):
    serverchannel = discord.Object("421720136693841921")
    msg = "Looks like {0} left us. Bye bye.".format(member.name)
    await bot.send_message(serverchannel, msg)







#commands

@bot.command(pass_context=True)
async def ping(ctx):
    embed = discord.Embed(title="PONG", description=":ping_pong:", color=0xf0546a)
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def serverinfo(ctx):
    embed = discord.Embed(name="{}'s info".format(ctx.message.server.name), description="Servers info.", color=0xf0546a)
    embed.set_author(name="GAME OVER")
    embed.add_field(name="Name", value=ctx.message.server.name, inline=True)
    embed.add_field(name="ID", value=ctx.message.server.id, inline=True)
    embed.add_field(name="Members", value=len(ctx.message.server.members))
    embed.add_field(name="Roles", value=len(ctx.message.server.roles), inline=True)
    embed.add_field(name="Was created:", value=ctx.message.server.created_at)
    embed.set_thumbnail(url=ctx.message.server.icon_url)
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def flip(ctx):
    flip = random.choice(["Head", "Tail"])
    embed = discord.Embed(name="FLIP", color=0x2669ff)
    embed.add_field(name="Coin:", value= flip)
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def vote(ctx, *, votequestion: str):
    embed = discord.Embed(name="vote", color=0x12c23f)
    embed.add_field(name="Vote question: ", value=votequestion)
    votemsg = await bot.say(embed=embed)
    await bot.add_reaction(votemsg, "✅")
    await bot.add_reaction(votemsg, "❌")

@bot.command(pass_context=True)
async def info(ctx, user: discord.Member):
    embed = discord.Embed(title="{}'s info".format(user.name), description="Users info.", color=0xfff200)
    embed.add_field(name="NAME", value=user.name, inline=True)
    embed.add_field(name="ID", value=user.id, inline=True)
    embed.add_field(name="STATUS", value=user.status, inline=True)
    embed.add_field(name="HIGHEST ROLE", value=user.top_role)
    embed.add_field(name="JOINED", value=user.joined_at)
    embed.set_thumbnail(url=user.avatar_url)
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author
    embed = discord.Embed(title="Help", description="list of all commands", color=0xfff200)
    embed.add_field(name='.ping', value='bot responds with  pong', inline=False)
    embed.add_field(name='.serverinfo', value='shows info about the server', inline=False)
    embed.add_field(name='.flip', value='bot flips a virtual coin', inline=False)
    embed.add_field(name='.vote [question/vote]', value='bot creates a poll for pepole to vote', inline=False)
    embed.add_field(name='.info [@user]', value='shows info about the specified user', inline=False)
    embed.add_field(name='.gif', value='sends a random gif', inline=False)
    embed.add_field(name='.game [@user]', value='shows the game that the mentioned user is playing', inline=False)
    await bot.send_message(author, embed=embed)
    await bot.say('{}, check your DM'.format(author.mention))

@bot.command(pass_context=True)
async def gif(ctx):
    gif_tag = ""
    rgif = g.random(tag=str(gif_tag))
    response = requests.get(str(rgif.get("data", {}).get('image_original_url')), stream=True)
    await bot.send_file(ctx.message.channel, io.BytesIO(response.raw.read()), filename='video.gif')

@bot.command(pass_context=True)
async def game(ctx, user: discord.Member):
    embed = discord.Embed(name="Game", color=0xf0546a)
    embed.add_field(name="{} is now playing: ".format(user.name), value=user.game.name)
    await bot.say(embed=embed)

@bot.event
async def on_message(message):
    contents = message.content.split(" ")
    for word in contents:
        if "discord.gg" in message.content.lower():
            if not message.author.id in bypass_list:
                try:
                    await bot.delete_message(message)
                    await bot.send_message(message.channel, "**Hey!** You're not allowed to send links to other servers here!")
                except discord.errors.NotFound:
                    return
    await bot.process_commands(message)



#token

bot.run("NDczNTc2MzcwNzkwOTg5ODU1.DkEIIQ.zm2KXPdXIBtTGQINhJLvTHuujX0")
