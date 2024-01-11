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

SERVER_INFO = {}
SERVER_INFO[1187847033596432394] = {"guild_name": "Bot Test", 
                                      "roles": {"chill": 1189712419996586055, "council": 1189712386509262948}, 
                                      "report_channel": 1189700021009010840,
                                      "mod_report_channel": 1189971481170563195}
SERVER_INFO[1073654117475569784] = {"guild_name": "SpellTable Pals",
                                        "roles": {"chill": 1073656663518744586, "council": 1091947617476415498},
                                        "report_channel": 1188131117035950160,
                                        "mod_report_channel": 1186943235470405692}

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
    description="Sync the bot's commands"
    )
async def sync_command(interaction):
    if interaction.user.id == OWNER_USER_ID:
        response = "Synced!"
        await tree.sync()
        await interaction.response.send_message(response, ephemeral=True)
    else:
        response = "You are not authorized to use this command."
        await interaction.response.send_message(response, ephemeral=True)


@tree.command(
    name="info",
    description="Get info about the bot"
    )
async def info_command(interaction):
    response = "Hello! \n\
I'm here to help you have a better SpellTable experience! \n\
*For information about my commands, type /help.*"        
    await interaction.response.send_message(response, ephemeral=True)
    
    
@tree.command(
    name="help",
    description="Get help with the bot"
    )
async def help_command(interaction):
    response = "Here are my commands: \n\
*/info* - Get info about the bot \n\
*/help* - Get help with the bot \n\
*/ping* - Get the bot's latency \n\
*/block* - Submits a block request for a given SpellTable user. \n\
*/stats* - Get your SpellTable stats! \n\
If you have any questions, please contact @Goldeneyes."       
    await interaction.response.send_message(response, ephemeral=True)
    
    
@tree.command(
    name="ping",
    description="Get the bot's latency"
    )
async def ping_command(interaction):
    response = f"Pong! {round(client.latency * 1000)}ms"        
    await interaction.response.send_message(response, ephemeral=True)
    
    
