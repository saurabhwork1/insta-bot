import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")

DOWNLOAD = "downloads"

if not os.path.exists(DOWNLOAD):
    os.makedirs(DOWNLOAD)