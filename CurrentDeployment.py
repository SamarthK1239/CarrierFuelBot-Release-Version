import os
import discord
from discord.ext.commands import Bot
import time
import psycopg2
import ssl


mydb = psycopg2.connect(
  host="your hosting link",
  user="username",
  password="password",
  database="database name here"
)

cursor = mydb.cursor()

data1 = ""

sql = "INSERT INTO fuel_levels (name, fuel_level, reserves, buy_order) VALUES (%s, %s, %s, %s)"
duplicate_sql = 'SELECT name from fuel_levels where name=%s;'
update_sql = "UPDATE fuel_levels SET fuel_level=%s WHERE name=%s;"
storage_update_sql = "UPDATE fuel_levels SET reserves=%s WHERE name=%s;"
bo_update_sql = "UPDATE fuel_levels SET buy_order=%s WHERE name=%s;"
delete_sql = 'DELETE FROM fuel_levels WHERE name=%s;'

bot = Bot(command_prefix=">")

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=" for >help"))
    print("bot online")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    else:
        embedVar = discord.Embed(title="Carrier Fuel Levels", description="", color=0x1abc9c)
        additionEmbed = discord.Embed(title="Add a Carrier", description="", color=0x1abc9c)
        helpEmbed = discord.Embed(title="Commands", description="", color=0xe67e22)
        updateEmbed = discord.Embed(title="Update a Carrier", description="", color=0xf1c40f)
        recommendationEmbed = discord.Embed(title="Recommended Carrier for Refuelling", description="", color=0xe74c3c)
        deleteEmbed = discord.Embed(title="Delete Carrier", description="", color=0xad1457)

        if '>fuel' in message.content:
             cursor.execute("SELECT * FROM fuel_levels;")
             myresult = cursor.fetchall()
             for x in myresult:
                 data1 = "**" + x[1] + "%** capacity + **"+ x[2] + "T** stored + **" + x[3] + "T** buy order"
                 embedVar.add_field(name=x[0], value=data1, inline=False)       
             await message.channel.send(embed=embedVar)
             time.sleep(1)
            
            
        if '>addCarrier' in message.content:
            editedMessage = (message.content).replace("%", "")
            editedMessage = editedMessage.replace("T", "")
            name = editedMessage[12: len(editedMessage)]
            name = name.split(";")
            print(name[0])
            for x in enumerate(name):
                name[x[0]] = x[1].strip()
                
            cursor.execute(duplicate_sql, (name[0], ))
            instances = len(cursor.fetchall())         
            if  instances == 0:
                try:
                    embed_data = "Added carrier " + name[0] + " which is at " + name[1] + "% fuel, has " + name[2] + "T in storage and a standing buy order for " + name[3] + "T of tritium"
                    data = (name[0], name[1], name[2])
                    additionEmbed.add_field(name='Added Carrier!', value=embed_data, inline=False)
                    await message.channel.send(embed=additionEmbed)
                    cursor.execute(sql, name)
                    mydb.commit()
                    time.sleep(1)
                except:
                    additionEmbed.add_field(name='An Error Occurred', value='Looks like something went wrong. Please check your syntax and try again.', inline=False)
                    await message.channel.send(embed=additionEmbed)
                    time.sleep(1)
            else:
                additionEmbed.add_field(name='Error', value='This carrier already exists. Try the updateCarrier command to update the fuel levels', inline=False)
                await message.channel.send(embed=additionEmbed)
                time.sleep(1)
                


        if '>help' in message.content:
            helpEmbed.add_field(name='Prompt', value='\">\"', inline=False)
            helpEmbed.add_field(name='fuel', value='Get the data for different carriers (syntax: >fuel)', inline=False)
            helpEmbed.add_field(name='addCarrier', value='Add a new carrier to the database\n(syntax: >addCarrier name;fuel level;fuel in storage;buy order)', inline=False)
            helpEmbed.add_field(name='updateCarrier', value='Update a carrier that already exists\n(syntax: >updateCarrier name;fuel level; fuel in storage;buy order)', inline=False)
            helpEmbed.add_field(name='removeCarrier', value='Remove a carrier that is in the database already. \n(syntax: >removeCarrier name)', inline=False)
            helpEmbed.add_field(name='help', value='This command', inline=False)

            await message.channel.send(embed=helpEmbed)
            time.sleep(1)

        if '>updateCarrier' in message.content:
            editedMessage = (message.content).replace("%", "")
            editedMessage = editedMessage.replace("T", "")
            name = editedMessage[14: len(editedMessage)]
            name = name.split(";")
            print(name[0])
            for x in enumerate(name):
                name[x[0]] = x[1].strip()
                
            cursor.execute(duplicate_sql, (name[0],))
            length = len(cursor.fetchall())
            if  length != 0:
                try:
                    cursor.execute(update_sql, (name[1], name[0]))
                    mydb.commit()
                    print("done")
                    cursor.execute(bo_update_sql, (name[3], name[0]))
                    mydb.commit()
                    print("done")
                    cursor.execute(storage_update_sql, (name[2], name[0]))
                    mydb.commit()
                    print("done")
                    updateEmbed.add_field(name='Completed!', value='The carrier data has been updated. Thanks!', inline=False)
                    await message.channel.send(embed=updateEmbed)
                    time.sleep(1)
                except:
                    additionEmbed.add_field(name='An Error Occurred', value='Looks like something went wrong. Please check your syntax and try again.', inline=False)
                    await message.channel.send(embed=additionEmbed)
                    time.sleep(1)
            else:
                updateEmbed.add_field(name='Error', value='Unable to find this carrier. Try adding it using the addCarrier command first.', inline=False)
                await message.channel.send(embed=updateEmbed)
                time.sleep(1)


        if '>removeCarrier' in message.content:
            data = message.content[15: len(message.content)]
            print(data)
            data = data.strip()
            cursor.execute(duplicate_sql, (data, ))
            instances = len(cursor.fetchall())
            if instances != 0:
                try:
                    cursor.execute(delete_sql, (data, ))
                    mydb.commit()
                    deleteEmbed.add_field(name="Done!", value="This carrier has been deleted from the database. If this was an error, please add the carrier back using the command.", inline=False)
                    await message.channel.send(embed=deleteEmbed)
                    time.sleep(1)
                except:
                    deleteEmbed.add_field(name="Error", value="Something went wrong, try again. If the problem persists, ping @Relic#1267", inline=False)
                    await message.channel.send(embed=deleteEmbed)
                    time.sleep(1)
            else:
                deleteEmbed.add_field(name="Error", value="That carrier doesn't seem to exist. Check if the carrier exists by using the fuel command, and check if your spelling is correct.", inline=False)
                await message.channel.send(embed=deleteEmbed)
                time.sleep(1)
        
bot.run('bot token here')
