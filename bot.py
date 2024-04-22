import os
import random
import shutil
import uuid
import PIL.Image
import discord
from discord.ext import commands, tasks
import requests
import responses
import sqlite3


#Setting up Chicken objects as Player Data
class Chicken:
    def __init__(self, ownerID=-1, str=-1, agl=-1, int=-1, mult=-1, mon=-1, tra=-1, ear=-1, cos=-1, cos2=""):
        self.ownerID = ownerID
        self.str = str
        self.agl = agl
        self.int = int
        self.mult = mult
        self.mon = mon
        self.tra = tra
        self.ear = ear
        self.cos = cos
        self.cos2 = cos2
        self.connection = sqlite3.connect("mydata.db")
        self.cursor = self.connection.cursor()

    # def load_chicken(self, id_number):
    #     self.cursor.execute(f"""
    #     SELECT * FROM chickens
    #     WHERE id = {id_number}
    #     """
    #     )
    #     results = self.cursor.fetchone()
    #     self.ownerID = id_number
    #     self.str = results[1]
    #     self.agl = results[2]
    #     self.int = results[3]

    def insert_person(self):
        print(self.cos2)
        self.cursor.execute(f"""
        INSERT INTO chickens VALUES
        ({self.ownerID}, {self.str}, {self.agl}, {self.int}, {self.mult}, {self.mon}, {self.tra}, {self.ear}, {self.cos}, "{self.cos2}") 
        """)
        self.connection.commit()
        self.connection.close()


