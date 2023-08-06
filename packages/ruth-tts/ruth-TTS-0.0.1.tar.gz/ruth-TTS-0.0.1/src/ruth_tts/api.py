import shutil

import requests


class Tts:
    def __init__(self, region, text, voice):
        self.region = region
        self.text = text
        self.voice = voice

    def convert(self):
        local_filename = "download.wav"
        with requests.post("http://137.184.57.49:8000/convert", json={"region": self.region,
                                                                      "text": self.text, "voice": self.voice},
                           stream=True) as r:
            with open(local_filename, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
        return local_filename


a = Tts("eastus", "what", "gabby")
a.convert()
