import platform
import random

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from discord.utils import get
import time


class ResumeFunctions(commands.Cog, name="resumeFunctions"):

    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(
        name="startpicker",
        description="Starts a random user picker.",
    )
    @app_commands.describe(countdown="The time to wait for users to react.")
    async def start_picker(
            self, context: Context, *, countdown: int
    ) -> None:
        embed = discord.Embed(title="FiveFour Randomizer Bot", description="React to this Message to Enter the drawing!", color=0xBEBEFE)
        embed.set_footer(text="Drawing Ends in: " + str(countdown) + "s", icon_url=None)
        embed.add_field(name="Entries:", value="0", inline=True)
        msg = await context.send(embed=embed)
        await msg.add_reaction("✅")
        time.sleep(1)
        while countdown:
            msg = await context.fetch_message(msg.id)
            reaction = get(msg.reactions, emoji="✅")
            embed.set_field_at(0, name="Entries:", value=reaction.count, inline=True)
            embed.set_footer(text="Drawing Ends in: " + str(countdown) + "s", icon_url=None)
            await msg.edit(embed=embed)
            countdown -= 1
            time.sleep(1)
        embed.set_footer(text="Drawing Ended!", icon_url=None)
        await msg.edit(embed=embed)

        time.sleep(3)


async def setup(bot) -> None:
    await bot.add_cog(ResumeFunctions(bot))