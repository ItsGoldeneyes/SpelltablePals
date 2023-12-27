import os
import requests
import discord
from discord import app_commands

'''
--------------
SETUP
--------------
'''

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

BACKEND_API = "https://backend-production-c33b.up.railway.app"
OWNER_USER_ID = "744739465045737623"

'''
--------------
SLASH COMMANDS
--------------
'''
@tree.command(
    name="sync",
    description="Sync the bot's commands",
    guild=discord.Object(id=1187847033596432394)
)
async def sync_command(interaction):
    if interaction.user.id == OWNER_USER_ID:
        await tree.sync(guild=discord.Object(id=1187847033596432394))
        response = "Synced!"
        await interaction.response.send_message(response, ephemeral=True)
    else:
        response = "You are not authorized to use this command."
        await interaction.response.send_message(response, ephemeral=True)

@tree.command(
    name="info",
    description="Get info about the bot",
    guild=discord.Object(id=1187847033596432394)
)
async def info_command(interaction):
    response = "Hello! /n\
I am a bot created by @Goldeneyes, /n\
I'm here to help you curate the SpellTable Pals experience. /n\
*For information about my commands, type /help.*"        
    await interaction.response.send_message(response, ephemeral=True)
    
@tree.command(
    name="help",
    description="Get help with the bot",
    guild=discord.Object(id=1187847033596432394)
)
async def help_command(interaction):
    response = "Here are my commands: /n\
*/info* - Get info about the bot /n\
*/help* - Get help with the bot /n\
*/ping* - Get the bot's latency /n\
*/block* - Submits a block request for a given SpellTable user. /n\
If you have any questions, please contact @Goldeneyes."       
    await interaction.response.send_message(response, ephemeral=True)
    
@tree.command(
    name="ping",
    description="Get the bot's latency",
    guild=discord.Object(id=1187847033596432394)
)
async def ping_command(interaction):
    response = f"Pong! {round(client.latency * 1000)}ms"        
    await interaction.response.send_message(response, ephemeral=True)
    
@tree.command(
    name="block",
    description="Submits a block request for a given SpellTable user",
    guild=discord.Object(id=1187847033596432394)
)
async def block_command(interaction, username: str, reason: str):
    if username == None or reason == None:
        response = "Please provide a username and a reason."
        await interaction.response.send_message(response, ephemeral=True)
        return
    
    api_response = requests.post(f"{BACKEND_API}/block_user", json={"username": username, "reason": reason})
    
    if api_response.status_code != 200:
        response = "Something went wrong. Please try again later."
        await interaction.response.send_message(response, ephemeral=True)
        return
    
    if api_response.json()["status"] != "Success":
        if api_response.json()["status"] == "Failed: chill":
            response = "User is Certified Chill, please contact a moderator if you would like to proceed."
            await interaction.response.send_message(response, ephemeral=True)
            return
        
        response = "Something went wrong. Please try again later."
        await interaction.response.send_message(response, ephemeral=True)
        return
        
    response = f"Block request submitted for {username} with reason: {reason}."        
    await interaction.response.send_message(response, ephemeral=True)
    return
    
@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=1187847033596432394))
    print("Ready!")
    
    
client.run(os.environ["DISCORD_TOKEN"])