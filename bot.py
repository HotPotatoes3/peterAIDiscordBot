import os
import shutil
import uuid
import PIL.Image

import discord
from discord.ext import commands

import requests

import responses






#sending messages through non-slash commands
async def send_message(message, user_message):
    try:
        response = responses.handle_response(user_message)
        await message.reply(response)
    except Exception as e:
        print(e)


intents = discord.Intents.default()
intents.message_content = True

def run_discord_bot(discord):

    app_commands = discord.app_commands

    TOKEN = os.environ['TOKEN']

    bot = commands.Bot(command_prefix="?", intents=discord.Intents.all())



    #NON-SLASH COMMANDS
    @bot.event
    async def on_message(message):
        if message.author != bot.user:
            username = str(message.author)
            user_message = str(message.content)
            channel = str(message.channel)

            print(f"{username} said: '{user_message}' ({channel})")

            if(len(message.attachments) == 0):
                await send_message(message, user_message)
            elif(message.content[0:10] == '?askpeter+'):
                url = message.attachments[0].url
                if url[0:26] == "https://cdn.discordapp.com":
                    r = requests.get(url, stream=True)
                    imageName = str(uuid.uuid4()) +'.jpg'
                    with open(imageName, 'wb') as out_file:
                        print('Saving image: ' + imageName)
                        shutil.copyfileobj(r.raw,out_file)
                    img = PIL.Image.open(imageName)

                    await message.reply(responses.image_to_text(message.content[11:], img))
                    os.remove(imageName)







    @bot.event
    async def on_ready():
        print("Slash Commands working")
        try:
            synced = await bot.tree.sync()
            print(f"Synced {len(synced)} command(s)")
            for i in synced:
                print(i)
        except Exception as e:
            print(e)

    # SLASH COMMANDS
    @bot.tree.command(name='askpeter')
    @app_commands.describe(input = "What do you want to ask/tell Peter?")
    async def askpeter(interaction: discord.Interaction, input: str):
        try:
            await interaction.response.defer()
            resp = responses.slash_response("askpeter", input)
            await interaction.followup.send(resp)
        except Exception as e:
            print(e)
            await interaction.response.send_message("Failed")

    @bot.tree.command(name='help')
    async def help(interaction: discord.Interaction):
        await interaction.response.send_message('**Commands:**\n\n**?askpeter {Your question/statement}:** Responds as Peter Griffin from Family Guy')



    bot.run(TOKEN)
