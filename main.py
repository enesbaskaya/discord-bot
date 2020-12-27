import discord
from discord.ext import commands
from discord.utils import get
import youtube_dl
import os

#botun tokken bilgisi
TOKEN = open('token.txt', 'r').read()

#botu tetikleyen etiket
BOT_PREFIX = '!Btg '

#bot üretiriyorum
bot = commands.Bot(command_prefix=BOT_PREFIX)

#komutlarımızı liste içine ekliyoruz
commandList = []
commandFile = open('command.txt', 'r')
commandLines = commandFile.readlines()
for line in commandLines: 
    commandList.append(line.strip())


# botun hazır hala getirilmesi ilk çalışma anı
@bot.event
async def on_ready():
    print(bot.user.name + ' ready to use!')

# botun ses kanalına dahil edilmesi
# @bot.command(pass_context=True, aliases=['j', 'joi'])
# async def join(ctx):
#     global voice
#     channel = ctx.message.author.voice.channel
#     voice = get(bot.voice_clients, guild=ctx.guild)

#     if voice and voice.is_connected():
#         await voice.move_to(channel)
#     else:
#         voice = await channel.connect()
#         print(f'Bot {channel} kanalına bağlandı')

#     await ctx.send(f'{bot.user.name} **{channel}Ses Kanalına**  katıldı!')

#bot komutlarını görmek içim
@bot.command()
async def mycommands(ctx):
    counter = 0
    for i in commandList:
        await ctx.send(str((counter+1)) + ". Command: " + i+", ")
        counter += 1

# botun ses kanalından atılması
@bot.command(pass_context=True, aliases=['l', 'lea'])
async def disconnect(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"{bot.user.name} {channel}left the voice channel!")
        await ctx.send("See you! 👋🏃🏼")
    else:
        print("The bot is not on the voice channel!")
        await ctx.send("The bot is not on the voice channel!")


@bot.command(pass_context=True, aliases=['p', 'pla'])
async def play(ctx, url: str):

    global voice
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f'Bot {channel} kanalına bağlandı')

    await ctx.send(f'{bot.user.name} {channel} joined the voice channel! 😎 ')

    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            print("Removed old song file")
    except PermissionError:
        print("Trying to delete song file, but it's being played")
        await ctx.send("ERROR: Music playing")
        return

    # await ctx.send("Getting everything ready now")

    voice = get(bot.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now\n")
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"Renamed File: {file}\n")
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"),
               after=lambda e: print("Song done!"))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    nname = name.rsplit("-", 2)
    await ctx.send(f"Playing: **{nname[0]} ⏸**")
    print("playing\n")


@bot.command(pass_context=True, aliases=['pa', 'pau'])
async def pause(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_playing():
        print('Music Paused')
        voice.pause()
        await ctx.send('Music Paused! ▶')
    else:
        print('Music not playing failed pause')
        await ctx.send('Music not playing failed pause')


@bot.command(pass_context=True, aliases=['r', 'res'])
async def resume(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_paused():
        print('Resumed Music')
        voice.resume()
        await ctx.send('Resumed Music! 🎬 ')
    else:
        print('Music is not paused')
        ctx.send('Music is not paused!')


@bot.command(pass_context=True, aliases=['s', 'sto'])
async def stop(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_playing():
        print('Music Stopped')
        voice.stop()
        await ctx.send('Music Stopped! ⛔️')
    else:
        print('No music playing failed to stop')
        await ctx.send('No music playing failed to stop')

@bot.command()
async def whatsup(ctx):
    await ctx.send('iyi sen nasılsın')



# botun çalıştırılması
bot.run('NzkxOTgxMzgzMjQ0MzE2Njcz.X-XEJA.ZO2LjHltPzAkgghdid2I9JfVlbQ')
