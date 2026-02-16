import os
import discord
from discord.ext import commands
import threading
import http.server
import socketserver

# --- SERVEUR DE MAINTIEN (RENDER) ---
def run_server():
    port = int(os.environ.get("PORT", 8080))
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        httpd.serve_forever()
threading.Thread(target=run_server, daemon=True).start()

# --- CONFIG BOT ---
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'✅ EN LIGNE : {bot.user.name}')

@bot.command()
async def ping(ctx):
    await ctx.send('Pong ! 🏓')

# --- LANCEMENT ---
token = os.environ.get("DISCORD_TOKEN")
bot.run(token)