@tree.command(
    name="block",
    description="Submits a block request for a given SpellTable user"
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
            
            for guild in client.guilds:
                report_channel = client.get_channel(SERVER_INFO[guild.id]["mod_report_channel"])
                if report_channel == None:
                    continue
                else:
                    await report_channel.send(f"{interaction.user.display_name} attempted to block {username} for reason {reason}, but {username} is a Certified Chill user.")
            
            response = "User is Certified Chill, please contact a moderator if you would like to proceed."
            await interaction.response.send_message(response, ephemeral=True)
            return
        
        response = "Something went wrong. Please try again later."
        await interaction.response.send_message(response, ephemeral=True)
        return
    for guild in client.guilds:
        report_channel = client.get_channel(SERVER_INFO[guild.id]["report_channel"])
        if report_channel == None:
            continue
        else:
            await report_channel.send(f"User **{username}** blocked by {interaction.user.display_name} for reason {reason}")
    
    
    response = f"Block request logged."        
    await interaction.response.send_message(response, ephemeral=True)
    return


@tree.command(
    name="unblock",
    description="Submits an unblock request for a given SpellTable user"
    )
async def unblock_command(interaction, username: str):
    user_roles = SERVER_INFO[interaction.guild.id]["roles"]
    if user_roles["council"] not in [role.id for role in interaction.user.roles]:
        response = "You are not authorized to use this command."
        await interaction.response.send_message(response, ephemeral=True)
        return
    
    if username == None:
        response = "Please provide a username."
        await interaction.response.send_message(response, ephemeral=True)
        return
    
    api_response = requests.post(f"{BACKEND_API}/unblock_user", json={"username": username})
    
    if api_response.status_code != 200:
        response = "Something went wrong. Please try again later."
        await interaction.response.send_message(response, ephemeral=True)
        return
    
    if api_response.json()["status"] != "Success":
        response = f"Error unblocking user: {api_response.json()['status']}"
        await interaction.response.send_message(response, ephemeral=True)
        return
    
    for guild in client.guilds:
        report_channel = client.get_channel(SERVER_INFO[guild.id]["mod_report_channel"])
        if report_channel == None:
            continue
        else:
            await report_channel.send(f"User **{username}** unblocked by {interaction.user.display_name}")
    
    response = f"Unblock request logged."        
    await interaction.response.send_message(response, ephemeral=True)
    return


@tree.command(
    name="stats",
    description="Get your SpellTable stats!"
)
async def stats_command(interaction, username: str):
    response = "This command is currently disabled."
    await interaction.response.send_message(response, ephemeral=True)
    # await interaction.response.defer()
    # if not username:
    #     username = interaction.user.display_name
    
    # api_response = requests.post(f"{BACKEND_API}/get_user_stats", json={"username": username})
    
    # if api_response.status_code != 200:
    #     response = "Something went wrong. Please try again later."
    #     await interaction.followup.send(response)
    #     return
    
    # if api_response.json()["status"] != "Success":
    #     response = f"Error getting stats: {api_response.json()['status']}"
    #     await interaction.followup.send(response)
    #     return
    
    # stats = api_response.json()["stats"]
    # response = f"Stats for {username}: \n\
    # **{stats['total_games']}** Games Played \n\
    # Most Played Commander: {stats['most_played_commander']} \n\
    # Most Played Color: {stats['most_played_color']} \n\
    # Most Played Opponent: {stats['most_played_opponent']} \n\
    # "
    # await interaction.followup.send(response)
    return


@tree.command(
    name="fetch",
    description="Fetches all users in bot's servers"
)
async def fetch_command(interaction):
    await interaction.response.defer()
    # Get all users in all servers bot is in
    request_body = {}
    for guild in client.guilds:
        user_roles = SERVER_INFO[guild.id]["roles"]
        for member in guild.members:
            if member.id == BOT_ID:
                continue
            if user_roles["council"] in [member_role.id for member_role in member.roles]:
                role = "council"
            elif user_roles["chill"] in [member_role.id for member_role in member.roles]:
                role = "chill"
            else:
                role = ''
            request_body[member.id] = {"role": role, "username": member.display_name}
            print(member.display_name)
            print(member.username)
            print(member.nick)
            print("----")
        
    api_response = requests.post(f"{BACKEND_API}/update_pal_profiles", json=request_body)
    if api_response.json()["status"] != "Success":
        print("Something went wrong. Please try again later.")
        return
    print("Users updated!")
    response = "Users updated!"
    await interaction.followup.send(response, ephemeral=True)

'''
--------------
LOOPS
--------------
'''

@tasks.loop(seconds = 21600)
async def fetch_users():
    '''
    Fetches all users in all servers bot is in and updates their roles through the api
    '''
    
    # Get all users in all servers bot is in
    request_body = {}
    for guild in client.guilds:
        user_roles = SERVER_INFO[guild.id]["roles"]
        for member in guild.members:
            if member.id == BOT_ID:
                continue
            if user_roles["council"] in [member_role.id for member_role in member.roles]:
                role = "council"
            elif user_roles["chill"] in [member_role.id for member_role in member.roles]:
                role = "chill"
            else:
                role = ''
            request_body[member.id] = {"role": role, "username": member.display_name}
        
    api_response = requests.post(url=f"{BACKEND_API}/update_pal_profiles", json=request_body)
    if api_response.json()["status"] != "Success":
        print("Something went wrong. Please try again later.")
        return
    print("Users updated!")
    
    
# @tasks.loop(seconds = 600)
# async def update_games():
#     '''
#     Triggers the backend to process the active games
#     '''

#     api_response = requests.request("POST", url=f"{BACKEND_API}/process_games", data={})    
#     if api_response.json()["status"] != "Success":
#         print("Something went wrong. Please try again later.")
#         return
#     print("Games updated!")
    
'''
--------------
START BOT
--------------
'''
    
@client.event
async def on_ready():
    print("Ready!")
    fetch_users.start()
    
    
client.run(os.environ["DISCORD_TOKEN"])