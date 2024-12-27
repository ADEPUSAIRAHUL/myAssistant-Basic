import speech_recognition as sr
import pyttsx3
import wikipedia
import webbrowser
import os
from pytube import Search
import random
from googlesearch import search
import requests
import datetime
import pyjokes
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from googletrans import Translator
import json

# Initialize the recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()
translator = Translator()

# Function for speaking
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function for listening to commands
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand the audio")
            return ""
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition service")
            return ""

# Function for getting information from Wikipedia
def get_wikipedia_info(query):
    try:
        result = wikipedia.summary(query, sentences=2)
        return result
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Multiple results found. Please specify your query: {e.options}"
    except wikipedia.exceptions.HTTPTimeoutError:
        return "Sorry, I couldn't fetch the information. Please try again later."

# Function for searching YouTube and playing a video
def play_youtube_video(query):
    search = Search(query)
    results = search.results
    if results:
        selected_video = random.choice(results)
        video_url = selected_video.watch_url
        speak(f"Playing {query} on YouTube")
        webbrowser.open(video_url)
    else:
        speak("Sorry, no videos found for that query.")

# Function for performing a Google search
def google_search(query):
    speak(f"Searching for {query} on Google")
    search_results = search(query, num_results=5)
    for result in search_results:
        print(result)
    speak("You can check the results on your screen.")

# Function for getting the current weather
def get_weather(city):
    api_key = "your_api_key"  # Replace with your OpenWeatherMap API key
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "q=" + city + "&appid=" + api_key
    response = requests.get(complete_url)
    data = response.json()
    
    if data["cod"] != "404":
        if "main" in data:
            weather_data = data["main"]
            temp = weather_data["temp"]
            pressure = weather_data["pressure"]
            humidity = weather_data["humidity"]
            weather_description = data["weather"][0]["description"]
            weather_report = f"Temperature: {temp}K\nPressure: {pressure}hPa\nHumidity: {humidity}%\nDescription: {weather_description}"
            return weather_report
        else:
            return "Weather data is currently unavailable."
    else:
        return "City Not Found"

# Function for telling jokes
def tell_joke():
    return pyjokes.get_joke()

# Function for getting news headlines
def get_news():
    api_key = "your_api_key"  # Replace with your news API key
    base_url = "https://newsapi.org/v2/top-headlines?country=in&apiKey=" + api_key
    response = requests.get(base_url)
    news_data = response.json()
    
    if "articles" in news_data:
        articles = news_data["articles"]
        headlines = [article["title"] for article in articles[:5]]
        return headlines
    else:
        return ["Sorry, no news articles are currently available."]

# Function for getting the current date and time
def get_current_time():
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M")
    current_date = now.strftime("%d-%m-%Y")
    return f"Current date is {current_date} and time is {current_time}"

# Function for sending emails
def send_email(to_email, subject, body):
    from_email = "your_email@example.com"  # Replace with your email
    from_password = "your_password"  # Replace with your email password or App Password

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, from_password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        return "Email sent successfully"
    except smtplib.SMTPAuthenticationError:
        return "Failed to authenticate with the email server. Check the email address and password."
    except smtplib.SMTPException as e:
        return f"Failed to send email: {str(e)}"

# Function for translating text
def translate_text(text, dest_language):
    translation = translator.translate(text, dest=dest_language)
    return translation.text

# Function for managing shopping lists
shopping_list = []

def add_to_shopping_list(item):
    shopping_list.append(item)
    return f"Added {item} to your shopping list."

def view_shopping_list():
    if shopping_list:
        return f"Your shopping list: {', '.join(shopping_list)}"
    else:
        return "Your shopping list is empty."

# Main function to run the assistant
def run_assistant():
    speak("Hello, I'm your assistant. How can I help you?")
    
    while True:
        command = listen()
        
        if 'exit' in command or 'quit' in command:
            speak("Goodbye!")
            break
        
        elif 'wikipedia' in command:
            speak("What do you want to know?")
            query = listen()
            info = get_wikipedia_info(query)
            speak(info)
        
        elif 'open youtube and play' in command:
            song = command.split('play')[-1].strip().strip('"')
            play_youtube_video(song)
        
        elif 'open cmd' in command:
            speak("Opening Command Prompt")
            os.system("start cmd")
        
        elif 'search google for' in command:
            query = command.split('for')[-1].strip()
            google_search(query)
        
        elif 'weather in' in command:
            city = command.split('in')[-1].strip()
            weather = get_weather(city)
            speak(weather)
        
        elif 'tell me a joke' in command:
            joke = tell_joke()
            speak(joke)
        
        elif 'news headlines' in command:
            headlines = get_news()
            for headline in headlines:
                speak(headline)
        
        elif 'time' in command:
            current_time = get_current_time()
            speak(current_time)
        
        elif 'send email to' in command:
            speak("What is the subject?")
            subject = listen()
            speak("What is the message?")
            body = listen()
            email_address = command.split('to')[-1].strip()
            email_status = send_email(email_address, subject, body)
            speak(email_status)
        
        elif 'translate' in command:
            speak("What do you want to translate?")
            text = listen()
            speak("Which language?")
            dest_language = listen().lower()
            translation = translate_text(text, dest_language)
            speak(f"The translation is: {translation}")
        
        elif 'add to shopping list' in command:
            item = command.split('list')[-1].strip()
            add_status = add_to_shopping_list(item)
            speak(add_status)
        
        elif 'view shopping list' in command:
            shopping_list_view = view_shopping_list()
            speak(shopping_list_view)
        
        else:
            speak("Sorry, I didn't understand that. Please try again.")

# Start the assistant
if __name__ == "__main__":
    run_assistant()
