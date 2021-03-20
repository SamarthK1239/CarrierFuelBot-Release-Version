import discord
from discord.ext import commands
from models.fuel import FuelIn, FuelOut
from db_manager import fuel_db

class Carrier(commands.Cog):
    bot: commands.Bot
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def get_fuel_from_user_by_name(self, ctx: commands.Context) -> FuelOut:
        def check(message: discord.Message):
            if ctx.author != message.author:
                return False
            return True

        await ctx.send('Enter the fuel name')
        fuel_name: str = (await self.bot.wait_for('message', check=check)).content.strip()

        retrieved_fuels = await fuel_db.get_fuels_by_name_and_guild(
            name=fuel_name,
            guild_id=ctx.guild.id
        )
        
        if len(retrieved_fuels) == 1:
            return retrieved_fuels[0]
        elif len(retrieved_fuels) == 0:
            await ctx.send('No carriers with that name were found!')
            return None

        fuels_embed = discord.Embed(title="Carrier Fuel Levels", description="", color=0x1abc9c)
        for i in range(0, len(retrieved_fuels)):
            fuel = retrieved_fuels[i]
            fuel_message = f"""
            **{fuel.fuel_level}%** Capacity + **{fuel.reserves}T** stored + buying tritium: **{fuel.buy_order}T**
            """
            fuels_embed.add_field(name=f'{i + 1}. {fuel.name}', value=fuel_message, inline=False)
    
        await ctx.send(embed=fuels_embed)
        await ctx.send('Please select the fuel')
        fuel_choice = int((await self.bot.wait_for('message', check=check)).content.strip())
        try:
            selected_fuel = retrieved_fuels[fuel_choice - 1]
            return selected_fuel
        except Exception:
            await ctx.send('Not a valid choice! Please try again')
            return None

    
    async def get_fuel_from_user(self, ctx: commands.Context, mode: str) -> FuelIn:
        def check(message: discord.Message):
            if ctx.author != message.author:
                return False
            return True

        fuel_name_prompt: str = None
        if mode.lower() == 'add':
            fuel_name_prompt = 'Enter the fuel name'
        elif mode.lower() == 'update':
            fuel_name_prompt = 'Enter the new fuel name'
            
        await ctx.send(fuel_name_prompt)
        fuel_name: str = (await self.bot.wait_for('message', check=check)).content.strip()

        await ctx.send('Enter the fuel level(capacity)')
        fuel_level = int((await self.bot.wait_for('message', check=check)).content.strip())
        if (fuel_level >=0 and fuel_level <= 100) == False:
            await ctx.send('Not a valid fuel level! Please try again')
            return None

        await ctx.send('Enter the reserves')
        reserves = float((await self.bot.wait_for('message', check=check)).content.strip())

        response_to_bool = {
            'y': True,
            'n': False,
            'yes': True,
            'no': False,
        }

        await ctx.send('Buying tritium(y/n or yes/no)')
        buy_order_response = str((await self.bot.wait_for('message', check=check)).content.strip()).strip().lower()
        if buy_order_response not in response_to_bool.keys():
            await ctx.send('Not a valid response. Please try again. You must only enter (y/n) or (yes/no)')
            return None
        buy_order = response_to_bool[buy_order_response]

        return FuelIn(
            name=fuel_name,
            fuel_level=fuel_level,
            reserves=reserves,
            buy_order=buy_order,
            guild_id=ctx.guild.id
        )
    
    @commands.command()
    async def ac(self, ctx: commands.Context):
        input_fuel = await self.get_fuel_from_user(
            ctx=ctx,
            mode='add',
        )
        if input_fuel == None:
            return None
        
        created_fuel = await fuel_db.insert_one_fuel(input_fuel)
        
        bool_to_response = {
            True: 'Yes',
            False: 'No',
        }
        created_message = f'''Added carrier **{created_fuel.name}** which is at **{created_fuel.fuel_level}**% 
        has **{created_fuel.reserves}T** in storage and buying tritium: **{bool_to_response[created_fuel.buy_order]}**
        '''
        add_embed = discord.Embed(title="Add a Carrier", description="", color=0x1abc9c)
        add_embed.add_field(name='Added Carrier!', value=created_message, inline=False)

        await ctx.send(embed=add_embed)
    
    @commands.command()
    async def uc(self, ctx: commands.Context):
        fuel_to_update = await self.get_fuel_from_user_by_name(ctx)
        if fuel_to_update == None:
            return None
        input_fuel = await self.get_fuel_from_user(
            ctx=ctx,
            mode='update',
        )
        if input_fuel == None:
            return None
            
        await fuel_db.update_one_fuel(fuel_to_update.id, input_fuel)
        update_embed = discord.Embed(title="Update a Carrier", description="", color=0xf1c40f)
        update_embed.add_field(name='Completed!', value='The carrier data has been updated. Thanks!', inline=False)
        await ctx.send(embed=update_embed)
    
    @commands.command()
    async def rc(self, ctx: commands.Context):
        fuel_to_delete = await self.get_fuel_from_user_by_name(ctx)
        if fuel_to_delete == None:
            return None
        delete_embed = discord.Embed(title="Delete Carrier", description="", color=0xad1457)
        try:
            await fuel_db.delete_one_fuel(fuel_to_delete.id)
            delete_embed.add_field(name="Done!", value="This carrier has been deleted from the database. If this was an error, please add the carrier back using the command.", inline=False)
        except Exception:
            delete_embed.add_field(name="Error", value="Something went wrong, try again. If the problem persists, ping @Relic#1267", inline=False)
        
        await ctx.send(embed=delete_embed)


def setup(bot: commands.Bot):
    bot.add_cog(Carrier(bot))

def teardown(bot: commands.Bot):
    bot.remove_cog('Carrier')
