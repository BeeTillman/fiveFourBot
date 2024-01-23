import platform
import random

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context


class ResumeFunctions(commands.Cog, name="resumeFunctions"):

    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(
        name="startpicker",
        description="Starts a random user picker.",
    )
    @app_commands.guilds(discord.Object(id=882708596437534996))
    async def start_picker(
            self, context: Context
    ) -> None:
        embed = discord.Embed(description="What is your bet?", color=0xBEBEFE)
        await context.send(embed=embed)

async def setup(bot) -> None:
    await bot.add_cog(ResumeFunctions(bot))