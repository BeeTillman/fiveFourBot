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
        global users
        thumbnail = discord.File("images/gift-box.png", filename="thumbnail.png")
        # NOTE: Initialize the embed
        embed = discord.Embed(
            title="FiveFour Randomizer Bot",
            description="React to this Message to Enter the drawing!",
            color=0xBEBEFE
        )
        embed.set_footer(text="Drawing Ends in: " + str(countdown) + "s", icon_url=None)
        embed.add_field(name="Entries:", value="0", inline=True)
        embed.add_field(name="Users:", value="None", inline=False)
        embed.set_thumbnail(url="attachment://thumbnail.png")
        msg = await context.send(embed=embed, files=[thumbnail])
        # NOTE: Add the reaction to the message
        await msg.add_reaction("🙋")
        time.sleep(1)
        # NOTE: Start the countdown and update the embed
        while countdown:
            msg = await context.fetch_message(msg.id)
            reaction = get(msg.reactions, emoji="🙋")
            users = set()
            # NOTE: Get all the users that reacted to the message and display the number of them and their names
            async for user in reaction.users():
                if user != self.bot.user:
                    users.add(user)
            if len(users) != 0:
                embed.set_field_at(0, name="Entries:", value=reaction.count-1, inline=True)
                embed.set_field_at(1, name="Users:", value=f"" ', '.join(user.name for user in users), inline=False)
            embed.set_footer(text="Drawing Ends in: " + str(countdown) + "s", icon_url=None)
            await msg.edit(embed=embed)
            countdown -= 1
            time.sleep(1)
        # NOTE: End the drawing and pick a winner
        embed.description = "Drawing Ended!"
        if len(users) == 0:
            embed.add_field(name="Winner: ", value="No one entered the drawing!", inline=True)
            embed.set_footer(text="Drawing Ended!", icon_url=None)
            await msg.edit(embed=embed)
            await msg.clear_reactions()
        else:
            winner = random.choice(list(users))
            embed.add_field(name="Winner: ", value=winner.name, inline=True)
            embed.set_footer(text="Drawing Ended!", icon_url=None)
            await msg.edit(embed=embed)
            await msg.clear_reactions()
            await context.send(f"Drawing Ended! The Winner is... <@" + str(winner.id) + ">")

async def setup(bot) -> None:
    await bot.add_cog(ResumeFunctions(bot))