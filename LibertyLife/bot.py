from discord.ext import commands
import discord
from cogs.utils import checks
import datetime, re
import json, asyncio
import copy
import logging
from logging.handlers import RotatingFileHandler
import traceback
import sys
from collections import Counter

description = """
Je suis LibertyLife, le bot officiel de Liberty Life RP sur PS3/PS4 ! ;)
"""

l_extensions = [

    'cogs.basics',
    #'cogs.test',
    'cogs.admin',
    'cogs.funs',
    'cogs.utility',
    'cogs.search',
    'cogs.ci'
]

# DISCORD LOGGER #
discord_logger = logging.getLogger('discord')
discord_logger.setLevel(logging.CRITICAL)
log = logging.getLogger()
log.setLevel(logging.INFO)
handler = logging.FileHandler(filename='logs/discord.log', encoding='utf-8', mode='w')
log.addHandler(handler)

help_attrs = dict(hidden=True, in_help=True, name="DONOTUSE")


# CREDENTIALS #
try:
    def load_credentials():
        with open('params.json') as f:
            return json.load(f)
except:
    print("Le fichier de paramètre est introuvable, veuillez le créer et le configurer.")

credentials = load_credentials()
prefix = credentials.get("prefix", ["-"])
bot = commands.Bot(command_prefix=prefix, description=description, pm_help=None, help_attrs=help_attrs)

@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.NoPrivateMessage):
        await bot.send_message(ctx.message.author, 'Cette commande ne peut pas être utilisée en message privée.')
    elif isinstance(error, commands.DisabledCommand):
        await bot.send_message(ctx.message.author, 'Désoler mais cette commande est désactivé, elle ne peut donc pas être utilisée.')
    elif isinstance(error, commands.CommandInvokeError):
        print('In {0.command.qualified_name}:'.format(ctx), file=sys.stderr)
        traceback.print_tb(error.original.__traceback__)
        print('{0.__class__.__name__}: {0}'.format(error.original), file=sys.stderr)

@bot.event
async def on_ready():
    print('---------------------')
    print('CONNECTÉ :')
    print("""   Nom d\'utilisateur : {0.name}#{0.discriminator}
   ID : {0.id}""".format(bot.user))
    print('Merci d\'utiliser Eve-Dj')
    print('---------------------')
    await bot.change_presence(game=discord.Game(name=credentials.get("game", "Spyrisk#2089|-help")), status=discord.Status("dnd"), afk=False)
    if bot.client_id == None: 
        bot.client_id = bot.user.id
    if not hasattr(bot, 'uptime'):
        bot.uptime = datetime.datetime.utcnow()

@bot.event
async def on_resumed():
    print('resumed...')

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    try:
        await bot.process_commands(message)
    except Exception as e:
        print('Erreur rencontré : \n {}: {} \n \n'.format(type(e).__name__, e))

@bot.command(pass_context=True, hidden=True)
@checks.is_owner()
async def do(ctx, times : int, *, command):
    """Repeats a command a specified number of times."""
    msg = copy.copy(ctx.message)
    msg.content = command
    for i in range(times):
        await bot.process_commands(msg)

async def on_command_error(self, ctx, error):
    if isinstance(error, commands.NoPrivateMessage):
        await ctx.author.send('Cette commande ne peut pas être utilisée en message privée.')
    elif isinstance(error, commands.DisabledCommand):
        await ctx.author.send('Désoler mais cette commande est désactivé, elle ne peut donc pas être utilisée.')
    elif isinstance(error, commands.CommandInvokeError):
        print(f'In {ctx.command.qualified_name}:', file=sys.stderr)
        traceback.print_tb(error.original.__traceback__)
        print(f'{error.original.__class__.__name__}: {error.original}', file=sys.stderr)

## LOAD ##
if __name__ == '__main__':
    try:
        credentials = load_credentials()
        token = credentials.get('token')
		if token is None:
			print("/!\ Le token est manquant dans le fichier params.json...")
        bot.client_id = credentials.get('client_id', None)
    except:
        print("Impossible de démarer LibertyLife dû à une erreur inconnue.")


    for extension in l_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print('Impossible de charger l\'extension {}\n{}: {}'.format(extension, type(e).__name__, e))

    try:
        bot.run(token)
    except:
        print("Une erreur est survenue avec votre Token, merci de le vérifier.")

    handlers = log.handlers[:]
    for hdlr in handlers:
        hdlr.close()
log.removeHandler(hdlr)