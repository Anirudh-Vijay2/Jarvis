# Required Libraries
# Made with love in india 
# Created by Anirudh Vijay 
import pyttsx3
import speech_recognition as sr
import datetime
import random
import wikipedia
import requests
import openai
import subprocess
from datetime import datetime, date
from playsound import playsound
import webbrowser
import time
import os
import sys

def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Please Do Not Copy My Code
url = "https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey=YOUR_KEY" # News API
openai.api_key="YOUR_API_KEY" # Open AI ApiKey
# Initializing Pyttsx3

engine = pyttsx3.init('sapi5')
engine.setProperty('rate', 190)

# Checking For Available Voices
# Mainly Checking For Brian Voice

voices = engine.getProperty('voices')
AvailableVoices = []
print("Available Voices Are: ")
for voic in voices:
    print(voic.name)
    AvailableVoices.append(voic.name)
print("\n")
if "IVONA 2 Brian - British English male voice [22kHz]" in AvailableVoices:
    print("Brian Voice Available")
    index = AvailableVoices.index("IVONA 2 Brian - British English male voice [22kHz]")
    print(index)
    # When Found Brian Voice
else:
    print("Brian Voice Not Available")
    print(f"Since Brian Voice Is Not Available Jarvis Will Use {AvailableVoices[0]} As Voice")
    print("Contact Anirudh Vijay To Download Brian Voice...!")
    # When Cant Find Brian Voice 
    index = 0
engine.setProperty('voice', voices[index].id)

def speakJarvis(audio):
    # Speaking Function 
    # Important For Speaking
    engine.say(audio)
    engine.runAndWait()
    
completion=openai.Completion() # Initialising Open AI

def takeCommand():
    # Taking Command From The User Through The Microphone
    # Very Important For The Working Of Jarvis
    global query
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 2
        audio = r.listen(source)
    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in') 
        print(f"User said: {query}\n") 
    except Exception as e:
        # speakJarvis("Say that again please")
        print("Say that again please...") 
        return "None" #None string will be returned
    return query

status = True # This is the default status of Jarvis 'False' means that Jarvis is currently OFF

def setTimerJarvis():
    # Timer Fuction Used By Jarvis To Set Timer
    query=""
    speakJarvis("For how many seconds do you want me to set timer?")
    query = takeCommand().lower()
    number = []
    IntQ = int(query)
    for i in range(IntQ):
        number.append(i)
    for n in number[::-1]:
        speakJarvis(n)
        time.sleep(1)
    speakJarvis("30 seconds completed ")
    
def newsReader():
    # News Reading Function Used To Read News To The User
    speakJarvis("Reading top headlines by times of India")
    news = requests.get(url).json()
    for x in range(0, 5):
        Heading = news['articles'][x]["title"]
        speakJarvis(Heading)
        
def Reply(question):
    # Replying To User Using The Open AI tool
    prompt=f'User: {question}\n Jarvis_Power_By_openai: '
    response=completion.create(prompt=prompt, engine="text-davinci-002", max_tokens=200)
    answer=response.choices[0].text.strip()
    return answer

while status != True:
    # Changing The Status Of Jarvis 
    # Status Will Change When You Say "wake up jarvis" or "wake up"
    query = takeCommand().lower()
    if "wake up" in query:
            p = subprocess.Popen("python .\\ext\\interface.py", stdout=subprocess.PIPE, shell=True) # This Will Turn On The Graphical User Interface (GUI) Of Javis
            playsound("C:\\Program Files (x86)\\Jarvis\\audio\\jarvis1.wav")
            speakJarvis("Initializing system")
            playsound("C:\\Program Files (x86)\\Jarvis\\audio\\jarvis2.wav")
            status = True
if status == True:
    # Checking Whether Status Is 'True' Or Not
    # Jarvis Will Start Working When The Status Is True
    while True:
        # Main Loop
        query = takeCommand().lower()
        if "shutdown jarvis" in query:
            # Command For Shutting Down Jarvis
            speakJarvis("Preparing to power down and run diagnostics")
            speakJarvis("Shutting systems down")
            p.kill()
            break
        elif "who is" in query or "wikipedia" in query:
            # Searching In wikipedia
            if "who is" in query:
                query = query.replace("who is", "")
            if "wikipedia" in query:
                query = query.replace("wikipedia", "")
            result = wikipedia.summary(query, sentences=2)
            speakJarvis(f"According to wikipedia {result}")
        elif  "random number" in query and "between" not in query:
            speakJarvis(random.randint(1, 100))
        elif "current time" in query:
            ctime = datetime.now()
            ctimex1 = ctime.strftime("%H:%M:%S")
            speakJarvis(f"The current time is {ctimex1}")
        elif "date" in query:
            today = date.today()
            FinalDate = today.strftime("%b-%d-%Y")
            speakJarvis(FinalDate)
        elif "open youtube" in query:
            speakJarvis("Opening youtube")
            webbrowser.open("www.youtube.com")
        elif "open google" in query:
            speakJarvis("Opening google")
            webbrowser.open("www.google.com")
        elif "set timer" in query:
            setTimerJarvis()     
        elif "read top news headlines" in query or "read news" in query:
            newsReader()
        elif "what is your name" in query:
            speakJarvis("My name is Jarvis")
        elif "who made you" in query:
            speakJarvis("Anirudh Vijay made me")
        elif "play song" in query or "play music" in query:
            speakJarvis("Playing Song From Youtube")
            webbrowser.open("https://www.youtube.com/watch?v=unQlCp-lL6I&list=PLXtmyk_oFEJjlPu6d-XImEoBwjdBLiop2")
        elif "bgm" in query:
            speakJarvis("Playing a random BGM")
            musicFolder = 'C:\\Program Files (x86)\\Jarvis\\bgm'
            songs = os.listdir(musicFolder)
            randMusic = random.choice(songs)
            print(f"Playing {randMusic}")
            os.startfile(os.path.join(musicFolder, randMusic))
        else:
            print(len(query))
            print(query)
            if len(query)>1 and query != "none":
                ans = Reply(query)
                print(ans)
                # speakJarvis(ans)
                speakJarvis("Sorry A.P.I expired")
            else:
                print("Nothing")
        