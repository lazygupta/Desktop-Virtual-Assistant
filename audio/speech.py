import pyttsx3
import speech_recognition as sr
import ui.gui as gui

# Initialize the text-to-speech engine
engine = pyttsx3.init('sapi5')
engine.setProperty('rate', 170)
engine.setProperty('volume', 1.0)
engine.setProperty('voice', engine.getProperty('voices')[1].id)

def speak(text):
    global engine
    words = text.split()  # Split text into words
    if len(words) > 20:
        # Shorten the text to the first 20 words and add an indicator
        short_text = ' '.join(words[:30]) + " ... and many more You can look in the prompt text file for complete answers"
    else:
        short_text = text

    # Update GUI and speak the shortened text
    gui.update_text_speaker(short_text)
    if not text == "I have saved the file as prompt.txt in promptresults":
        engine.say(short_text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        gui.update_text_listener("Listening...")
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source, phrase_time_limit=5)
    
    try:
        query = r.recognize_google(audio, language='en-in')
        gui.update_text_listener(f"User said: {query}")
        return query
    except sr.UnknownValueError:
        gui.update_text_listener("Sorry, I couldn't understand that.")
    except sr.RequestError:
        gui.update_text_listener("Network error.")
    return None

if __name__ == '__main__':
    speak("Hello, how are you doing?")
    audio_text = listen()
    if audio_text:
        print(f"Recognized Speech: {audio_text}")
    else:
        print("No speech recognized.")

