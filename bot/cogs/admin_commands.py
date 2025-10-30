import discord
from discord.ext import commands
from database.repositories import TextRepository
import logging

logger = logging.getLogger(__name__)

class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.repo = TextRepository()
    
    @commands.command(name='stats', help='Show database statistics')
    @commands.has_permissions(administrator=True)
    # @commands.has_role(123456789012345678)   role id

    
    async def stats(self, ctx):
        try:
            guild_id = ctx.guild.id if ctx.guild else None
            stats = self.repo.get_stats(guild_id)
            
            embed = discord.Embed(
                title="📊 Database Statistics",
                color=discord.Color.gold()
            )
            
            embed.add_field(
                name="Total Documents",
                value=stats['total_documents'],
                inline=True
            )
            
            if stats['top_authors']:
                top_text = "\\n".join([
                    f"<@{author['_id']}>: {author['count']} texts"
                    for author in stats['top_authors'][:5]
                ])
                embed.add_field(
                    name="Top Contributors",
                    value=top_text,
                    inline=False
                )
            
            await ctx.send(embed=embed)
            
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            await ctx.send("❌ Failed to retrieve statistics.")
    
    @commands.command(name='servertexts', help='List recent texts in this server')
    @commands.has_permissions(manage_messages=True)
    async def server_texts(self, ctx, limit: int = 10):
        try:
            if not ctx.guild:
                await ctx.send("❌ This command can only be used in a server.")
                return
            
            documents = self.repo.get_by_guild(ctx.guild.id, limit)
            
            if not documents:
                await ctx.send("📭 No texts saved in this server yet.")
                return
            
            embed = discord.Embed(
                title=f"📚 Recent Server Texts ({len(documents)})",
                color=discord.Color.blue()
            )
            
            for doc in documents:
                embed.add_field(
                    name=doc.title,
                    value=f"By {doc.author_name} - ID: `{doc._id}`",
                    inline=False
                )
            
            await ctx.send(embed=embed)
            
        except Exception as e:
            logger.error(f"Error listing server texts: {e}")
            await ctx.send("❌ Failed to retrieve server texts.")

async def setup(bot):
    await bot.add_cog(AdminCommands(bot))