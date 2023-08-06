import shutil
from typing import Text

import requests


class Tts:
    def __init__(self, region: Text, text: Text, voice: Text):
        self.region = region
        self.text = text
        self.voice = voice

    def convert(self, file_name: Text):
        local_filename = file_name
        with requests.post("http://137.184.57.49:8000/convert", json={"region": self.region,
                                                                      "text": self.text, "voice": self.voice},
                           stream=True) as r:
            with open(local_filename, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
        return local_filename
