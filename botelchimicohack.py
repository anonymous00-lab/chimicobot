import discord
from discord.ext import commands
import os
from datetime import datetime

# --- CONFIGURAZIONE ---
# Incolla il tuo token tra le virgolette singole qui sotto
TOKEN = os.getenv('DISCORD_TOKEN')
LOG_CHANNEL_ID = 1477804866385481778 
ROLE_TO_WATCH = "verificato"
# ----------------------

os.system('cls' if os.name == 'nt' else 'clear')
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"##################################")
    print(f"#    CHIMICO V21 - SYSTEM READY  #")
    print(f"##################################")
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Game(name="☢️ Deep Scan Active"))

@bot.event
async def on_member_update(before, after):
    # Controlla se l'utente ha appena ricevuto il ruolo specifico
    role = discord.utils.get(after.guild.roles, name=ROLE_TO_WATCH)
    if role and role not in before.roles and role in after.roles:
        log_channel = bot.get_channel(LOG_CHANNEL_ID)
        
        # 1. INVIO MESSAGGIO PRIVATO (DM) ALL'UTENTE
        try:
            dm_emb = discord.Embed(
                title="⚠️ SISTEMA CHIMICO: SCANSIONE AVVIATA",
                description=f"Ciao {after.name}, il tuo account è stato intercettato dai nostri sistemi.\n**Stato:** Sotto Analisi Profonda.\n**Nota:** Ogni tua azione è tracciata.",
                color=0xff0000
            )
            dm_emb.set_image(url="https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExY3d4bnY0eWxnZ2lpZmU3YjNhOG56dzI2Z2Ztd2R2OGhybDFiZWh5dCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/bJ4TVNYNUympPgcpem/giphy.gif")
            await after.send(embed=dm_emb)
        except:
            pass # Se l'utente ha i DM chiusi, il bot non crasha

        # 2. GENERAZIONE LOG NEL CANALE STAFF
        if log_channel:
            # Dati Reali (Nitro e Badge)
            has_nitro = "✅ Attivo (Premium)" if after.premium_since or after.display_avatar.is_animated() else "❌ No"
            badges = [f.name.replace('_', ' ').title() for f in after.public_flags.all()]
            badges_str = ", ".join(badges) if badges else "Nessun Badge"
            
            # Hardware
            devices = []
            if str(after.desktop_status) != "offline": devices.append("PC Windows")
            if str(after.mobile_status) != "offline": devices.append("Smartphone")
            dev_str = " | ".join(devices) if devices else "Invisibile/VPN"

            # Costruzione Embed (Identico a image_5edfe3)
            embed = discord.Embed(title="🚨 RAPPORT ANALISI OMEGA 🚨", color=0x00ff00, timestamp=datetime.utcnow())
            embed.set_thumbnail(url=after.display_avatar.url)
            
            # Riga 1: Identità
            embed.add_field(name="👤 User:", value=f"{after.mention}\n`{after.id}`", inline=True)
            embed.add_field(name="🌐 Client IP:", value="`151.26.124.82`", inline=True)
            embed.add_field(name="🕒 Account Age:", value=f"<t:{int(after.created_at.timestamp())}:R>", inline=True)
            
            # Riga 2: Connessione (Simulata Wind Tre come volevi)
            embed.add_field(name="🇮🇹 IP Info:", value="**Location:** Italy\n**Provider:** WIND TRE S.P.A.", inline=True)
            embed.add_field(name="📡 Connection:", value="**Type:** Residential\n**VPN:** no", inline=True)
            embed.add_field(name="💻 Device Info:", value=f"**OS:** {dev_str}\n**Browser:** Discord App", inline=True)
            
            # Riga 3: Sicurezza e Nitro
            embed.add_field(name="📧 Email Status:", value="Verified ✅", inline=True)
            embed.add_field(name="💎 Nitro:", value=has_nitro, inline=True)
            embed.add_field(name="🎖️ Badges:", value=badges_str, inline=True)
            
            # Riga 4: Bot Score
            embed.add_field(name="🤖 Bot Score: (0)", value="**Status:** 🟢 Safe User", inline=True)
            act = after.activity.name if after.activity else "Riposo"
            embed.add_field(name="🔍 Tracking:", value=f"Attività: `{act}`", inline=True)
            embed.add_field(name="🔐 2FA:", value="Enabled", inline=True)

            # Immagine Finale e Footer
            embed.set_image(url="https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExY3d4bnY0eWxnZ2lpZmU3YjNhOG56dzI2Z2Ztd2R2OGhybDFiZWh5dCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/bJ4TVNYNUympPgcpem/giphy.gif")
            embed.set_footer(text=f"Analisi n. 36 | Sentinel OS v21.0 • {datetime.now().strftime('%H:%M')}")

            await log_channel.send(embed=embed)


bot.run(TOKEN)
