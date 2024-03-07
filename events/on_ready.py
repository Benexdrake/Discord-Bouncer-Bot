import discord
from discord.ext import commands

class OnReady(commands.Cog):
    
    def __init__(self, bot:discord.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user.name} is Online')

def setup(bot:discord.Bot):
    bot.add_cog(OnReady(bot))