from gtts import gTTS

def text_to_speech(text, filename="output.mp3"):
    """
    Converts given text to Hindi speech and saves it as an MP3 file.
    """
    tts = gTTS(text=text, lang="hi", slow=False)
    tts.save(filename)
    return filename 
