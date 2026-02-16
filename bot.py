import os
import discord
from discord.ext import commands
import random
import http.server
import socketserver
import threading
import certifi
import ssl

# --- 1. MOTEUR RENDER (Pour garder le bot vivant) ---
def run_server():
    port = int(os.environ.get("PORT", 8080))
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        httpd.serve_forever()

threading.Thread(target=run_server, daemon=True).start()

# --- 2. CONFIGURATION SSL (Pour éviter les erreurs Mac) ---
ssl._create_default_https_context = ssl._create_unverified_context
os.environ['SSL_CERT_FILE'] = certifi.where()

# --- 3. CRÉATION DU BOT ---
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'✅ {bot.user.name} est EN LIGNE !')

# --- 4. TES COMMANDES (8ball & Clear) ---
@bot.command(name="8ball")
async def eight_ball(ctx, *, question):
    question_clean = question.lower()
    pseudo = ctx.author.name
    if "ton âge" in question_clean:
        reponse = "Je suis un bot, je suis né il y a quelques jours !"
    elif "qui est le plus beau" in question_clean:
        reponse = f"C'est évidemment {pseudo} ! ✨"
    else:
        reponses = ["C'est certain !", "Peu probable.", "Oui !", "Non."]
        reponse = random.choice(reponses)
    await ctx.send(f"❓ **{question}**\n🎱 {reponse}")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"🧹 Supprimé {amount} messages !", delete_after=5)

# --- LANCEMENT FINAL ---
token = os.environ.get("DISCORD_TOKEN")
if token:
    print("Tentative de connexion à Discord...")
    bot.run(token)
else:
    print("ERREUR : DISCORD_TOKEN introuvable dans Render > Environment")

