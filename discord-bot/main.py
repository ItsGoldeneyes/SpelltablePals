import os
import requests
import discord
from discord import app_commands
from discord.ext import tasks

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

# Set TEST_SERVER to True if testing bot on the Test Server
TEST_SERVER = True
if TEST_SERVER:
    SPELLTABLE_PALS_GUILD_ID = 1187847033596432394 # Bot Test
    USER_ROLES = {"chill": 1189712419996586055, "council": 1189712386509262948}
    REPORT_CHANNEL = 1189700021009010840
else:
    SPELLTABLE_PALS_GUILD_ID = 1073654117475569784 # SpellTable Pals
    USER_ROLES = {"chill": 1073656663518744586, "council": 1091947617476415498}
    REPORT_CHANNEL = 1188131117035950160
    

BACKEND_API = "https://backend-production-c33b.up.railway.app"
OWNER_USER_ID = 744739465045737623
BOT_ID = 1187847835920629881

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
I am a bot created by @Goldeneyes, \n\
I'm here to help you curate the SpellTable Pals experience. \n\
*For information about my commands, type /help.*"        
    await interaction.response.send_message(response, ephemeral=True)
    
    
@tree.command(
    name="help",
    description="Get help with the bot",
    guild=discord.Object(id=1187847033596432394)
)
async def help_command(interaction):
    response = "Here are my commands: \n\
*/info* - Get info about the bot \n\
*/help* - Get help with the bot \n\
*/ping* - Get the bot's latency \n\
*/block* - Submits a block request for a given SpellTable user. \n\
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
    
    report_channel = client.get_channel(REPORT_CHANNEL)
    await report_channel.send(f"User {username} blocked by {interaction.username} for reason {reason}")
    
    response = f"Block request logged."        
    await interaction.response.send_message(response, ephemeral=True)
    return

'''
--------------
LOOP TO UPDATE USERS
--------------
'''

@tasks.loop(seconds = 100)
async def fetch_users():
    '''
    Fetches all users in all servers bot is in and updates their roles through the api
    '''
    
    # Get all users in all servers bot is in
    request_body = {}
    guild = client.get_guild(SPELLTABLE_PALS_GUILD_ID)
    for member in guild.members:
        if member.id == BOT_ID:
            continue
        if USER_ROLES["council"] in [member_role.id for member_role in member.roles]:
            role = "council"
        elif USER_ROLES["chill"] in [member_role.id for member_role in member.roles]:
            role = "chill"
        else:
            role = ''
        
        request_body[member.id] = {"role": role, "username": member.name}
        
    print(request_body)
'''
--------------
START BOT
--------------
'''
    
@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=1187847033596432394))
    print("Ready!")
    fetch_users.start()
    
    
client.run(os.environ["DISCORD_TOKEN"])