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
            # Measure bot latency
            start_time = time.time()
            message = await ctx.send("🏓 Pinging...")
            end_time = time.time()
            
            # Calculate response time
            response_time = (end_time - start_time) * 1000
            
            # Get websocket latency
            ws_latency = self.bot.latency * 1000
            
            # Create embed
            embed = discord.Embed(
                title="🏓 Pong!",
                color=discord.Color.green()
            )
            
            embed.add_field(
                name="Response Time",
                value=f"{response_time:.2f}ms",
                inline=True
            )
            
            embed.add_field(
                name="WebSocket Latency",
                value=f"{ws_latency:.2f}ms",
                inline=True
            )
            
            # Add status indicator
            if ws_latency < 100:
                status = "🟢 Excellent"
            elif ws_latency < 200:
                status = "🟡 Good"
            elif ws_latency < 300:
                status = "🟠 Fair"
            else:
                status = "🔴 Poor"
            
            embed.add_field(
                name="Status",
                value=status,
                inline=True
            )
            
            embed.set_footer(text=f"Requested by {ctx.author}")
            
            await message.edit(content=None, embed=embed)
            
        except Exception as e:
            logger.error(f"Error in ping command: {e}")
            await ctx.send("❌ Failed to check latency.")

async def setup(bot):
    await bot.add_cog(UtilityCommands(bot))