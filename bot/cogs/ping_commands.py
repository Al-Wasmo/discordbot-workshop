import discord
from discord.ext import commands
import time
import logging

logger = logging.getLogger(__name__)

class UtilityCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='ping', help='Check bot latency')
    async def ping(self, ctx):
        try:
            message = await ctx.send("🏓 Pinging...")


            time.sleep(4)
                        
            # Create embed
            embed = discord.Embed(
                title="🏓 Pong!",
                color=discord.Color.green()
            )
            
            await message.edit(content=None, embed=embed)
            
        except Exception as e:
            logger.error(f"Error in ping command: {e}")
            await ctx.send("❌ Failed to check latency.")

async def setup(bot):
    await bot.add_cog(UtilityCommands(bot))