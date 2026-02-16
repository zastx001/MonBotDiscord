import os
import discord
from discord.ext import commands
import random
import http.server
import socketserver
import threading

# 1. SERVEUR DE MAINTIEN (Pour Render)
def run_server():
    port = int(os.environ.get("PORT", 8080))
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Serveur Web OK sur port {port}")
        httpd.serve_forever()

threading.Thread(target=run_server, daemon=True).start()

# 2. SETUP DU BOT
intents = discord.Intents.default()
intents.message_content = True  # <-- IMPORTANT : Coche la case sur Discord aussi !
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'✅ SUCCÈS : {bot.user.name} est connecté à Discord !')

# 3. TES COMMANDES
@bot.command(name="8ball")
async def eight_ball(ctx, *, question):
    reponses = ["Oui", "Non", "Peut-être", "C'est certain !", "Peu probable."]
    await ctx.send(f"🎱 {random.choice(reponses)}")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"🧹 Supprimé {amount} messages !", delete_after=5)

# 4. LANCEMENT AVEC DEBUG
token = os.environ.get("DISCORD_TOKEN")
if token:
    print("Log : Tentative de connexion...")
    bot.run(token)
else:
    print("❌ ERREUR : Aucun DISCORD_TOKEN trouvé dans Render > Environment")
