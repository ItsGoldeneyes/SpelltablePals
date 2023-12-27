import os
import discord
from discord import app_commands


intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@tree.command(
    name="commandname",
    description="My first application Command",
    guild=discord.Object(id=1187847033596432394)
)
async def first_command(interaction):
    await interaction.response.send_message("Hello!")
    
@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=1187847033596432394))
    print("Ready!")
    
    
client.run(os.environ["DISCORD_TOKEN"])