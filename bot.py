import discord
from discord.ext import commands

from db_manager import fuel_db
from db_manager.db_connector import db
from constants.environment import DISCORD_TOKEN

bot = commands.Bot(command_prefix=">")

extension_names = [
    'extensions.carrier'
]

for extension_name in extension_names:
    bot.load_extension(extension_name)

@bot.command()
async def fuels(ctx: commands.Context):
    fuels = await fuel_db.get_all_fuels_by_guild(guild_id=ctx.guild.id)
    if len(fuels) == 0:
        await ctx.send('No fuels for this server! Use the >addCarrier command to add one')
        return None
    fuels_embed = discord.Embed(title="Carrier Fuel Levels", description="", color=0x1abc9c)
    for fuel in fuels:
        fuel_message = f'**{fuel.fuel_level}%** Capacity + **{fuel.reserves}T** stored + **{fuel.buy_order}T** Buy order'
        fuels_embed.add_field(name=fuel.name, value=fuel_message, inline=False)
    
    await ctx.send(embed=fuels_embed)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=" for >help"))
    await fuel_db.create_fuels_table()
    print(f'Logged in as {bot.user}')

@bot.event
async def on_disconnect():
    print('disconnecting')
    await db.disconnect()
        
bot.run(DISCORD_TOKEN)
