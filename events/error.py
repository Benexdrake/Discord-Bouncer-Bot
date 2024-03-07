import discord
from discord.ext import commands

import os
from dotenv import load_dotenv

class Error(commands.Cog):
    
    def __init__(self, bot:discord.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_application_command_error(self,ctx:commands.Context,error):
        load_dotenv()
        

        channel = await self.bot.fetch_channel(os.getenv('log'))
        ctx.respond(f'You got an Error: {error}')
        await channel.send(f'Es ist ein Fehler aufgetreten ```{error}```')
        raise error

def setup(bot):
    bot.add_cog(Error(bot))