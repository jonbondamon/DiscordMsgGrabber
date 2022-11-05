import yaml, discord

with open("settings.yml", mode="r") as yaml_file:
        settings_yaml = yaml.safe_load(yaml_file)

class MyClient(discord.Client):

    async def on_ready(self):
        print('Logged on as', self.user)
     

    async def on_message(self, msg):

        # don't respond to ourselves
        if msg.author == self.user:
            return

        server = await validMsg(msg)
        if server:
            await sendMsg(msg, server)

async def validMsg(msg):

    # intialize serverlist into variable
    server_list = settings_yaml['server_list']
    # is msg from server in list?
    if msg.guild.id in server_list:
        # is msg from channel in list?
        if msg.channel.id in server_list[msg.guild.id]:
            # if so return server channel list
            return server_list[msg.guild.id]
        else:
            return None
    else:
        return None

async def sendMsg(msg, server):

    user = msg.author
    pfp = user.avatar_url
    images = msg.attachments
    content = msg.content
    channel = server[msg.channel.id]
    

client = MyClient()
client.run(settings_yaml['discord_selfbot_token'])