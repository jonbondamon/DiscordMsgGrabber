import yaml, discord, os
from discord_webhook import DiscordEmbed, DiscordWebhook

with open("settings.yml", mode="r") as yaml_file:
        settings_yaml = yaml.safe_load(yaml_file)

mention = settings_yaml['mention']

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

def replaceMentions(content):
    content_split = content.split(' ')
    for segment in content_split:
        if segment.find('<@') != -1:
            segment = mention
    content_filtered = ''.join(content_split)
    return content_filtered

async def sendMsg(msg, server):

    user = msg.author
    pfp = user.avatar_url
    images = msg.attachments
    content = msg.content
    channel = server[msg.channel.id]
    color = server['color']

    webhook = DiscordWebhook(url='https://discord.com/api/webhooks/1038936830566993940/qaEEoacHhIxsEemHWcbcTDBSBli529W8svTzj_pBWrr75FKZ-YF0Nxh8Nv76BLMyFlMf')
    embed = DiscordEmbed()
    embedCounter = 0

    embed.set_author(name=user.name, icon_url=str(pfp))

    first_img = True

    if content != '':

        content = replaceMentions(content)
        embed.set_description(content)
        embed.set_footer(text=channel)
        embed.set_color(color=color)
        embed.set_timestamp()
        webhook.add_embed(embed=embed)
        embedCounter = embedCounter + 1
        first_img = False

    if images:
        for image in images:
            if embedCounter == 10:
                webhook.execute(remove_embeds=True)
                embedCounter = 0
                first_img = True
            embed_img = DiscordEmbed()
            if first_img:
                embed_img.set_footer(text=channel)
                first_img = False
            filename, file_extension = os.path.splitext(image.url)
            if file_extension in ['.jpg', '.jpeg', '.gif', '.png', '.eps', '.raw']:
                embed_img.set_image(url = image.url)
            else: 
                embed_img.set_title(image.filename)
                embed_img.set_url(image.url)
            embed_img.set_color(color=color)
            embed_img.set_author(name=user.name, icon_url=str(pfp))
            embed_img.set_timestamp()
            webhook.add_embed(embed=embed_img)
            embedCounter = embedCounter + 1

    webhook.execute(remove_embeds=True)




    

client = MyClient()
client.run(settings_yaml['discord_selfbot_token'])