import discord
from discord.ext import commands

from db_manager import fuel_db
from db_manager.db_connector import db
from constants.environment import DISCORD_TOKEN

bot = commands.Bot(command_prefix=">")
bot.remove_command('help')

extension_names = [
    'extensions.carrier'
]

for extension_name in extension_names:
    bot.load_extension(extension_name)

@bot.command()
async def fuel(ctx: commands.Context):
    bool_to_response = {
        True: 'Yes',
        False: 'No'
    }
    fuels = await fuel_db.get_all_fuels_by_guild(guild_id=ctx.guild.id)
    if len(fuels) == 0:
        await ctx.send('No fuels for this server! Use the >addCarrier command to add one')
        return None
    fuels_embed = discord.Embed(title="Carrier Fuel Levels", description="", color=0x1abc9c)
    for fuel in fuels:
        fuel_message = f"""
        **{fuel.fuel_level}%** Capacity + **{fuel.reserves}T** stored + buying tritium: **{bool_to_response[fuel.buy_order]}**
        """
        fuels_embed.add_field(name=fuel.name, value=fuel_message, inline=False)
    
    await ctx.send(embed=fuels_embed)

@bot.command()
async def help(ctx):
    help_embed = discord.Embed(title="Commands", description="", color=0xe67e22)
    help_embed.add_field(name='Prompt', value='\">\"', inline=False)
    help_embed.add_field(name='fuel', value='Get the data for different carriers \n **Syntax: >fuel**', inline=False)
    help_embed.add_field(name='Add a Carrier', value='Add a new carrier to the database \n **Syntax: >ac name;fuel level;fuel in storage;buy order (y or n)**', inline=False)
    help_embed.add_field(name='Update a Carrier', value='Update a carrier that already exists \n **Syntax: >uc name;fuel level; fuel in storage;buy order (y or n)**', inline=False)
    help_embed.add_field(name='Remove a Carrier', value='Remove a carrier that is in the database already. **\n Syntax: >rc name**', inline=False)
    help_embed.add_field(name='help', value='This command', inline=False)

    await ctx.send(embed=help_embed)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=" for >help"))
    await db.connect()
    # Will only create table if it does not exist
    await fuel_db.create_fuels_table()
    print(f'Logged in as {bot.user}')

@bot.event
async def on_disconnect():
    print('disconnecting')
    await db.disconnect()
        
bot.run(DISCORD_TOKEN)