def run_discord_bot(discord):
    TOKEN = os.environ['TOKEN']

    app_commands = discord.app_commands
    bot = commands.Bot(command_prefix=".?", intents=discord.Intents.all())
    bot.remove_command("help")

    chickens = []
    connection = sqlite3.connect("mydata.db")

    @bot.event
    async def on_ready():
        print("Slash Commands working")
        try:
            synced = await bot.tree.sync()
        except Exception as e:
            print(e)

        cursor = connection.cursor()
        # cursor.execute("""DROP TABLE chickens""")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS chickens(
            owner_ID INTEGER,
            str INTEGER,
            agl INTEGER,
            int INTEGER,
            mult INTEGER,
            mon INTEGER,
            tra INTEGER,
            ear INTEGER,
            cos INTEGER,
            cos2 TEXT

        )
        """)

        cursor.execute("SELECT * FROM chickens")
        results = cursor.fetchall()
        print(results)

        global chickens
        chickens = results
        check.start()

    @tasks.loop(seconds=20)
    async def check():
        global chickens

        cursor = connection.cursor()

        for i in range(len(chickens)):
            z = list(chickens[i])
            if z[7] < 86400:
                if z[6] == 1 and z[1] < 900000000:
                    if (z[1] == 1):
                        z[1] -= 1
                    z[1] += 20
                    z[7] += 20
                    z[5] += 1
                elif z[6] == 2 and z[2] < 900000000:
                    if (z[2] == 1):
                        z[2] -= 1
                    z[2] += 20
                    z[7] += 20
                    z[5] += 1
                elif z[6] == 3 and z[3] < 900000000:
                    if (z[3] == 1):
                        z[3] -= 1
                    z[3] += 20
                    z[7] += 20
                    z[5] += 1
            else:
                z[7] = 0
                z[6] = 0
            chickens[i] = tuple(z)

            cursor.execute(
                f"UPDATE chickens SET owner_ID=?, str=?, agl=?, int=?, mult=?, mon=?, tra=?, ear=?, cos=?, cos2=? WHERE owner_ID={chickens[i][0]}",
                chickens[i])
            connection.commit()

        print('test-tick')
        print(chickens)
        print(len(chickens))

    @bot.event
    async def on_message(message):
        if message.author != bot.user:
            username = str(message.author)
            user_message = str(message.content)
            channel = str(message.channel)

            print(f"{username} said: '{user_message}' ({channel})")
            await bot.process_commands(message)

    # NON-SLASH COMMAND
    @bot.command()
    async def help(ctx):
        await ctx.message.reply(responses.ai_response("help", None, None))

    @bot.command()
    async def helpchicken(ctx):
        await ctx.message.reply("Run **?mychicken** to view/initizalize your chicken (run it in a dm to not reveal your current power)\n\nRun **?trainchicken** to train one of your chicken's stats, default rate is 20 power every 20 seconds and $1 every 20 seconds, regardless of which stat you train.\nYour chicken will continue to train for 24 hours unless stopped using **?stoptrain**, or a duel commencing.\n\nRun **?duel {other player discord tag ping} {amount of money you want to bet}** to begin a duel\nDuels require both players to have the amount of money bet, and the winner takes all.\nWhen dueling, you may choose what stat you would like to duel with however, your probability increases/decreases depending on what style your opponent selects.\nIntelligence gets a 2x increase over strength, Strength gets a 2x increase over agility, and Agility gets a 2x increase over intelligence.\nThe player with the higher battle power after picking their style is not guaranteed to win, but they will have a higher probability of winning.\n\nRun **?skinshop** to view current skins (more to come), and use **?purchase {skin name in shop}** to purchase a skin")

    @bot.command()
    async def askpeter(ctx):
        try:
            input = ctx.message.content[10:]
            resp = responses.ai_response("askpeter", input, None)
            await ctx.message.reply(resp)
        except Exception as e:
            print(e)
            await ctx.message.reply("Please check your input and try again")

    @bot.command()
    async def askpeterpro(ctx):
        imageName = ''
        try:
            input = ctx.message.content[12:]
            r = requests.get(ctx.message.attachments[0], stream=True)
            imageName = str(uuid.uuid4()) + '.jpg'
            with open(imageName, 'wb') as out_file:
                print('Saving image: ' + imageName)
                shutil.copyfileobj(r.raw, out_file)
            img = PIL.Image.open(imageName)
            resp = responses.ai_response('askpeter2', input, img)
            os.remove(imageName)
            await ctx.message.reply(resp)
        except Exception as e:
            print(e)
            await ctx.message.reply(
                "An error occured, please try again, or contact the developer if this issue persists.")
            os.remove(imageName)

    @bot.command()
    async def mychicken(ctx):
        global chickens
        newChicken = True
        id = ctx.author.id
        str = 1
        agl = 1
        int = 1
        mult = 1
        mon = 20
        tra = 0
        ear = 0
        cos = 0
        cos2 = "default"
        for i in chickens:
            if i[0] == id:
                str = i[1]
                agl = i[2]
                int = i[3]
                mult = i[4]
                mon = i[5]
                tra = i[6]
                ear = i[7]
                cos = i[8]
                cos2 = i[9]
                newChicken = False
                break
        if newChicken:
            chick = Chicken(id, str, agl, int, mult, mon, tra, ear, cos, cos2)
            try:
                chick.insert_person()
            except Exception as e:
                print(e)

            chickens.append((id, str, agl, int, mult, mon, tra, ear, cos, cos2))

        resp = f"**Your Chicken (currently):**\nStrength: {str}\nAgility: {agl}\nIntelligence: {int}\n\nYou have ${mon}, and your current multiplier is: x{mult}\n"
        if (tra != 0):
            resp += 'Your Chicken is currently training.'
        if (cos == 0):
            resp += "https://imgur.com/CWw0OWA"
        elif(cos == 1):
            resp += "https://imgur.com/DQ8ZbTv"
        elif (cos == 2):
            resp += "https://imgur.com/88kMYDR"
        elif (cos == 3):
            resp += "https://imgur.com/yiTOZQQ"

        await ctx.reply(resp)

    @bot.command()
    async def trainchicken(ctx):
        global chickens
        for i in range(len(chickens)):
            z = list(chickens[i])
            if z[0] == ctx.author.id and z[6] <= 0:
                z[6] = -1
                chickens[i] = tuple(z)
                view = Menu1()
                await ctx.reply(view=view, ephemeral=True)
                return
        await ctx.reply("Run ?mychicken, and make sure your chicken is created and not currently training.")

    @bot.command()
    async def stoptrain(ctx):
        global chickens
        for i in range(len(chickens)):
            z = list(chickens[i])
            if z[0] == ctx.author.id and z[6] != 0:
                await ctx.reply("Stopped training chicken")
                z[6] = 0
                z[7] = 0
            chickens[i] = tuple(z)
            return
        await ctx.reply("Run ?mychicken, and make sure your chicken is created and currently training.")

    @bot.command()
    async def duel(ctx):
        global chickens

        c = None
        d = None
        amount = ''

        for i in range(len(ctx.message.content)):
            if ctx.message.content[len(ctx.message.content) - 1 - i].isdigit():
                amount = ctx.message.content[len(ctx.message.content) - 1 - i] + amount
            else:
                break

        #Check to see if amount is valid integer
        try:
            amount = int(amount)
            if amount < 0:
                await ctx.reply("Invalid input")
                return
        except Exception as e:
            print(amount)
            await ctx.reply("Invalid input")
            return

        for i in chickens:
            if i[0] == ctx.author.id and i[5] >= amount:
                c = ctx.author
        if c is None:
            await ctx.reply("Run ?mychicken, and check to see if you have enough money before trying again")
            return

        for i in ctx.guild.members:
            if i.mention in ctx.message.content:
                for j in (chickens):
                    print(len(chickens))
                    print(j[0])
                    print(j[5])
                    if j[0] == i.id and j[5] >= amount and j[0] != c.id:
                        d = i
                break
        if d is None:
            await ctx.reply(
                "The challenged player does not have a chicken activated or does not have enough money to match the bet. (have them run ?mychicken)")
            return

        await duelConfirm(c, d, amount, ctx)

    @bot.command()
    async def equip(ctx):
        global chickens
        for i in range(len(chickens)):
            z = list(chickens[i])
            if z[0] == ctx.author.id:
                if "default" in ctx.message.content:
                    z[8] = 0
                    await ctx.reply("Switched to default chicken.")
                elif "honored_chicken" in ctx.message.content and "honored_chicken" in z[9]:
                    z[8] = 1
                    await ctx.reply("Switched to honored chicken.")
                elif "bone_chicken" in ctx.message.content and "bone_chicken" in z[9]:
                    z[9] = 2
                    await ctx.reply("Switched to bone chicken.")
                elif "heisenberd" in ctx.message.content and "heisenberd" in z[9]:
                    z[9] = 2
                    await ctx.reply("Switched to heisen-berd.")

            chickens[i] = z

    @bot.command()
    async def cheat65379(ctx):
        global chickens
        for i in range(len(chickens)):
            z = list(chickens[i])
            if z[0] == ctx.author.id:
                z[5] += 1000000000
            chickens[i] = z

    @bot.command()
    async def purchase(ctx):
        global chickens
        for i in range(len(chickens)):
            z = list(chickens[i])
            if z[0] == ctx.author.id:
                if "honored_chicken" in ctx.message.content:
                    if "honored_chicken" in z[9]:
                        await ctx.reply("You already have this skin, (use ?equip)")
                    elif z[5] < 1000000:
                        await ctx.reply("You cannot afford this skin.")
                    else:
                        z[5] -= 1000000
                        z[9] += "honored_chicken"
                        await ctx.reply("You have purchased the honored chicken (use ?equip)")
                elif "bone_chicken" in ctx.message.content:
                    if "bone_chicken" in z[9]:
                        await ctx.reply("You already have this skin, (use ?equip)")
                    elif z[5] < 2000000:
                        await ctx.reply("You cannot afford this skin.")
                    else:
                        z[5] -= 2000000
                        z[9] += "bone_chicken"
                        await ctx.reply("You have purchased the honored chicken (use ?equip)")



            chickens[i] = z

    @bot.command()
    async def skinshop(ctx):
        await ctx.reply("**Current cosmetics shop:**\nHeisen-berd: $500000 (?purchase heisenberd) https://imgur.com/yiTOZQQ\nHonored Chicken: $1000000 (?purchase honored_chicken) https://imgur.com/DQ8ZbTv\nBone Chicken: $2000000 (?purchase bone_chicken) https://imgur.com/88kMYDR")

    async def duelConfirm(challenger, defender, amount, ctx):
        view = Menu2(challenger, defender, amount, ctx)
        await ctx.send(
            f"{defender.mention}, You are being challenged by {challenger.mention} for an amount of ${amount}. Would you like to accept?",
            view=view)

    async def beginDuel(challenger, defender, amount, c, d, ctx):
        view = Menu3(challenger, defender, amount, c, d, ctx)
        await ctx.send(
            f"A duel has started betweeen {challenger.mention} and {defender.mention}. Both players, click a button to choose what fighting style you will use? The winner will then be determined.",
            view=view)


    class Menu1(discord.ui.View):
        def __init__(self):
            super().__init__()
            self.value = None
            self.active = True

        @discord.ui.button(label="Train Strength", style=discord.ButtonStyle.red)
        async def str(self, interaction: discord.Interaction, button: discord.ui.button):
            if not self.active:
                await interaction.response.send_message("Inactive button", ephemeral=True)
                return
            global chickens
            for i in range(len(chickens)):
                z = list(chickens[i])
                if z[0] == interaction.user.id and z[6] == -1:
                    z[6] = 1
                    chickens[i] = tuple(z)
                    self.active = False
                    await interaction.response.send_message("Training Strength")
                    return
                chickens[i] = tuple(z)

            await interaction.response.send_message("Button not meant for you", ephemeral=True)
            return

        @discord.ui.button(label="Train Agility", style=discord.ButtonStyle.blurple)
        async def agl(self, interaction: discord.Interaction, button: discord.ui.button):
            if not self.active:
                await interaction.response.send_message("Inactive button", ephemeral=True)
                return
            global chickens
            for i in range(len(chickens)):
                z = list(chickens[i])
                if z[0] == interaction.user.id and z[6] == -1:
                    z[6] = 2
                    chickens[i] = tuple(z)
                    self.active = False
                    await interaction.response.send_message("Training Agility")
                    return
                chickens[i] = tuple(z)

            await interaction.response.send_message("Button not meant for you", ephemeral=True)
            return

        @discord.ui.button(label="Train Intelligence", style=discord.ButtonStyle.green)
        async def int(self, interaction: discord.Interaction, button: discord.ui.button):
            if not self.active:
                await interaction.response.send_message("Inactive button", ephemeral=True)
                return
            global chickens
            for i in range(len(chickens)):
                z = list(chickens[i])
                if z[0] == interaction.user.id and z[6] == -1:
                    z[6] = 3
                    chickens[i] = tuple(z)
                    self.active = False
                    await interaction.response.send_message("Training Intelligence")
                    return
                chickens[i] = tuple(z)

            await interaction.response.send_message("Button not meant for you", ephemeral=True)
            return

    class Menu2(discord.ui.View):
        def __init__(self, challenger, defender, amount, ctx):
            super().__init__()
            self.value = None
            self.challenger = challenger
            self.defender = defender
            self.amount = amount
            self.ctx = ctx
            self.active = True

        @discord.ui.button(label="Accept", style=discord.ButtonStyle.green)
        async def accept(self, interaction: discord.Interaction, button: discord.ui.button):
            if not self.active:
                await interaction.response.send_message("Inactive button", ephemeral=True)
                return
            global chickens
            c = None
            d = None
            if interaction.user == self.defender:
                for i in range(len(chickens)):
                    z = list(chickens[i])
                    if z[0] == self.challenger.id:
                        z[6] = 0
                        z[7] = 0
                        z[5] -= self.amount
                        c = z

                    elif z[0] == self.defender.id:
                        z[6] = 0
                        z[7] = 0
                        z[5] -= self.amount
                        d = z
                    chickens[i] = tuple(z)
                self.active = False
                await interaction.response.defer()
                await beginDuel(self.challenger, self.defender, self.amount, c, d, self.ctx)

            else:
                await interaction.response.send_message("Button not for you", ephemeral=True)
                return

        @discord.ui.button(label="Decline", style=discord.ButtonStyle.red)
        async def decline(self, interaction: discord.Interaction, button: discord.ui.button):
            if not self.active:
                await interaction.response.send_message("Inactive button", ephemeral=True)
                return
            if interaction.user == self.defender:
                self.active = False
                await interaction.responsedefer()
                await interaction.response.send_message("Challenge Declined")
                return
            else:
                await interaction.response.send_message("Button not for you", ephemeral=True)
                return

    class Menu3(discord.ui.View):
        def __init__(self, challenger, defender, amount, c, d, ctx):
            super().__init__()
            self.value = None
            self.challenger = challenger
            self.defender = defender
            self.amount = amount
            self.c = c
            self.d = d
            self.ctx = ctx

            self.startCount = 0
            self.cPower = 0
            self.cChoice = 0
            self.dPower = 0
            self.dChoice = 0

            self.active = True

        async def determineWinner(self, c, d):
            global chickens
            tp = c + d
            x = random.randint(1, tp)
            print(f"C: {c}")
            print(f"D: {d}")
            print(f"x: {x}")

            if x <= c:
                self.c[5] += self.amount * 2
                resp = f"{self.challenger.mention} is the Winner!"
                if (self.c[8] == 0):
                    resp += "https://imgur.com/CWw0OWA"
                elif (self.c[8] == 1):
                    resp += "https://imgur.com/DQ8ZbTv"
                elif (self.c[8] == 2):
                    resp += "https://imgur.com/88kMYDR"
                elif (self.c[8]  == 3):
                    resp += "https://imgur.com/yiTOZQQ"

                for i in range(len(chickens)):
                    if chickens[i][0] == self.c[0]:
                        chickens[i] = self.c
                await self.ctx.send(resp)


            else:
                self.d[5] += self.amount * 2
                resp = f"{self.defender.mention} is the Winner!"
                if (self.d[8] == 0):
                    resp += "https://imgur.com/CWw0OWA"
                elif (self.d[8] == 1):
                    resp += "https://imgur.com/DQ8ZbTv"
                elif (self.d[8] == 2):
                    resp += "https://imgur.com/88kMYDR"
                elif (self.d[8]  == 3):
                    resp += "https://imgur.com/yiTOZQQ"

                for i in range(len(chickens)):
                    if chickens[i][0] == self.c[0]:
                        chickens[i] = self.c
                await self.ctx.send(resp)

            return

        @discord.ui.button(label="Fight with Strength", style=discord.ButtonStyle.red)
        async def str(self, interaction: discord.Interaction, button: discord.ui.button):
            if not self.active:
                await interaction.response.send_message("Inactive button", ephemeral=True)
                return
            if interaction.user.id == self.challenger.id and self.startCount < 2:
                if self.startCount == 0:
                    self.startCount += 1
                    self.cPower = self.c[1]
                    self.cChoice = 1
                    await self.ctx.send("Challenger has Chosen, waiting for Defender's Choice")
                    return
                elif self.dChoice != 0:
                    self.startCount += 1
                    self.cPower = self.c[1]
                    if self.dChoice == 2:
                        self.cPower *= 2
                    elif self.dChoice == 3:
                        self.dPower *= 2
                    self.active = False
                    await interaction.response.defer()
                    await self.determineWinner(self.cPower, self.dPower)
                    return
            elif interaction.user.id == self.defender.id and self.startCount < 2:
                if self.startCount == 0:
                    self.startCount += 1
                    self.dPower = self.d[1]
                    self.dChoice = 1
                    await self.ctx.send("Defender has Chosen, waiting for Challenger's Choice")
                    return
                elif self.cChoice != 0:
                    self.startCount += 1
                    self.dPower = self.d[1]
                    if self.dChoice == 2:
                        self.cPower *= 2
                    elif self.dChoice == 3:
                        self.dPower *= 2
                    self.active = False
                    await interaction.response.defer()
                    await self.determineWinner(self.cPower, self.dPower)
                    return

            else:
                await interaction.response.send_message("Button not for you", ephemeral=True)
            return

        @discord.ui.button(label="Fight with Agility", style=discord.ButtonStyle.blurple)
        async def agl(self, interaction: discord.Interaction, button: discord.ui.button):
            if not self.active:
                await interaction.response.send_message("Inactive button", ephemeral=True)
                return
            if interaction.user.id == self.challenger.id and self.startCount < 2:
                if self.startCount == 0:
                    self.startCount += 1
                    self.cPower = self.c[2]
                    self.cChoice = 2
                    await interaction.response.defer()
                    await self.ctx.send("Challenger has Chosen, waiting for Defender's Choice")
                    return
                elif self.dChoice != 0:
                    self.startCount += 1
                    self.cPower = self.c[2]
                    if self.dChoice == 3:
                        self.cPower *= 2
                    elif self.dChoice == 1:
                        self.dPower *= 2
                    self.active = False
                    await interaction.response.defer()
                    await self.determineWinner(self.cPower, self.dPower)
                    return

            elif interaction.user.id == self.defender.id and self.startCount < 2:
                if self.startCount == 0:
                    self.startCount += 1
                    self.dPower = self.d[2]
                    self.dChoice = 2
                    await interaction.response.defer()
                    await self.ctx.send("Defender has Chosen, waiting for Challenger's Choice")
                    return
                elif self.cChoice != 0:
                    self.startCount += 1
                    self.dPower = self.d[2]
                    if self.dChoice == 3:
                        self.cPower *= 2
                    elif self.dChoice == 1:
                        self.dPower *= 2
                    self.active = False
                    await interaction.response.defer()
                    await self.determineWinner(self.cPower, self.dPower)
                    return

            else:
                await self.ctx.send("Button not meant for you")
            return

        @discord.ui.button(label="Fight with Intelligence", style=discord.ButtonStyle.green)
        async def int(self, interaction: discord.Interaction, button: discord.ui.button):
            if not self.active:
                await interaction.response.send_message("Inactive button", ephemeral=True)
                return
            if interaction.user.id == self.challenger.id and self.startCount < 2:
                if self.startCount == 0:
                    self.startCount += 1
                    self.cPower = self.c[3]
                    self.cChoice = 3
                    await interaction.response.defer()
                    await self.ctx.send("Challenger has Chosen, waiting for Defender's Choice")
                    return
                elif self.dChoice != 0:
                    self.startCount += 1
                    self.cPower = self.c[3]
                    if self.dChoice == 1:
                        self.cPower *= 2
                    elif self.dChoice == 2:
                        self.dPower *= 2
                    self.active = False
                    await interaction.response.defer()
                    await self.determineWinner(self.cPower, self.dPower)
                    return
            elif interaction.user.id == self.defender.id and self.startCount < 2:
                if self.startCount == 0:
                    self.startCount += 1
                    self.dPower = self.d[3]
                    self.dChoice = 3
                    await interaction.response.defer()
                    await self.ctx.send("Defender has Chosen, waiting for Challenger's Choice")
                    return
                elif self.cChoice != 0:
                    self.startCount += 1
                    self.dPower = self.d[3]
                    if self.dChoice == 1:
                        self.cPower *= 2
                    elif self.dChoice == 2:
                        self.dPower *= 2
                    self.active = False
                    await interaction.response.defer()
                    await self.determineWinner(self.cPower, self.dPower)
                    return
            else:
                await self.ctx.send("Button not meant for you")
            return

    # SLASH COMMANDS
    @bot.tree.command(name='askpeter', description='Responds as Peter Griffin from Family Guy')
    @app_commands.describe(input="What do you want to ask/tell Peter?")
    async def askpeter(interaction: discord.Interaction, input: str):
        try:
            await interaction.response.defer()
            resp = responses.ai_response("askpeter", input, None)
            await interaction.followup.send(resp)
        except Exception as e:
            print(e)
            await interaction.response.send_message("Failed")

    @bot.tree.command(name='askpeterpro', description='Responds to text input + images Peter Griffin from Family Guy')
    @app_commands.describe(input="What do you want to ask/tell Peter?")
    async def askpeter2(interaction: discord.Interaction, input: str, file: discord.Attachment):
        imageName = ''
        try:
            await interaction.response.defer()
            r = requests.get(file, stream=True)
            imageName = str(uuid.uuid4()) + '.jpg'
            with open(imageName, 'wb') as out_file:
                print('Saving image: ' + imageName)
                shutil.copyfileobj(r.raw, out_file)
            img = PIL.Image.open(imageName)
            resp = responses.ai_response('askpeter2', input, img)
            await interaction.followup.send(resp)
            os.remove(imageName)
        except Exception as e:
            print(e)
            await interaction.followup.send(
                "An error occured, please try again, or contact the developer if this issue persists.")
            os.remove(imageName)

    @bot.tree.command(name='help', description='List commands (non-slash commands)')
    async def help(interaction: discord.Interaction):
        try:
            await interaction.response.defer()
            resp = responses.ai_response("help", None, None)
            await interaction.followup.send(resp)
        except Exception as e:
            print(e)
            await interaction.response.send_message("Failed")

    bot.run(TOKEN)
