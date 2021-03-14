import discord
from discord.ext import commands
from models.fuel import FuelIn
from db_manager import fuel_db

class Carrier(commands.Cog):
    bot: commands.Bot
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    async def get_fuel_from_user(self, ctx: commands.Context) -> FuelIn:
        def check(message: discord.Message):
            if ctx.author != message.author:
                return False
            return True

        await ctx.send('Enter the fuel name')
        fuel_name: str = (await self.bot.wait_for('message', check=check)).content.strip()

        await ctx.send('Enter the fuel level')
        fuel_level = int((await self.bot.wait_for('message', check=check)).content.strip())

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
    async def devAddCarrier(self, ctx: commands.Context):
        input_fuel = await self.get_fuel_from_user(ctx)
        created_fuel = await fuel_db.insert_one_fuel(input_fuel)

        created_message = f'''Added carrier {created_fuel.name} which is at {created_fuel.fuel_level}% 
        has {created_fuel.reserves}T in storage and a standing buy order of {created_fuel.buy_order}
        '''
        add_embed = discord.Embed(title="Add a Carrier", description="", color=0x1abc9c)
        add_embed.add_field(name='Added Carrier!', value=created_message, inline=False)

        await ctx.send(embed=add_embed)
    
    @commands.command()
    async def devUpdateCarrier(self, ctx: commands.Context):
        await ctx.send('updateCarrierDev command')


def setup(bot: commands.Bot):
    bot.add_cog(Carrier(bot))

def teardown(bot: commands.Bot):
    bot.remove_cog('Carrier')
