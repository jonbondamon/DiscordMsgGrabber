exec(open(r'bot_2\venv\Scripts\activate_this.py').read(), {'__file__': r'bot_2\venv\Scripts\activate_this.py'})

from discord.ext import commands
import discord, yaml

with open("settings.yml", mode="r") as yaml_file:
        settings_yaml = yaml.safe_load(yaml_file)

intents =  discord.Intents.all()
client = commands.Bot(command_prefix='/', intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):

    if message.author != client.user:
        if message.channel.id == settings_yaml['message_exhange_channel_id']:
            embeds = message.embeds
            footer = embeds[0].footer
            channel = str(footer).split("'")[1::2][0]
            channel = client.get_channel(int(channel))
            embeds[0].set_footer(text='')
            for embed in embeds:
                if embed.description and'.mp4' in embed.description:
                    await channel.send(embed.description)
                else:
                    await channel.send(embed=embed)

client.run(settings_yaml['discord_token'])