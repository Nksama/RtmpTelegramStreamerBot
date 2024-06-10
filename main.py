from pyrogram import Client , filters
import os
import config
import subprocess

bot = Client(
    "rtmpstreamer" ,
    api_id=6,
    api_hash="eb06d4abfb49dc3eeb1aeb98ae0f581e",
    bot_token=config.BOT_TOKEN
    )

outputurl = config.RTMP_URL + config.RTMP_KEY
ffmpeg_process = None

@bot.on_message(filters.command("start"))
def hello(_, m):
    m.reply("Hello there")

@bot.on_message(filters.command("play"))
def play(_, m):
    global ffmpeg_process
    m.reply("Downloading......")
    x = m.reply_to_message.download()
    m.reply("Playing....")
    if ffmpeg_process:
        ffmpeg_process.terminate()
    ffmpeg_command = [
        "ffmpeg", "-re", "-i", x,
        "-c:v", "libx264", "-preset", "fast", "-b:v", "1500k", "-maxrate", "1500k", "-bufsize", "3000k",
        "-pix_fmt", "yuv420p", "-g", "25", "-keyint_min", "25",
        "-c:a", "aac", "-b:a", "96k", "-ac", "2", "-ar", "44100",
        "-f", "flv", outputurl
    ]

    ffmpeg_process = subprocess.Popen(ffmpeg_command)


@bot.on_message(filters.command("uplay"))
def uplay(_, m):
    global ffmpeg_process
    url = m.text.replace("/uplay " , "")
    m.reply("Playing....")
    if ffmpeg_process:
        ffmpeg_process.terminate()
    ffmpeg_command = [
        "ffmpeg", "-re", "-i", url,
        "-c:v", "libx264", "-preset", "fast", "-b:v", "1500k", "-maxrate", "1500k", "-bufsize", "3000k",
        "-pix_fmt", "yuv420p", "-g", "25", "-keyint_min", "25",
        "-c:a", "aac", "-b:a", "96k", "-ac", "2", "-ar", "44100",
        "-f", "flv", outputurl
    ]

    ffmpeg_process = subprocess.Popen(ffmpeg_command)

@bot.on_message(filters.command("stop"))
def stop(_, m):
    global ffmpeg_process
    if ffmpeg_process:
        ffmpeg_process.terminate()
        ffmpeg_process = None
        m.reply("Stopped streaming.")
    else:
        m.reply("No active playback to stop.")


bot.run()
