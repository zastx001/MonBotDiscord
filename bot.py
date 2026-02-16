import os, discord, random, threading, http.server, socketserver
from discord.ext import commands

# --- SERVEUR ANTI-DODO ---
def run_server():
    port = int(os.environ.get("PORT", 8080))
    with socketserver.TCPServer(("", port), http.server.SimpleHTTPRequestHandler) as httpd:
        httpd.serve_forever()
threading.Thread(target=run_server, daemon=True).start()

# --- BOT CONFIG ---
intents = discord.Intents.all() # On met TOUT pour être tranquille
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'✅ ZASTX EST EN LIGNE !')

@bot.command()
async def ping(ctx):
    await ctx.send('Pong ! 🏓')

@bot.command(name="8ball")
async def eight_ball(ctx, *, question):
    reponses = ["Oui", "Non", "Peut-être", "C'est certain !", "Jamais."]
    await ctx.send(f"🎱 {random.choice(reponses)}")

# --- LANCEMENT (LA LIGNE CRITIQUE) ---
token = os.environ.get("DISCORD_TOKEN")
bot.run(token)
