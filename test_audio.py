from gtts import gTTS

text = "A robot learns emotions and feels happy."

tts = gTTS(text=text, lang="en")

tts.save("test.mp3")

print("Saved test.mp3")