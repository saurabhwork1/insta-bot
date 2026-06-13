import yt_dlp
import uuid
import os

from config import DOWNLOAD


def download(url, type):

    name=str(uuid.uuid4())

    path=f"{DOWNLOAD}/{name}"

    if type=="video":

        options={
        "format":"best",
        "outtmpl":path+".%(ext)s",
        "retries":5,
        "quiet":True
        }

    else:

        options={
        "format":"bestaudio",
        "outtmpl":path+".%(ext)s",
        "postprocessors":[
            {
            "key":"FFmpegExtractAudio",
            "preferredcodec":"mp3",
            "preferredquality":"320"
            }
        ],
        "retries":5,
        "quiet":True
        }


    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([url])


    for file in os.listdir(DOWNLOAD):

        if name in file:
            return DOWNLOAD+"/"+file