
import os
import certifi
import ssl
import http.server
import socketserver
import threading
import os

def run_server():
    port = int(os.environ.get("PORT", 8080))
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        httpd.serve_forever()

threading.Thread(target=run_server, daemon=True).start()


ssl._create_default_https_context = ssl._create_unverified_context

# On configure le certificat AVANT toute chose
os.environ['SSL_CERT_FILE'] = certifi.where()

import random
import discord
from discord.ext import commands


# On prépare les permissions
intents = discord.Intents.default()
intents.message_content = True 

# On crée le bot
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    # Ça ajoute le petit texte sous son nom
    await bot.change_presence(activity=discord.Game(name="surveiller le serveur !"))
    print(f"Le bot {bot.user} est prêt et stylé !")


@bot.command()
async def salut(ctx):
    await ctx.send("Yo ! Je suis vivant !")

# Remplace les lettres ci-dessous par ton vrai Token
# Commande 1 : Voir la vitesse du bot
@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000) # Convertit en millisecondes
    await ctx.send(f"🏓 Pong ! Ma latence est de {latency}ms.")

# --- COMMANDES FUN ---

# 1. Voir l'avatar de quelqu'un
@bot.command()
async def avatar(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"📸 Avatar de {member.name}", color=discord.Color.blue())
    embed.set_image(url=member.avatar.url)
    await ctx.send(embed=embed)

# 2. Envoyer une image stylée au hasard (Chien/Chat/etc)
@bot.command()
async def image(ctx):
    # Liste d'images (tu peux en ajouter d'autres entre les guillemets !)
    images = [
        "https://placedog.net/500", 
        "https://cataas.com/cat",
        "https://loremflickr.com/320/240/brazil"
    ]
    url_image = random.choice(images)
    embed = discord.Embed(title="🖼️ Voici une image pour toi !", color=discord.Color.random())
    embed.set_image(url=url_image)
    await ctx.send(embed=embed)

# --- ÉVÉNEMENTS ---

# 3. Message de bienvenue automatique
@bot.event
async def on_member_join(member):
    channel = member.guild.system_channel # Trouve le salon principal
    if channel:
        await channel.send(f"👋 Bienvenue sur le serveur {member.mention} ! On est maintenant {member.guild.member_count} !")

# --- TON CODE 8BALL ET CLEAR (REMIS PROPREMENT) ---

@bot.command(name="8ball")
async def eight_ball(ctx, *, question):
    question_clean = question.lower()
    pseudo = ctx.author.name
    if "ton âge" in question_clean or "quel âge as-tu" in question_clean:
        reponse = "Je suis un bot, je suis né il y a quelques jours ! 👶"
    elif "mon âge" in question_clean:
        reponse = f"Écoute {pseudo}, t'as l'âge d'un génie ! 😎"
    elif "qui est le plus beau" in question_clean:
        reponse = f"C'est évidemment {pseudo} ! ✨"
    else:
        reponse = random.choice(["C'est certain !", "Peu probable.", "Fonce !", "Non."])
    await ctx.send(f"❓ **{question}**\n🎱 {reponse}")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"🧹 Supprimé {amount} messages !", delete_after=5)

# --- LANCEMENT ---

bot.run(os.getenv("DISCORD_TOKEN"))

