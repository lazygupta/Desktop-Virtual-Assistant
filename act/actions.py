import os
import cv2
import subprocess as sp
from audio.speech import speak, listen
from PIL import ImageGrab
from decouple import config
from act.screenrecord import record_screen, stop_recording
import threading
from aim.vision import describe_image
import webbrowser
import pyperclip
import platform
import psutil
import requests
from datetime import datetime
from googletrans import Translator
from gtts import gTTS
import pyttsx3

programs = {
    'notepad': "notepad.exe",
    'calculator': "C:\\Windows\\System32\\calc.exe",
    'word': "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE",
    'excel': "C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE",
    'powerpoint': "C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.EXE"
}

def open_notepad():
    os.startfile(programs['notepad'])

def open_word():
    sp.Popen(programs['word'])

def open_excel():
    sp.Popen(programs['excel'])

def open_ppt():
    sp.Popen(programs['powerpoint'])

def open_cmd():
    os.system('start cmd')

def open_calculator():
    sp.Popen(programs['calculator'])

def open_camera():
    sp.run('start microsoft.windows.camera:', shell=True)

def open_website():
    speak('Which website would you like to open?')
    url = listen().lower()
    webbrowser.open(url)

def take_screenshot():
    media_dir = config("MEDIA_DIR")
    screenshot_file = config("SCREENSHOT_FILE")
    screenshot = ImageGrab.grab()
    screenshot.save(media_dir + "/" + screenshot_file)
    print("Screenshot saved as: " + screenshot_file)
    speak("Screenshot saved in media folder as " + screenshot_file)

def start_screen_record():
    recording_thread = threading.Thread(target=record_screen)
    recording_thread.start()

def stop_screen_record():
    stop_recording()

def camera_vision():
    media_dir = config("MEDIA_DIR0")
    screenshot_file = config("SCREENSHOT_FILE")
    
    cap = cv2.VideoCapture(0)  # 0 is the default camera index
    # Capture an image if the camera is opened successfully
    if cap.isOpened():
        ret, frame = cap.read()  # Capture one frame
        if ret:
            # Save the captured image to the specified file
            cv2.imwrite(os.path.join(media_dir, screenshot_file), frame)
            print("Image captured and saved.")
            speak("Image captured and saved.")
        else:
            print("Failed to capture image.")
        cap.release()
    else:
        print("Cannot access the camera.")

    

# New Features

def search_files(filename, directory):
    # Ask user for directory if not provided
    # if not directory:
    #     speak("In which directory would you like to search?")
    #     directory = listen().strip()
    
    if not os.path.isdir(directory):
        speak("The directory you specified does not exist. Please try again.")
        return

    result = []
    for root, dirs, files in os.walk(directory):
        if filename in files:
            result.append(os.path.join(root, filename))
    
    if result:
        speak(f"Found {len(result)} results.")
        for file in result:
            print(file)
    else:
        speak("No files found with that name.")

def set_volume(level):
    try:
        from ctypes import cast, POINTER
        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
        
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMasterVolumeLevelScalar(level / 100, None)
        speak(f"Volume set to {level}%")
    except ImportError:
        speak("Volume control is not supported on this system.")

def get_system_info():
    info = platform.uname()
    sys_info = (
        f"System: {info.system}\n"
        f"Node Name: {info.node}\n"
        f"Release: {info.release}\n"
        f"Version: {info.version}\n"
        f"Machine: {info.machine}\n"
        f"Processor: {info.processor}\n"
    )
    print(sys_info)
    speak("System information displayed.")

def read_clipboard():
    content = pyperclip.paste()
    speak("Clipboard content: " + content)
    print("Clipboard content:", content)

def copy_to_clipboard(text):
    pyperclip.copy(text)
    speak("Text copied to clipboard.")

def check_battery():
    battery = psutil.sensors_battery()
    plugged = "Plugged In" if battery.power_plugged else "Not Plugged In"
    percentage = battery.percent
    speak(f"Battery is at {percentage}% and is {plugged}.")

def toggle_wifi(state):
    if state == "on":
        os.system("netsh interface set interface 'Wi-Fi' admin=enabled")
        speak("Wi-Fi turned on.")
    elif state == "off":
        os.system("netsh interface set interface 'Wi-Fi' admin=disabled")
        speak("Wi-Fi turned off.")
    else:
        speak("Invalid command for Wi-Fi.")

def get_news():
    api_key = config("NEWS_API_KEY")
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
    response = requests.get(url).json()
    if response["status"] == "ok":
        articles = response["articles"][:5]
        for article in articles:
            speak(article["title"])

def get_weather(city="London"):
    api_key = config("WEATHER_API_KEY")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    print(url)
    response = requests.get(url).json()
    if response.get("main"):
        temp = response["main"]["temp"]
        description = response["weather"][0]["description"]
        speak(f"The temperature in {city} is {temp}°C with {description}.")
    else:
        speak("Weather data not available.")

def set_reminder(message, delay):
    speak(f"Reminder set for {message} in {delay} seconds.")
    threading.Timer(delay, lambda: speak(f"Reminder: {message}")).start()\
    
def get_age(dob):
    # dob format: "25 May 2024" (e.g., "25 May 2024")
    try:
        birth_date = datetime.strptime(dob, "%d %B %Y")
        today = datetime.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age
    except ValueError:
        speak("Invalid date format. Please use the format: DD Month YYYY, e.g., 25 May 2024.")
        return None
    
def convert_currency(amount, base_currency, target_currency):
    try:
        # API endpoint for currency conversion
        # url = f"https://api.exchangerate.host/convert?from={base_currency}&to={target_currency}&amount={amount}"
        url = f"https://api.exchangerate.host/convert?access_key=0ff42acdb11f37ae6565b1a01e26d665&from={base_currency}&to={target_currency}&amount={amount}&format=1"
        # Making the API request
        response = requests.get(url)
        data = response.json()
        
        # Check if the request was successful
        if response.status_code == 200 and data["info"]:
            converted_amount = data["result"]
            return converted_amount
        else:
            speak("Sorry, I couldn't fetch the conversion rate. Please try again.")
            return None
    except Exception as e:
        speak("An error occurred while trying to convert the currency.")
        print(e)
        return None
    



def translate_text_file(file_path, target_language):

    translator = Translator()
    
    try:
        # Read the text from the file
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()
        
        # Translate the text
        translated = translator.translate(text, dest=target_language)
        
        # Print or return the translated text
        print(f"Translated text:\n{translated.text}")
        return translated.text

    except Exception as e:
        print("An error occurred during translation.")
        print(e)
        return None
    

def read_text_file(file_path, language='en'):
    media_dir = config("MEDIA_DIR4")
    try:
        # Open the file and read its content
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()

        # Initialize the TTS engine (gTTS or pyttsx3)
        tts = gTTS(text=text, lang=language)
        output_file_path = os.path.join(media_dir, "output.mp3")
        tts.save(output_file_path) # Save the speech as an mp3 file

        # Play the mp3 file (can use OS command to play)
        os.system(f"start {output_file_path}")   # For Windows
        # os.system("mpg321 output.mp3")  # For Linux/MacOS

        speak("I have read the text file aloud.")
    except Exception as e:
        print(f"Error reading or processing file: {e}")
        speak("Sorry, there was an error reading the file.")
