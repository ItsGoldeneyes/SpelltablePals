import os
import requests
import discord
from discord import app_commands
from discord.ext import tasks, commands

ENVIRONMENT = os.environ["ENVIRONMENT"]
BACKEND_API = os.environ["BACKEND_API"]

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

SERVER_INFO = {}
SERVER_INFO[1187847033596432394] = {"guild_name": "Bot Test",
                                      "roles": {"chill": 1189712419996586055, "council": 1189712386509262948},
                                      "report_channel": 1189700021009010840,
                                      "mod_report_channel": 1189971481170563195,
                                      "invite_channel": 1210359718795542579}
SERVER_INFO[1073654117475569784] = {"guild_name": "SpellTable Pals",
                                        "roles": {"chill": 1073656663518744586, "council": 1091947617476415498},
                                        "report_channel": 1188131117035950160,
                                        "mod_report_channel": 1186943235470405692,
                                      "invite_channel": 1073654117475569786}

OWNER_USER_ID = 744739465045737623
BOT_ID = 1187847835920629881

class InviteCommands(commands.Cog):
    def __init__(self, client):
        self.client = client
    @tree.command(
    name="toggle_invite_link",
    description="Toggle the invite link for the bot"
    )
    async def toggle_invite_link_command(interaction):
        print("toggle_invite_link_command")
        user_roles = SERVER_INFO[interaction.guild.id]["roles"]
        if user_roles["council"] not in [role.id for role in interaction.user.roles]:
            response = "You are not authorized to use this command."
            await interaction.response.send_message(response, ephemeral=True)
            return

        api_response = requests.get(f"{BACKEND_API}/get_discord_invite")

        if api_response.status_code != 200:
            response = "Something went wrong. Please try again later."
            await interaction.response.send_message(response, ephemeral=True)
            return

        if api_response.json()["invite_link"] == "None":
            invite_link_enabled = True
            new_invite_link = await self.client.get_channel(SERVER_INFO[interaction.guild.id]["invite_channel"]).create_invite(max_age=0, max_uses=0, unique=True)
            api_response = requests.post(f"{BACKEND_API}/update_discord_invite", json={"invite_link": str(new_invite_link), "enabled": "None"})

        else:
            invite_link_enabled = False
            invite = await interaction.guild.invites()
            for i in invite:
                if i.url == api_response.json()["invite_link"]:
                    await i.delete()
                    break
            api_response = requests.post(f"{BACKEND_API}/update_discord_invite", json={"invite_link": "None", "enabled": "Toggle"})

        if api_response.status_code != 200:
            response = "Something went wrong. Please try again later."
            await interaction.response.send_message(response, ephemeral=True)
            return

        if api_response.json()["status"] != "Success":
            response = f"Error updating invite link: {api_response.json()['status']}"
            await interaction.response.send_message(response, ephemeral=True)
            return

        if invite_link_enabled:
            response = f"Invite link enabled!"
        else:
            response = f"Invite link disabled!"
        await interaction.response.send_message(response, ephemeral=True)
        return
    @commands.Cog.listener()
    async def on_ready(self):
        print("InviteCommands cog is ready.")

def setup(client) # Setup for the cog
    client.add_cog(InviteCommands(client)) # Add the class to the cog.