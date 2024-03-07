import discord
from discord.ext import commands
from discord.commands import slash_command

import os
from dotenv import load_dotenv

class Button(commands.Cog):
    def __init__(self, bot:discord.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(InviteButtonView())

    @slash_command()
    @discord.default_permissions(administrator=True)
    @discord.guild_only()
    async def create_invite_button(self,ctx:commands.Context):
        file = open('regeln.txt', 'r')
        content = file.read()
        file.close()

        await ctx.respond(content, view=InviteButtonView())

def setup(bot:discord.Bot):
    bot.add_cog(Button(bot))


# --------------------------------------------------------------------------------------------------------------------------------

class InviteButtonView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Click me for Invite', style=discord.ButtonStyle.primary, custom_id='invite_button', row=1)
    async def button_callback1(self,button,interaction:discord.Interaction):
        modal = ReactionModal(title='Invite Question Modal')
        await interaction.response.send_modal(modal)


class ReactionModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs):
        super().__init__(
            discord.ui.InputText(
                label='Twitter Account Url',
                placeholder='https://twitter.com/your_username',
                style=discord.InputTextStyle.singleline, 
                required=False
            ),
            discord.ui.InputText(
                label='Frage 1:',
                placeholder=os.getenv('q1'),
                style=discord.InputTextStyle.long, 
                required=True
            ),
            discord.ui.InputText(
                label='Frage 2:',
                placeholder=os.getenv('q2'),
                style=discord.InputTextStyle.long, 
                required=True
            ),
            discord.ui.InputText(
                label='Frage 3:',
                placeholder=os.getenv('q3'),
                style=discord.InputTextStyle.long, 
                required=True
            ),
            *args,
            **kwargs)
        
    async def callback(self, interaction: discord.Interaction):
        
        load_dotenv()

        await interaction.response.send_message('U will never see this Message', ephemeral=True)

        q1 = os.getenv('q1') + ': \n```' + self.children[1].value+'```'
        q2 = os.getenv('q2') + ': \n```' + self.children[2].value+'```'
        q3 = os.getenv('q3') + ': \n```' + self.children[3].value+'```'

        await interaction.user.send(f'Anfrage wurde an die Admins gesendet.\n# Deine Antworten:\n{q1}\n{q2}\n{q3}\n')

        guild:discord.Guild = interaction.client.get_guild(int(os.getenv('adminGuild')))

        channel:discord.TextChannel = guild.get_channel(int(os.getenv('inviteChannel')))

        embed = discord.Embed(
            color=discord.Color.blue()
        )

        if 'https://twitter.com/' in self.children[0].value:
            embed.title='Twitter Profile'
            embed.url=self.children[0].value

        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar) 

        embed.add_field(name=os.getenv('q1'), value= '```' + self.children[1].value+'```', inline=False)
        embed.add_field(name=os.getenv('q2'), value= '```' + self.children[2].value+'```', inline=False)
        embed.add_field(name=os.getenv('q3'), value= '```' + self.children[3].value+'```', inline=False)

        await channel.send(f'ID: {interaction.user.id}', embeds=[embed], view=AcceptDeclineButtonView())

        # await interaction.user.kick()



class AcceptDeclineButtonView(discord.ui.View):
    
    def __init__(self):
        super().__init__(timeout=None)


    @discord.ui.button(label='Accept', style=discord.ButtonStyle.green, custom_id='accept_button', row=1)
    async def button_accept_callback(self,button:discord.Button,interaction:discord.Interaction):
        userId = self.message.content.split('\n')[0].split(' ')[1]

        user = await interaction.client.fetch_user(int(userId))

        guild:discord.Guild = interaction.client.get_guild(int(os.getenv('secretGuild')))
        
        channel:discord.TextChannel = guild.get_channel(int(os.getenv('secretGuildChannel')));
        new_invite:discord.Invite = await channel.create_invite(max_uses=1)

        button = discord.ui.Button(label='Discord Invite Link',url=new_invite.url)
        view = discord.ui.View()
        view.add_item(button)

        await user.send('You got Accepted', view=view)


        message = await interaction.response.send_message('Accept')

        await message.delete_original_response()
        await self.message.delete()
        
    @discord.ui.button(label='Decline', style=discord.ButtonStyle.danger, custom_id='decline_button', row=1)
    async def button_decline_callback2(self,button:discord.Button,interaction:discord.Interaction):
        userId = self.message.content.split('\n')[0].split(' ')[1]

        modal = DeclineModal(title=userId)
        await interaction.response.send_modal(modal)


class DeclineModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs):
        super().__init__(
            discord.ui.InputText(
                label='Begründung:',
                placeholder='Begründung eingeben',
                style=discord.InputTextStyle.long, 
                required=True
            ),
            *args,
            **kwargs)
        
    async def callback(self, interaction: discord.Interaction):
        message = await interaction.response.send_message('OK')
        await interaction.message.delete()
        await message.delete_original_response()
        userId = self.title
        user = await interaction.client.fetch_user(int(userId))
        await user.send(f'# Begründung:\n{self.children[0].value}')
