import os

import discord
from discord.ext import commands

import responses

#sending messages through non-slash commands
async def send_message(message, user_message, is_private):
    try:
        response = responses.handle_response(user_message)
        await message.author.send(response) if is_private else await message.reply(response)
    except Exception as e:
        return


intents = discord.Intents.default()
intents.message_content = True

def run_discord_bot(discord):

    app_commands = discord.app_commands

    TOKEN = os.environ['TOKEN']

    client = discord.Client(intents=intents)
    bot = commands.Bot(command_prefix="?", intents=discord.Intents.all())

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')


    #NON-SLASH COMMANDS
    @bot.event
    async def on_message(message):
        if message.author != client.user:
            username = str(message.author)
            user_message = str(message.content)
            channel = str(message.channel)

            print(f"{username} said: '{user_message}' ({channel})")

            await send_message(message, user_message, is_private=False)

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



    # client.run(TOKEN)
    bot.run(TOKEN)