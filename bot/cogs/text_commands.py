import discord
from discord.ext import commands
from database.repositories import TextRepository
from database.models import TextDocument
import logging

logger = logging.getLogger(__name__)

class TextCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.repo = TextRepository()
    
    @commands.command(name='save', help='Save a text document')
    async def save_text(self, ctx, title: str, *, content: str):
        try:
            document = TextDocument(
                title=title,
                content=content,
                author_id=ctx.author.id,
                author_name=str(ctx.author),
                guild_id=ctx.guild.id if ctx.guild else None,
                channel_id=ctx.channel.id
            )
            
            doc_id = self.repo.create(document)
            
            embed = discord.Embed(
                title="✅ Text Saved!",
                description=f"**Title:** {title}\\n**ID:** `{doc_id}`",
                color=discord.Color.green()
            )
            embed.set_footer(text=f"Saved by {ctx.author}")
            await ctx.send(embed=embed)
            
        except Exception as e:
            logger.error(f"Error saving text: {e}")
            await ctx.send("❌ Failed to save text.")
    
    @commands.command(name='get', help='Retrieve a text document by ID')
    async def get_text(self, ctx, document_id: str):
        try:
            document = self.repo.get_by_id(document_id)
            
            if not document:
                await ctx.send("❌ Document not found.")
                return
            
            embed = discord.Embed(
                title=document.title,
                description=document.content[:4000],  # Discord limit
                color=discord.Color.blue()
            )
            embed.add_field(name="Author", value=document.author_name, inline=True)
            embed.add_field(name="ID", value=document_id, inline=True)
            embed.set_footer(text=f"Created: {document.created_at.strftime('%Y-%m-%d %H:%M')}")
            
            await ctx.send(embed=embed)
            
        except Exception as e:
            logger.error(f"Error retrieving text: {e}")
            await ctx.send("❌ Failed to retrieve text.")
    
    @commands.command(name='mytexts', help='List your saved texts')
    async def my_texts(self, ctx, limit: int = 5):
        try:
            documents = self.repo.get_by_author(ctx.author.id, limit)
            
            if not documents:
                await ctx.send("📭 You haven't saved any texts yet.")
                return
            
            embed = discord.Embed(
                title=f"📚 Your Saved Texts ({len(documents)})",
                color=discord.Color.blue()
            )
            
            for doc in documents:
                embed.add_field(
                    name=doc.title,
                    value=f"ID: `{doc._id}`\\n{doc.content[:100]}...",
                    inline=False
                )
            
            await ctx.send(embed=embed)
            
        except Exception as e:
            logger.error(f"Error listing texts: {e}")
            await ctx.send("❌ Failed to retrieve your texts.")
    
    @commands.command(name='search', help='Search texts by title')
    async def search_texts(self, ctx, *, query: str):
        try:
            guild_id = ctx.guild.id if ctx.guild else None
            documents = self.repo.search_by_title(query, guild_id)
            
            if not documents:
                await ctx.send(f"🔍 No texts found matching '{query}'")
                return
            
            embed = discord.Embed(
                title=f"🔍 Search Results for '{query}'",
                description=f"Found {len(documents)} result(s)",
                color=discord.Color.blue()
            )
            
            for doc in documents[:10]:  # Limit to 10 results
                embed.add_field(
                    name=doc.title,
                    value=f"By {doc.author_name} - ID: `{doc._id}`",
                    inline=False
                )
            
            await ctx.send(embed=embed)
            
        except Exception as e:
            logger.error(f"Error searching texts: {e}")
            await ctx.send("❌ Failed to search texts.")
    
    @commands.command(name='delete', help='Delete your text by ID')
    async def delete_text(self, ctx, document_id: str):
        try:
            success = self.repo.delete(document_id, ctx.author.id)
            
            if success:
                await ctx.send("✅ Text deleted successfully!")
            else:
                await ctx.send("❌ Failed to delete text. Make sure the ID is correct and you own this text.")
                
        except Exception as e:
            logger.error(f"Error deleting text: {e}")
            await ctx.send("❌ Failed to delete text.")





async def setup(bot):
    await bot.add_cog(TextCommands(bot))