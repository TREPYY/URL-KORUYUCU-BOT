import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Sunucuların özel URL'lerini kaydediyoruz
guild_vanity_cache = {}

@bot.event
async def on_ready():
    print(f"✅ Bot aktif: {bot.user}")
    for guild in bot.guilds:
        try:
            vanity = await guild.vanity_invite()
            if vanity:
                guild_vanity_cache[guild.id] = vanity.code
                print(f"{guild.name} URL: discord.gg/{vanity.code}")
        except:
            pass

@bot.event
async def on_guild_update(before, after):
    try:
        old_vanity = await before.vanity_invite()
        new_vanity = await after.vanity_invite()
    except:
        return

    if not old_vanity or not new_vanity:
        return

    if old_vanity.code != new_vanity.code:
        logs = [log async for log in after.audit_logs(limit=1, action=discord.AuditLogAction.guild_update)]
        changer = logs[0].user if logs else None

        if changer and changer.id != after.owner_id:
            try:
                await after.edit(vanity_code=old_vanity.code)
                print(f"🔒 URL geri alındı: discord.gg/{old_vanity.code}")

                # Log kanalı bul veya oluştur
                log_channel = discord.utils.get(after.text_channels, name="url-koruma-log")
                if not log_channel:
                    log_channel = await after.create_text_channel("url-koruma-log")

                await log_channel.send(
                    f"⚠️ {changer.mention} özel URL'yi değiştirmeye çalıştı! "
                    f"Eski URL geri yüklendi: **discord.gg/{old_vanity.code}**"
                )
            except Exception as e:
                print("URL geri alınamadı:", e)

bot.run("buraya bot tokenini ya")
