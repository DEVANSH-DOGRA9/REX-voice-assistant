import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
import pygame
import os
import subprocess  # Import the subprocess module for opening Notepad and Meld
from gtts import gTTS

newsapi = "6c6f2bef4096476fa07128c27cfdaaac"

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

# Global variable to keep track of the current YouTube video
current_youtube_url = None

def processCommand(c):
    global current_youtube_url
    try:
        c = c.lower()
        print(f"Processing command: {c}")  # Debugging line

        if "open google" in c:
            webbrowser.open("https://google.com")
            speak_old("Opening Google.")
        elif "open facebook" in c:
            webbrowser.open("https://facebook.com")
            speak_old("Opening Facebook.")
        elif "open youtube" in c:
            webbrowser.open("https://youtube.com")
            speak_old("Opening YouTube.")
        elif "open linkedin" in c:
            webbrowser.open("https://linkedin.com")
            speak_old("Opening LinkedIn.")
        elif c.startswith("play"):
            song = c[len("play "):].strip()  # Improved handling of song name
            link = musicLibrary.music.get(song)
            if link:
                webbrowser.open(link)  # Open the YouTube video in the browser
                speak_old(f"Playing {song}.")
                current_youtube_url = link  # Track the URL
            else:
                speak_old(f"Sorry, I couldn't find the song {song}.")
        elif c.lower() == "stop":
            if current_youtube_url:
                # For YouTube links, you can't directly stop playback through code.
                # Optionally, you can inform the user.
                speak_old("Stopping playback is not supported for YouTube links.")
                current_youtube_url = None
            else:
                # Don't say an error if nothing is playing
                pass
        elif "news" in c:
            try:
                r = requests.get(f"https://newsapi.org/v2/everything?q=tesla&from=2024-08-15&sortBy=publishedAt&apiKey={newsapi}")
                print(f"API Response Status Code: {r.status_code}")  # Debugging line
                if r.status_code == 200:
                    data = r.json()
                    print(f"API Response Data: {data}")  # Debugging line
                    articles = data.get('articles', [])
                    if articles:
                        for article in articles:
                            speak_old(article['title'])
                    else:
                        speak_old("No news articles found.")
                else:
                    speak_old("Sorry, I couldn't fetch the news.")
            except Exception as e:
                print(f"News fetch error: {e}")  # Debugging line
                speak_old(f"Error fetching news: {str(e)}")
        elif "open notepad" in c:
            try:
                subprocess.Popen(["notepad.exe"])  # Open Notepad
                speak_old("Opening Notepad.")
            except Exception as e:
                speak_old(f"Error opening Notepad: {str(e)}")
        elif "open meld" in c:
            try:
                subprocess.Popen(["meld"])  # Open Meld
                speak_old("Opening Meld.")
            except Exception as e:
                speak_old(f"Error opening Meld: {str(e)}")
        else:
            # Only speak an error message if the command is not recognized
            speak_old("Sorry, I didn't understand that command.")
        
    except Exception as e:
        print(f"Error processing command: {str(e)}")
        speak_old(f"Error processing command: {str(e)}")

if __name__ == "__main__":
    speak_old("Initializing Rex....")
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for wake phrase...")
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=3)
            phrase = recognizer.recognize_google(audio)
            print(f"Recognized phrase: {phrase}")  # Debugging line

            # Check if the phrase contains "Rex"
            if "rex" in phrase.lower():
                speak_old("Yes?")
                while True:
                    try:
                        with sr.Microphone() as source:
                            print("Listening for command...")
                            audio = recognizer.listen(source, timeout=3, phrase_time_limit=3)
                        command = recognizer.recognize_google(audio)
                        print(f"Command recognized: {command}")  # Debugging line
                        processCommand(command)
                    except sr.UnknownValueError:
                        # Handle unknown value errors silently
                        pass
                    except sr.RequestError as e:
                        print(f"API request error: {e}")
                        speak_old(f"API request error: {str(e)}")
                    except Exception as e:
                        print(f"Error: {e}")
                        speak_old(f"Error: {e}")
        except sr.UnknownValueError:
            # Handle unknown value errors silently
            pass
        except sr.RequestError as e:
            print(f"API request error: {e}")
            speak_old(f"API request error: {str(e)}")
        except Exception as e:
            print(f"Error: {e}")
            speak_old(f"Error: {e}")
