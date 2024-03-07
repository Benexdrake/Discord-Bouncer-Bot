import discord
import os
from dotenv import load_dotenv

class Bot(discord.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        status = discord.Status.dnd
        activity = discord.Activity(type=discord.ActivityType.watching, name='sich den Besuch an.')

        super().__init__(intents=intents, status=status, activity=activity)

    def run(self):
        self.loading('events')
        self.loading('slash_commands')

        load_dotenv()
        super().run(os.getenv('TOKEN'))

    def loading(self,folder:str):
        for filename in os.listdir(f"{folder}"):
            if filename.endswith('.py'):
                print(f'Loading {folder}: {filename[:-3]}')
                super().load_extension(f'{folder}.{filename[:-3]}')
