## Ruth - TTS

### To convert the text to speech

```python
from ruth_tts.api import Tts
converter = Tts("eastus", 'How are you doing', "gabby")
converter.convert("file_name.wav")
```