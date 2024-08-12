from gtts import gTTS
import os
import webbrowser
import speech_recognition as sr
import musiclibrary
import requests

recognizer = sr.Recognizer()
newsapi = "1bb5b87adbb64c5ca9963445030285ee"

def speak(text):
    tts = gTTS(text=text, lang='en')
    tts.save("temp.mp3")
    os.system("afplay temp.mp3")  # Use afplay for macOS; change if using a different OS
    os.remove("temp.mp3")  # Remove the file after playing it

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif "open github" in c.lower():
        webbrowser.open("https://github.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musiclibrary.music.get(song)
        
        if link:
            webbrowser.open(link)
        else:
            speak("Sorry, I couldn't find that song.")
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
        if r.status_code == 200:
            # Parse the JSON response
            data = r.json()

            # Extract the articles
            articles = data.get("articles", [])

            # Speak out the top headlines
            for article in articles:
                speak(article['title'])
        else:
            speak("Sorry, I couldn't fetch the news.")
    else:
        speak("Sorry, I didn't understand that command.")

if __name__ == "__main__":
    speak("Initializing Eva")

    # List available microphones (optional, for debugging)
    mic_list = sr.Microphone.list_microphone_names()
    print("Available microphones:", mic_list)

    # Create a loop to continuously listen to the microphone
    while True:
        print("Recognizing...")
        try:
            # Use the correct microphone index (default is 0)
            with sr.Microphone(device_index=0) as source:  
                recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjust for ambient noise
                print("Listening!")
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=15)  # Adjust timeout and phrase_time_limit as needed
                word = recognizer.recognize_google(audio)
               
                if word.lower() == "eva":
                    speak("Yes, how can I help you?")
                    print("Eva active..")
                    
                    # Listen for command without reopening the microphone
                    audio = recognizer.listen(source)
                    command = recognizer.recognize_google(audio)

                    processCommand(command)

        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Google Speech Recognition error; {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
