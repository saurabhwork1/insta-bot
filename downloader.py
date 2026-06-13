import yt_dlp
import uuid
import os
import asyncio

from config import DOWNLOAD


async def download(url, type, progress_callback=None):

    name=str(uuid.uuid4())

    path=f"{DOWNLOAD}/{name}"


    def hook(d):

        if d['status']=="downloading":

            total=d.get('total_bytes') or d.get('total_bytes_estimate')

            if total:

                done=d.get('downloaded_bytes',0)

                percent=int(done*100/total)

                if progress_callback:
                    asyncio.run_coroutine_threadsafe(
                        progress_callback(percent),
                        asyncio.get_event_loop()
                    )


    if type=="video":

        options={

        # highest quality
        "format":
        "bestvideo+bestaudio/best",

        "merge_output_format":
        "mp4",

        "outtmpl":
        path+".%(ext)s",

        "progress_hooks":
        [hook],

        "retries":10,

        "fragment_retries":10,

        "quiet":True

        }


    else:

        options={

        "format":
        "bestaudio",

        "outtmpl":
        path+".%(ext)s",

        "postprocessors":
        [
        {
        "key":
        "FFmpegExtractAudio",

        "preferredcodec":
        "mp3",

        "preferredquality":
        "320"
        }
        ],

        "progress_hooks":
        [hook],

        "retries":10,

        "quiet":True

        }



    with yt_dlp.YoutubeDL(options) as ydl:

        ydl.download([url])



    for file in os.listdir(DOWNLOAD):

        if name in file:

            return DOWNLOAD+"/"+file