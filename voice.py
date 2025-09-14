# assistant.py
import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import time
import subprocess
from ecapture import ecapture as ec
import wolframalpha
import requests
import shutil

# ------------------- Initialization -------------------
print('Loading your AI personal assistant - G-One')

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Corrected voice setup

# ------------------- Speak Function -------------------
def speak(text):
    engine.say(text)
    engine.runAndWait()

# ------------------- Greetings -------------------
def wishMe():
    hour = datetime.datetime.now().hour
    if hour >= 0 and hour < 12:
        speak("Hello, Good Morning")
        print("Hello, Good Morning")
    elif hour >= 12 and hour < 18:
        speak("Hello, Good Afternoon")
        print("Hello, Good Afternoon")
    else:
        speak("Hello, Good Evening")
        print("Hello, Good Evening")

# ------------------- Take User Command -------------------
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")
        audio = r.listen(source)
        try:
            statement = r.recognize_google(audio, language='en-in')
            print(f"User said: {statement}\n")
        except Exception:
            speak("Pardon me, please say that again")
            return None
        return statement

# ------------------- Main -------------------
if __name__ == '__main__':
    speak("Loading your AI personal assistant G-One")
    wishMe()

    while True:
        speak("Tell me how can I help you now?")
        statement = takeCommand()
        if statement is None:
            continue
        statement = statement.lower()

        if "good bye" in statement or "ok bye" in statement or "stop" in statement:
            speak('Your personal assistant G-One is shutting down, Goodbye')
            print('Your personal assistant G-One is shutting down, Goodbye')
            break

        # Wikipedia search
        elif 'wikipedia' in statement:
            speak('Searching Wikipedia...')
            statement = statement.replace("wikipedia", "")
            try:
                results = wikipedia.summary(statement, sentences=3)
                speak("According to Wikipedia")
                print(results)
                speak(results)
            except Exception:
                speak("Sorry, I could not find anything on Wikipedia.")

        # YouTube search
        elif 'open youtube' in statement:
            speak("Tell search query")
            query = takeCommand()
            if query:
                webbrowser.open_new_tab(f"https://www.youtube.com/results?search_query={query}")
                speak("YouTube is open now")
                time.sleep(5)

        # Open Google
        elif 'open google' in statement:
            webbrowser.open_new_tab("https://www.google.com")
            speak("Google Chrome is open now")
            time.sleep(5)

        # Open Gmail
        elif 'open gmail' in statement:
            webbrowser.open_new_tab("https://mail.google.com")
            speak("Google Mail is open now")
            time.sleep(5)

        # Weather info
        elif "weather" in statement:
            api_key = "YOUR_OPENWEATHERMAP_API_KEY"  # Replace with your key
            base_url = "https://api.openweathermap.org/data/2.5/weather?"
            speak("What's the city name?")
            city_name = takeCommand()
            if city_name:
                complete_url = base_url + "appid=" + api_key + "&q=" + city_name
                response = requests.get(complete_url)
                x = response.json()
                if x.get("cod") != "404":
                    y = x["main"]
                    current_temperature = y["temp"]
                    current_humidity = y["humidity"]
                    z = x["weather"]
                    weather_description = z[0]["description"]
                    speak(f"Temperature in Kelvin is {current_temperature}, "
                          f"humidity is {current_humidity} percent, "
                          f"description: {weather_description}")
                    print(f"Temperature = {current_temperature} K\nHumidity = {current_humidity}%\nDescription = {weather_description}")
                else:
                    speak("City not found.")

        # Tell time
        elif 'time' in statement:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")
            print(strTime)

        # About assistant
        elif 'who are you' in statement or 'what can you do' in statement:
            speak('I am G-One version 1.0, your personal assistant. I can open YouTube, Google, Gmail, take photos, search Wikipedia, check weather, provide news headlines, '
                  'and answer computational or geographical questions.')

        # Creator info
        elif "who made you" in statement or "who created you" in statement:
            speak("I was built by Purna and Chandrala Indrani")
            print("I was built by Purna and Chandrala Indrani")

        # Open StackOverflow
        elif "open stackoverflow" in statement:
            webbrowser.open_new_tab("https://stackoverflow.com/login")
            speak("Here is StackOverflow")

        # News headlines
        elif 'news' in statement:
            webbrowser.open_new_tab("https://timesofindia.indiatimes.com/home/headlines")
            speak('Here are some headlines from the Times of India. Happy reading!')
            time.sleep(6)

        # Take photo
        elif "camera" in statement or "take a photo" in statement:
            try:
                ec.capture(0, "G-One Camera", "img.jpg")
            except Exception:
                speak("Camera not accessible.")

        # Open custom search
        elif 'search' in statement:
            statement = statement.replace("search", "")
            webbrowser.open_new_tab(statement)
            time.sleep(5)

        # Ask computational/geographical questions
        elif 'ask' in statement:
            speak('I can answer computational or geographical questions. What do you want to ask?')
            question = takeCommand()
            if question:
                try:
                    app_id = "YOUR_WOLFRAMALPHA_APP_ID"  # Replace with your key
                    client = wolframalpha.Client(app_id)
                    res = client.query(question)
                    answer = next(res.results).text
                    speak(answer)
                    print(answer)
                except Exception:
                    speak("Sorry, I could not compute the answer.")

        # Log off PC
        elif "log off" in statement or "sign out" in statement:
            speak("Ok, your PC will log off in 10 seconds. Make sure you exit from all applications.")
            time.sleep(10)
            subprocess.call(["shutdown", "/l"])
