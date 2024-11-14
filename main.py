from audio.speech import speak, listen
from decouple import config 
from aim.conv import converse 
from act.actions import (
    open_notepad, open_word, open_excel, open_ppt, open_calculator, open_cmd, 
    take_screenshot, start_screen_record, stop_screen_record, open_camera, 
    camera_vision, open_website, search_files, set_volume, get_system_info, 
    read_clipboard, copy_to_clipboard, check_battery, toggle_wifi, get_news, 
    get_weather, set_reminder, get_age, convert_currency, translate_text_file, read_text_file
)
import threading
import ui.gui as gui 
import time
import os

BOT_NAME = config("VA_NAME")

exit_event = threading.Event()

def start_gui():
    gui.appear()

if __name__ == '__main__':
    awake = True
    gui_thread = threading.Thread(target=start_gui)
    gui_thread.start()

    speak(f"I am {BOT_NAME}. How may I help you?")

    while True:
        query = listen()
        if query is None:
            continue
        else:
            query = query.lower()
            intent = converse(query) 

        print(f"User Query: {query}")
        print(f"Identified Intent: {intent}")

        if not intent.startswith('ACTION_'):
            media_dir = config("MEDIA_DIR2")
            text_file = config("PROMPT_FILE")
            file_path = os.path.join(media_dir, text_file)
            with open(file_path, "w", encoding="utf-8") as output_file:
                output_file.write(intent)
                speak("I have saved the file as prompt.txt in promptresults")

            speak(intent)
            continue

        # Handling specific actions
        if intent == 'ACTION_AWAKEN':
            awake = True
            speak("How can I help you Sir?")
            gui.awaken()
            continue

        elif intent == 'ACTION_SLEEP':
            awake = False
            speak("Hibernating now")
            gui.sleep()
            continue

        if not awake:
            print("Currently hibernating...Zzzz...nothing to do.")
            continue

        elif intent == 'ACTION_EXIT':
            speak('Have a good day Sir')
            time.sleep(4)
            gui.close_window(exit_event)
            exit(1)

        elif intent == 'ACTION_APPEAR':
            gui_thread = threading.Thread(target=start_gui)
            gui_thread.start()

        elif intent == 'ACTION_MINIMIZE_DISAPPEAR_APPLICATION':
            gui.disappear()

        elif intent == 'ACTION_OPEN_NOTEPAD':
            open_notepad()

        elif intent == 'ACTION_OPEN_WORD':
            open_word()

        elif intent == 'ACTION_OPEN_EXCEL':
            open_excel()

        elif intent == 'ACTION_OPEN_POWERPOINT':
            open_ppt()

        elif intent == 'ACTION_OPEN_COMMAND_PROMPT':
            open_cmd()

        elif intent == 'ACTION_OPEN_CALCULATOR':
            open_calculator()

        elif intent == "ACTION_OPEN_BROWSER_WEBSITE":
            open_website()

        elif intent == "ACTION_TAKE_SCREENSHOT":
            take_screenshot()

        elif intent == "ACTION_START_SCREEN_RECORDING": #1
            start_screen_record()

        elif intent == "ACTION_STOP_SCREEN_RECORDING":
            stop_screen_record()

        elif intent == "ACTION_OPEN_CAMERA":
            open_camera()

        elif intent == "ACTION_WHAT_DO_YOU_SEE_IN_CAMERA": 
            camera_vision()

        elif intent == "ACTION_SEARCH_FILES":
            speak("What file are you looking for?")
            filename = listen().lower()  # Captures the filename from the user's response
            print(filename)

            speak("In which directory would you like to search?")
            directory = listen().strip()  # Captures the directory from the user's response
            print(directory)

            search_files(filename, directory)  # Pass both filename and directory to search_files function


        elif intent == "ACTION_SET_VOLUME":
            speak("At what level would you like to set the volume? (0 to 100)")
            try:
                level = int(listen())
                set_volume(level)
            except ValueError:
                speak("Sorry, I didn't catch a valid number for the volume level.")

        elif intent == "ACTION_GET_SYSTEM_INFO":
            get_system_info()

        elif intent == "ACTION_READ_CLIPBOARD":
            read_clipboard()

        elif intent == "ACTION_COPY_TO_CLIPBOARD":
            speak("What would you like to copy to the clipboard?")
            text = listen()
            copy_to_clipboard(text)

        elif intent == "ACTION_CHECK_BATTERY":
            check_battery()

        elif intent == "ACTION_TOGGLE_WIFI":
            speak("Would you like to turn Wi-Fi on or off?")
            state = listen().lower()
            toggle_wifi(state)

        elif intent == "ACTION_GET_NEWS":
            get_news()

        elif intent == "ACTION_GET_WEATHER":
            speak("Which city would you like the weather for?")
            city = listen().lower()
            print(city)
            get_weather(city)


        elif intent == "ACTION_SET_REMINDER":
            speak("What would you like to be reminded about?")
            message = listen()
            speak("In how many seconds should I remind you?")
            try:
                delay = int(listen())
                set_reminder(message, delay)
            except ValueError:
                speak("Sorry, I didn't catch a valid number for the delay.")

        elif intent == "ACTION_CALC_AGE":
            speak("Please tell me your date of birth in the format: Date Month Year (example 25 May 2024).")
            dob = listen().lower()  # Listen to the user's input
            age = get_age(dob)  # Calculate the age
            if age is not None:
                speak(f"Your age is {age} years.")
            else:
                speak("Sorry, I couldn't calculate your age. Please try again.")


        elif intent == "ACTION_CONVERT_CURRENCY":
            speak("Please tell me the amount and currency you want to convert from in format amount & currency (For example 100 USD)")
            amount_and_base_currency = listen()  # e.g., "100 USD"
    
            speak("Please tell me the currency you want to convert to for example EUR")
            target_currency = listen()  # e.g., "EUR"
    
            # Extract amount and base currency from the user's input
            try:
                amount, base_currency = amount_and_base_currency.split()[:2]
                amount = float(amount)
        
                # Call the currency conversion function
                converted_amount = convert_currency(amount, base_currency.upper(), target_currency.upper())
        
                if converted_amount is not None:
                    speak(f"{amount} {base_currency.upper()} is approximately {converted_amount:.2f} {target_currency.upper()}.")
                else:
                    speak("Sorry, I couldn't complete the conversion.")
            except ValueError:
                speak("Please provide the amount and currency in a valid format, like '100 USD'.")


        elif intent == "ACTION_TRANSLATE_TEXT_FILE":
            media_dir = config("MEDIA_DIR2")
            text_file = config("PROMPT_FILE")
            file_path = os.path.join(media_dir, text_file)
            
            def get_language():
                speak("Which language would you like to translate to?")
    
                while True:
                    try:
                        target_language = listen().lower()
                        return target_language
                    except Exception as e:
                        print(f"Error: {e}. Trying to listen again...")
                        speak("I didn't catch that. Could you please repeat?")

            language_codes = {
                "spanish": "es",
                "french": "fr",
                "german": "de",
                "chinese": "zh-cn",
                "english": "en",
                "hindi": "hi",
                "malayalam": "ml",
            }
            
            lang_text = get_language()

            target_language_code = language_codes.get(lang_text)
    
            if target_language_code:
                translated_text = translate_text_file(file_path, target_language_code)
                if translated_text:
                    translated_file_path = os.path.join(config("MEDIA_DIR1"), "translated.txt")
                    with open(translated_file_path, "w", encoding="utf-8") as output_file:
                        output_file.write(translated_text)
            
                    speak(f"The text has been translated to {lang_text}.")
                else:
                    speak("Sorry, I couldn't translate the text.")
            else:
                speak("Sorry, I couldn't recognize that language.")


        elif intent == "ACTION_READ_TEXT_FILE":
            media_dir = config("MEDIA_DIR1")
            text_file = config("TEXT_FILE")
            file_path = os.path.join(media_dir, text_file)
            
            def get_language():
                speak("Which language is the text file in?")
    
                while True:
                    try:
                        target_language = listen().lower()
                        return target_language
                    except Exception as e:
                        print(f"Error: {e}. Trying to listen again...")
                        speak("I didn't catch that. Could you please repeat?")

            language = get_language()

            language_codes = {
                "spanish": "es",
                "french": "fr",
                "german": "de",
                "chinese": "zh-cn",
                "english": "en",        
                "hindi": "hi",
                "malayalam": "ml",
            }

            target_language_code = language_codes.get(language)
            print(file_path)
            print(target_language_code)

            if target_language_code:
                read_text_file(file_path, target_language_code)  
            else:
                speak("Sorry, I couldn't recognize that language.")     
