# speech to text ( transcription) 


import speech_recognition as sr

r = sr.Recognizer()

audio = '/Users/shradhitsubudhi/Documents/veritonic/0a1febb3be74b7e892e141352c51440d1e04752259590c8e145fb926.wav'

with sr.AudioFile(audio) as source:
    audio = r.record(source)
    print ('Done!')

try:
    text = r.recognize_google(audio)
    print (text)

except Exception as e:
    print (e)
