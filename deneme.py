import discord
from discord.ext import commands
import random
import math

# --- Müzik için ek import ---
import asyncio
from yt_dlp import YoutubeDL
from discord import FFmpegPCMAudio

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} olarak giriş yaptık')

# ------------------ Basit Metin Komutları ------------------

@bot.command()
async def merhaba(ctx):
    await ctx.send('Selam')

@bot.command()
async def heh(ctx, count_heh: int = 5):
    await ctx.send("he" * count_heh)

@bot.command()
async def isimyazdir(ctx, *, isim: str):
    await ctx.send(isim)

# ------------------ Matematik Komutları ------------------

@bot.command(help="Üç sayıyı toplar. Kullanım: !topla 1 2 3")
async def topla(ctx, a: float, b: float, c: float):
    sonuc = a + b + c
    await ctx.send(f"Toplam: {sonuc}")

@bot.command(help="Çarpma. Kullanım: !carp 2 3")
async def carp(ctx, a: float, b: float):
    await ctx.send(f"Çarpım: {a * b}")

@bot.command(help="Bölme. Kullanım: !bol 10 2")
async def bol(ctx, a: float, b: float):
    if b == 0:
        await ctx.send("Hata: 0'a bölme yapılamaz.")
        return
    await ctx.send(f"Bölüm: {a / b}")

@bot.command(name="karekok", help="Karekök. Kullanım: !karekok 9")
async def kare_kok(ctx, x: float):
    if x < 0:
        await ctx.send("Hata: Negatif sayının gerçek karekökü yok.")
        return
    await ctx.send(f"√{x} = {math.sqrt(x)}")

@bot.command(name="us", help="Üslü sayı. Kullanım: !us 2 10")
async def us_al(ctx, taban: float, us: float):
    try:
        sonuc = taban ** us
    except OverflowError:
        await ctx.send("Hata: Sonuç çok büyük (overflow).")
        return

    if sonuc > 0:
        durum = "pozitif"
    elif sonuc < 0:
        durum = "negatif"
    else:
        durum = "sıfır"

    await ctx.send(f"{taban}^{us} = {sonuc} ({durum})")

# ------------------ Zar Komutu ------------------

@bot.command(name="zar", help="Zar atar. Kullanım: !zar [yuz] [adet]")
async def zar_at(ctx, yuz: int = 6, adet: int = 1):
    if yuz < 2 or adet < 1 or adet > 20:
        await ctx.send("Lütfen geçerli değerler girin. (yüz≥2, 1≤adet≤20)")
        return
    atislar = [random.randint(1, yuz) for _ in range(adet)]
    await ctx.send(f"{adet}x d{yuz} → {atislar} | Toplam: {sum(atislar)}")

# ------------------ Oyun Önerileri ------------------

OYUN_KATEGORILERI = {
    "fps": ["Counter-Strike 2", "Valorant", "Apex Legends", "Overwatch 2", "Call of Duty: Warzone"],
    "moba": ["League of Legends", "Dota 2", "Smite"],
    "battle_royale": ["Fortnite", "PUBG: Battlegrounds", "Warzone"],
    "spor": ["EA Sports FC 25", "NBA 2K", "Rocket League"],
    "rpg": ["Elden Ring", "The Witcher 3", "Cyberpunk 2077", "Baldur’s Gate 3"],
    "survivor": ["Minecraft", "Rust", "ARK: Survival Ascended", "Valheim"],
    "strateji": ["Age of Empires IV", "Civilization VI", "Total War: Warhammer III"],
    "yarış": ["Forza Horizon 5", "Gran Turismo 7", "F1 24"]
}

@bot.command(name="oyunoner", help="Popüler oyun önerir. Kullanım: !oyunoner [kategori]")
async def oyun_oner(ctx, kategori: str = None):
    if kategori is None:
        kategoriler = ", ".join(sorted(OYUN_KATEGORILERI.keys()))
        await ctx.send(f"Bir kategori seç: {kategoriler}\nÖrnek: `!oyunoner fps`")
        return

    kategori = kategori.lower()
    if kategori not in OYUN_KATEGORILERI:
        await ctx.send("Böyle bir kategori yok. `!oyunoner` yazarak listeyi görebilirsin.")
        return

    oyunlar = OYUN_KATEGORILERI[kategori][:5]
    await ctx.send(f"**{kategori.title()}** için öneriler: " + ", ".join(oyunlar))

# ------------------ Müzik (YouTube) ------------------

YDL_OPTS = {
    "format": "bestaudio/best",
    "quiet": True,
    "noplaylist": True,
    "extract_flat": False
}

FFMPEG_OPTS = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn"
}


# ------------------ BOTU BAŞLAT ------------------

bot.run("")
