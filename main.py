from pyrogram import Client , filters
import os
import config

bot = Client(
    "rtmpstreamer" ,
    api_id=6,
    api_hash="eb06d4abfb49dc3eeb1aeb98ae0f581e",
    bot_token=config.BOT_TOKEN
    )

outputurl = config.RTMP_URL + config.RTMP_KEY

@bot.on_message(filters.command("start"))
def hello(_ , m):
    m.reply("Hello there")

@bot.on_message(filters.command("play"))
def play(_,m):
    m.reply("Downloading......")
    x = m.reply_to_message.download()
    m.reply("Playing....")
    os.system(fr"""ffmpeg -re -i '{x}' \
-c:v libx264 -preset fast -b:v 1500k -maxrate 1500k -bufsize 3000k \
-pix_fmt yuv420p -g 25 -keyint_min 25 \
-c:a aac -b:a 96k -ac 2 -ar 44100 \
-f flv {outputurl}""")


@bot.on_message(filters.command("vplay"))
def play(_,m):
    m.reply("Downloading......")
    x = m.reply_to_message.download()
    m.reply("Playing....")
    os.system(fr"""ffmpeg -re -i '{x}' \
-c:v libx264 -preset fast -b:v 1500k -maxrate 1500k -bufsize 3000k \
-pix_fmt yuv420p -g 25 -keyint_min 25 \
-c:a aac -b:a 96k -ac 2 -ar 44100 \
-f flv {outputurl}
""")

@bot.on_message(filters.command("uplay"))
def uplay(_,m):

    url = m.text.split(" ")[1]
    m.reply("Playing....")

    # Stop the previous FFmpeg process if it's running

    ffmpeg_process = os.system(fr"""ffmpeg -re -i '{url}' \
    -c:v libx264 -preset fast -b:v 1500k -maxrate 1500k -bufsize 3000k \
    -pix_fmt yuv420p -g 25 -keyint_min 25 \
    -c:a aac -b:a 96k -ac 2 -ar 44100 \
    -f flv {outputurl}""")

@bot.on_message(filters.command("vuplay"))
def vuplay(_,m):


    url = m.text.split(" ")[1]
    m.reply("Playing....")


    ffmpeg_process = os.system(fr"""ffmpeg -re -i '{url}' \
    -c:v libx264 -preset fast -b:v 1500k -maxrate 1500k -bufsize 3000k \
    -pix_fmt yuv420p -g 25 -keyint_min 25 \
    -c:a aac -b:a 96k -ac 2 -ar 44100 \
    -f flv {outputurl}""")






bot.run()
