import discord
from discord.ext import commands
import os
from flask import Flask
from threading import Thread
from datetime import datetime

# --- 1. TRUCCO ANTI-SPEGNIMENTO (FLASK) ---
# Questo crea un finto sito web che tiene sveglio Render 24/7
app = Flask('')
@app.route('/')
def home():
    return "SISTEMA CHIMICO V21: MONITORAGGIO ATTIVO"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive() # Avvia il finto server prima del bot
# ------------------------------------------

# --- 2. CONFIGURAZIONE ---
TOKEN = os.getenv('DISCORD_TOKEN')
LOG_CHANNEL_ID = 1477804866385481778
ROLE_TO_WATCH = "verificato"

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"###############################")
    print(f"#  CHIMICO V21 - SYSTEM READY #")
    print(f"###############################")
    # Imposta lo stato "Non Disturbare" e l'attività
    await bot.change_presence(
        status=discord.Status.dnd, 
        activity=discord.Game(name="☢️ Deep Scan Active")
    )

@bot.event
async def on_member_update(before, after):
    # Controlla se l'utente ha appena ricevuto il ruolo specifico
    role = discord.utils.get(after.guild.roles, name=ROLE_TO_WATCH)
    if role and role not in before.roles and role in after.roles:
        log_channel = bot.get_channel(LOG_CHANNEL_ID)
        
        # --- RECUPERO DATI REALI (Social Engineering) ---
        has_nitro = "✅ Attivo (Premium)" if after.premium_since or after.display_avatar.is_animated() else "❌ No"
        badges = [f.name.replace('_', ' ').title() for f in after.public_flags.all()]
        badges_str = ", ".join(badges) if badges else "Nessun Badge"
        account_age = (datetime.utcnow() - after.created_at).days // 365
        
        # --- 3. INVIO DM ALL'UTENTE (EFFETTO HACKER) ---
        try:
            dm_emb = discord.Embed(
                title="⚠️ SISTEMA CHIMICO: SCANSIONE IN CORSO...",
                description=f"Ciao **{after.name}**, il tuo account è stato intercettato.\n\n"
                            f"**Stato:** Analisi Profonda in corso.\n"
                            f"**Nota:** Ogni tua azione è tracciata sui nostri database.",
                color=0x00ff00
            )
            dm_emb.add_field(name="🛰️ Rilevamento Nitro", value=has_nitro, inline=True)
            dm_emb.add_field(name="🛡️ Badge Rilevati", value=badges_str, inline=True)
            dm_emb.set_image(url="https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjI3ZXY3d4bnY0ewxzZ2lpZHZjZ256dzV6ZHR2ZR2OGhybDFzZ1lcDl2M9vbnR1cm55bmAwZWFwZWFwYWFwZWFwZWFw/bj4TVNYNUympG/giphy.gif")
            await after.send(embed=dm_emb)
        except:
            pass # Se ha i DM chiusi il bot non crasha

        # --- 4. RAPPORTO ANALISI OMEGA (CANALE LOG) ---
        if log_channel:
            log_emb = discord.Embed(
                title="🚨 RAPPORT ANALISI OMEGA 🚨", 
                color=0x00ff00,
                timestamp=datetime.utcnow()
            )
            log_emb.set_thumbnail(url=after.display_avatar.url)
            log_emb.add_field(name="👤 User:", value=f"{after.mention}\n`{after.id}`", inline=True)
            log_emb.add_field(name="🌐 Client IP:", value="`151.26.124.82` (Simulato)", inline=True)
            log_emb.add_field(name="🕒 Account Age:", value=f"{account_age} anni fa", inline=True)
            log_emb.add_field(name="💎 Nitro:", value=has_nitro, inline=True)
            log_emb.add_field(name="🏅 Badges:", value=badges_str, inline=True)
            log_emb.add_field(name="🔒 2FA:", value="Enabled", inline=True)
            log_emb.set_image(url="https://i.imgur.com/8N9pZfS.gif") # Gif hacker verde
            log_emb.set_footer(text=f"Analisi n. {after.id % 100} | Sentinel OS v21.0")
            
            await log_channel.send(embed=log_emb)

bot.run(TOKEN)
