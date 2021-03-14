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

        retrieved_fuels = await fuel_db.get_fuels_by_name(fuel_name)

        fuels_embed = discord.Embed(title="Carrier Fuel Levels", description="", color=0x1abc9c)
        for i in range(0, len(retrieved_fuels)):
            fuel = retrieved_fuels[i]
            fuel_message = f'**{fuel.fuel_level}%** Capacity + **{fuel.reserves}T** stored + **{fuel.buy_order}T** Buy order'
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

    
    async def get_fuel_from_user(self, ctx: commands.Context) -> FuelIn:
        def check(message: discord.Message):
            if ctx.author != message.author:
                return False
            return True

        await ctx.send('Enter the fuel name')
        fuel_name: str = (await self.bot.wait_for('message', check=check)).content.strip()

        await ctx.send('Enter the fuel level(capacity)')
        fuel_level = int((await self.bot.wait_for('message', check=check)).content.strip())
        if (fuel_level >=0 and fuel_level <= 100) == False:
            await ctx.send('Not a valid fuel level! Please try again')
            return None

        await ctx.send('Enter the reserves')
        reserves = float((await self.bot.wait_for('message', check=check)).content.strip())

        await ctx.send('Enter the buy order')
        buy_order = int((await self.bot.wait_for('message', check=check)).content.strip())

        return FuelIn(
            name=fuel_name,
            fuel_level=fuel_level,
            reserves=reserves,
            buy_order=buy_order,
        )
    
    @commands.command()
    async def addCarrier(self, ctx: commands.Context):
        input_fuel = await self.get_fuel_from_user(ctx)
        if input_fuel == None:
            return None
        
        created_fuel = await fuel_db.insert_one_fuel(input_fuel)

        created_message = f'''Added carrier {created_fuel.name} which is at {created_fuel.fuel_level}% 
        has {created_fuel.reserves}T in storage and a standing buy order of {created_fuel.buy_order}
        '''
        add_embed = discord.Embed(title="Add a Carrier", description="", color=0x1abc9c)
        add_embed.add_field(name='Added Carrier!', value=created_message, inline=False)

        await ctx.send(embed=add_embed)
    
    @commands.command()
    async def updateCarrier(self, ctx: commands.Context):
        fuel_to_update = await self.get_fuel_from_user_by_name(ctx)
        if fuel_to_update == None:
            return None
        input_fuel = await self.get_fuel_from_user(ctx)
        if input_fuel == None:
            return None
            
        await fuel_db.update_one_fuel(fuel_to_update.id, input_fuel)
        update_embed = discord.Embed(title="Update a Carrier", description="", color=0xf1c40f)
        update_embed.add_field(name='Completed!', value='The carrier data has been updated. Thanks!', inline=False)
        await ctx.send(embed=update_embed)


def setup(bot: commands.Bot):
    bot.add_cog(Carrier(bot))

def teardown(bot: commands.Bot):
    bot.remove_cog('Carrier')
