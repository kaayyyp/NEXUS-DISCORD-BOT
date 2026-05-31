import discord
from discord.ext import commands
import json
import os

class Setup(commands.Cog):
    """Setup & General Commands"""
    
    def __init__(self, bot):
        self.bot = bot
        self.config_file = "server_config.json"
        self.load_config()
    
    def load_config(self):
        """Load server configuration"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = {}
    
    def save_config(self):
        """Save server configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)
    
    @commands.command(name="setup")
    @commands.has_permissions(administrator=True)
    async def setup(self, ctx):
        """Setup case log channel and jail role"""
        guild_id = str(ctx.guild.id)
        case_channel = await ctx.guild.create_text_channel("📋-case-log")
        jail_role = await ctx.guild.create_role(name="Jailed", color=discord.Color.red())
        
        if guild_id not in self.config:
            self.config[guild_id] = {}
        
        self.config[guild_id]["case_log_channel"] = case_channel.id
        self.config[guild_id]["jail_role"] = jail_role.id
        self.save_config()
        
        embed = discord.Embed(title="✅ Server Setup Complete", description=f"Case Log Channel: {case_channel.mention}\nJail Role: {jail_role.mention}", color=discord.Color.green())
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Setup(bot))