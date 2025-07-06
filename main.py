from dis import disco
import logging
import discord
from discord.ext import commands
from discord import app_commands
import uuid
import json
import os

# Bot token and logging
TOKEN = os.getenv('TOKEN')
if TOKEN == None:
    raise Exception('Please Set the Discord Token ENV to run the bot')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
logging.basicConfig(level=logging.INFO, handlers=[handler])
logger = logging.getLogger(__name__)

# Discord intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)
GUILD_ID = 520992651571626014
GUILD = discord.Object(id=GUILD_ID)

# --- ATTACKS ---
class Attack:
    def __init__(self, name: str, damage: str, description: str | None = None, to_hit: int = 0, id: str | None = None):
        if id != None:
            self.id = uuid.UUID(id)
        else:
            self.id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.to_hit = to_hit
        self.damage = damage
    
    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "to_hit": self.to_hit,
            "damage": self.damage
        }
    
    def __str__(self):
        return f"**{self.name}**\n{self.description}\n*To-hit: {self.to_hit}*\n*Damage: {self.damage}*\n"


ATTACKS: dict[str, list[Attack]] = {}

def load_attacks():
    with open('attacks.json', 'r') as f:
        atk_dict: dict[str, dict] = json.load(f)
        for attack in atk_dict:
            ATTACKS[attack] = [Attack(**atk) for atk in atk_dict[attack]]

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    logger.info(f"Bot logged in as {bot.user}")
    # Sync commands for the guild
    await bot.tree.sync(guild=GUILD)
    print("Commands synced!")
    # Load attacks from file
    load_attacks()

# --- SLASH COMMANDS ---
@bot.tree.command(name='create', description='Create a new attack type', guild=GUILD)
@app_commands.describe(name='Name of the attack', description='Description of the attack', to_hit='To-hit bonus', damage='Damage dice string (e.g. 1d6)')
async def create_slash(interaction: discord.Interaction, name: str, description: str | None = None, to_hit: int = 0, damage: str = "1d6"):
    try:
        attack = Attack(name, damage, description, to_hit)
        if str(interaction.user.id) not in ATTACKS:
            ATTACKS[str(interaction.user.id)] = []
        ATTACKS[str(interaction.user.id)].append(attack)
        with open('attacks.json', 'w') as f:
            atk_dict = {}
            for atk in ATTACKS:
                atk_dict[atk] = [attck.json() for attck in ATTACKS[atk]]
            json.dump(atk_dict, f, indent=4)
    except Exception as e:
        await interaction.response.send_message(f"Exception occured: {e}")
    await interaction.response.send_message(f"Attack {attack.name} created successfully")

@bot.tree.command(name='list', description='List all attacks for the current user', guild=GUILD)
async def list_slash(interaction: discord.Interaction):
    logger.debug(f"Interaction User ID {interaction.user.id}")
    
    msg = ["**Attacks Created**\n"]
    if str(interaction.user.id) not in ATTACKS:
        await interaction.response.send_message("**You have no attacks!**\nCreate an attack using the `/create` command")
        return
    attack = ATTACKS[str(interaction.user.id)]
    msg.extend([str(atk) for atk in attack])
    await interaction.response.send_message("\n".join(msg))

bot.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)
