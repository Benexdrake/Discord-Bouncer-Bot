import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

class OnMemberJoin(commands.Cog):
    def __init__(self, bot:discord.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self,member:discord.Member):
        load_dotenv()

        channel = await self.bot.fetch_channel(os.getenv('log'))

        await channel.send(f'User:{member.display_name} ID:{member.id} joined the Server: {member.guild.name}')

def setup(bot:discord.Bot):
    bot.add_cog(OnMemberJoin(bot))