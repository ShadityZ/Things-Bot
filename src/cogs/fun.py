import json
import random
import discord
import aiohttp

from io import BytesIO
from discord.ext import commands
import urllib.request as request

from lib.data import eight_ball, bonk_objects
from lib.utils import api_call


def list_to_text(list: list):
    text = ""
    for item in list:
        if item.index != (len(list)-1):
            text.join(f"\n{item},")
        else:
            text.join(f"\n{item}")
    return text

class Fun_Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["8ball"])
    @commands.cooldown(rate=1, per=2.0, type=commands.BucketType.user)
    async def eightball(self, ctx, *, question: commands.clean_content):
        """ Consult 8ball to receive an answer """

        answer = random.choice(eight_ball)
        await ctx.send(f"🎱 **Question:** {question}\n**Answer:** {answer}")

    @commands.command(aliases=["flip", "coin"])
    @commands.cooldown(rate=1, per=2.0, type=commands.BucketType.user)
    async def coinflip(self, ctx):
        """ Coinflip! """
        coinsides = ["Heads", "Tails"]
        await ctx.send(f"**{ctx.author.name}** flipped a coin and got **{random.choice(coinsides)}**!")

    @commands.command()
    @commands.cooldown(rate=1, per=5.0, type=commands.BucketType.user)
    async def randomfact(self, ctx):
        """ Bored? Learn some random facts """
        fact = request.urlopen("https://uselessfacts.jsph.pl//random.json?language=en")
        data = json.loads(fact.read().decode())
        embed = discord.Embed(title="🎲 Random Fact:",
                            description=data["text"],
                            color=discord.Color.random())
        await ctx.send(embed=embed)

    @commands.command(aliases=["hit"])
    @commands.cooldown(rate=1, per=10.0, type=commands.BucketType.user)
    async def bonk(self, ctx, member: str, *, reason = "no reason"):
        """'Bonk' someone with objects for specified reasons!"""
        if member == self.bot:
            await ctx.send(f"{ctx.author.mention} tried to bonk me, but I dodged them!")
        elif member == ctx.author.mention:
            await ctx.send(f"{ctx.author.mention} bonked themselves with {random.choice(bonk_objects)} for {reason}.")
        else:
            await ctx.send(f"{ctx.author.mention} bonked {member} with {random.choice(bonk_objects)} for {reason}.")


    @commands.command()
    @commands.cooldown(rate=1, per=10.0, type=commands.BucketType.user)
    async def quote(self, ctx):
        """ Enlighten yourself with smart stuff from smart people """
        response = await api_call("https://zenquotes.io/api/random")
        quote = response[0]["q"] + "     -" + response[0]["a"]

        if quote == 'Too many requests. Obtain an auth key for unlimited access. -ZenQuotes.io':
            await ctx.send(
                "Do you seriously need more quotes? Wait 30 seconds please")
        else:
            await ctx.send(quote)

    @commands.command()
    async def advice(self, ctx):
        response = ""
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.adviceslip.com/advice") as response:
                response = await response.read()
                response = json.loads(response)
        advice = response['slip']['advice']
        await ctx.message.reply(advice)

    @commands.command()
    @commands.cooldown(rate=1, per=2.0, type=commands.BucketType.user)
    async def reverse(self, ctx, *, text: str):
        """ !poow ,ffuts esreveR
        Everything you type after reverse will of course, be reversed
        """
        t_rev = text[::-1].replace("@", "@\u200B").replace("&", "&\u200B")
        await ctx.send(f"🔁 {t_rev}")

    @commands.command(aliases=["hotcalc", "hot"])
    async def howhot(self, ctx, *, user: discord.Member = None):
        """ Returns a random percent for how hot is a discord user """
        user = user or ctx.author

        random.seed(user.id)
        r = random.randint(1, 100)
        hot = r / 1.17

        if hot > 75:
            emoji = "💞"
        elif hot > 50:
            emoji = "💖"
        elif hot > 25:
            emoji = "❤"
        else:
            emoji = "💔"

        await ctx.send(f"**{user.name}** is **{hot:.2f}%** hot {emoji}")

    @commands.command()
    @commands.cooldown(rate=1, per=5.0, type=commands.BucketType.user)
    async def meme(self, ctx):
        """ Get some fast laughs """
        response = await api_call("https://meme-api.herokuapp.com/gimme")
        meme = discord.Embed(title=response['title'], url=response['postLink'], 
                            color=discord.Color.random())
        meme.set_image(url=f"{response['url']}")
        await ctx.send(embed=meme)

