import speech_recognition as sr
from apscheduler.schedulers.background import BackgroundScheduler
from bs4 import BeautifulSoup
import requests
import time
from gtts import gTTS
import os 

def speak(text):
    tts = gTTS(text=text, lang='en', slow=False)
    tts.save("temp.mp3")
    os.system("mpg123 temp.mp3")

# Function to convert text to speech using pyttsx3 library
#def speak(text):
    #engine = pyttsx3.init()
    #engine.say(text)
    #engine.runAndWait()

# Function to capture audio input using the microphone and convert it to text
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio)
        print(f"You said: {command}")
    except sr.UnknownValueError:
        print("Sorry, I didn't understand that.")
        command = ""
    return command

# Function to set a reminder using the BackgroundScheduler from apscheduler
def set_reminder(task, delay):
    scheduler = BackgroundScheduler()
    scheduler.add_job(speak, "interval", seconds=delay, args=[f"It's time to {task}!"])
    scheduler.start()

# Function to search the web using Google search and parse the results using BeautifulSoup
def search_web(query):
    url = f"https://www.google.com/search?q={query}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.3"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    results = soup.find_all("div", class_="tF2Cxc")
    for result in results[:5]:
        title = result.find("h3").text
        link = result.find("a")["href"]
        speak(f"{title}: {link}")

# Main function
if __name__ == "__main__":
    # Greet the user
    speak("Hello, I am your voice assistant. What can I do for you?")

    # Main loop to listen for voice commands and execute appropriate functions
    while True:
        command = listen().lower()

        # Set a reminder
        if "set reminder" in command:
            task = input("What's the task? ")
            delay = int(input("In how many seconds should I remind you? "))
            set_reminder(task, delay)
            speak(f"Reminder set for {task} in {delay} seconds.")

        # Search the web
        elif "search the web" in command:
            query = input("What do you want to search for? ")
            search_web(query)

        # Exit the program
        elif "exit" in command:
            speak("Goodbye!")
            break
