from pyrogram import Client , filters
import os
import config
import subprocess
import yt_dlp


bot = Client(
    "rtmpstreamer" ,
    api_id=6,
    api_hash="eb06d4abfb49dc3eeb1aeb98ae0f581e",
    bot_token=config.BOT_TOKEN
    )

outputurl = config.RTMP_URL + config.RTMP_KEY
ffmpeg_process = None


ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '320',
    }],
    'outtmpl': '%(title)s.%(ext)s',
}


def download_video(video_url):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url)
        
        ydl.download([info['webpage_url']])
        filename = ydl.prepare_filename(info)

      # Print the filename
    try:
        return filename.replace("webm" , "mp3")
    except Exception as e:
        return filename
    


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
    ffmpeg_process.wait()
    os.remove(x) 


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
    ffmpeg_process.wait()
    os.remove(x) 

@bot.on_message(filters.command("stop"))
def stop(_, m):
    global ffmpeg_process
    if ffmpeg_process:
        ffmpeg_process.terminate()
        ffmpeg_process = None
        m.reply("Stopped streaming.")
    else:
        m.reply("No active playback to stop.")


@bot.on_message(filters.command("ytplay"))
def ytplay(_,m):
    global ffmpeg_process
    url = m.text.replace("/ytplay " , "")
    m.reply("DOWNLOADING.....")
    x = download_video(url)
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
    ffmpeg_process.wait()
    os.remove(x) 
    





bot.run()
