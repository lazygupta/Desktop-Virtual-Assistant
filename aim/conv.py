from langchain_google_genai import ChatGoogleGenerativeAI
from decouple import config 
import string

api_key =  config("GOOGLE_GEMINI_API_KEY")

llm = ChatGoogleGenerativeAI(model="gemini-pro",google_api_key=api_key)

base_prompt = (
    "If a prompt matches an action description(Or somewhat prompt matching with action's description) from the list below, respond with only the action name (no additional text). "
    "For any question that does not explicitly request an action or matches only vaguely with an action, respond with an answer to those"
    "If a prompt is informational (such as asking 'Who is...'), respond with a conversational answer, providing facts as a general AI assistant."
    "If no suitable action is identified, respond naturally as a conversation, answering questions, sharing information, or providing explanations as needed.\n"
    
    "If a statement could be interpreted in multiple ways, clarify if necessary, or choose the most probable action based on context. "
    "For statements not matching an action, respond in a friendly, conversational manner, providing helpful and informative answers as a general AI assistant."
    
    "List of available actions and their descriptions:\n"
    "- ACTION_CALC_AGE: Calculate my age.\n"
    "- ACTION_AWAKEN: Wake up and start listening for commands.\n"
    "- ACTION_SLEEP: Enter hibernation or 'sleep' mode.\n"
    "- ACTION_APPEAR: Make the virtual assistant window appear.\n"
    "- ACTION_EXIT: Exit the virtual assistant program.\n"
    "- ACTION_OPEN_NOTEPAD: Open the Notepad application.\n"
    "- ACTION_OPEN_WORD: Open Microsoft Word.\n"
    "- ACTION_OPEN_EXCEL: Open Microsoft Excel.\n"
    "- ACTION_OPEN_POWERPOINT: Open Microsoft PowerPoint.\n"
    "- ACTION_OPEN_COMMAND_PROMPT: Open the Command Prompt.\n"
    "- ACTION_OPEN_CAMERA: Open the device camera.\n"
    "- ACTION_OPEN_CALCULATOR: Open the calculator application.\n"
    "- ACTION_FIND_MY_IP: Find and display the device's IP address.\n"
    "- ACTION_OPEN_YOUTUBE: Open YouTube in the default browser.\n"
    "- ACTION_GET_WEATHER: Check and display current weather information.\n"
    "- ACTION_TAKE_SCREENSHOT: Capture a screenshot.\n"
    "- ACTION_START_SCREEN_RECORDING: Start screen recording.\n"
    "- ACTION_STOP_SCREEN_RECORDING: Stop screen recording.\n"
    "- ACTION_MINIMIZE_DISAPPEAR_APPLICATION: Minimize or hide the virtual assistant application window.\n"
    "- ACTION_OPEN_BROWSER_WEBSITE: Open a website in the default browser.\n"
    "- ACTION_SEARCH_FILES: Search a file\n"
    "- ACTION_WHAT_DO_YOU_SEE_IN_CAMERA: Take a photo from my camera or Click a Photo of myself\n"
    "- ACTION_CONVERT_CURRENCY: Convert a currency or Currency Converter\n"
    "- ACTION_TRANSLATE_TEXT_FILE: Translate language or Translate the file\n"
    "- ACTION_READ_TEXT_FILE: Read the text file or Read the file\n"
)

def remove_punctuation(text):
    # Remove asterisks and punctuation from the response
    return text.replace("*", "").translate(str.maketrans("", "", string.punctuation))

def converse(query):
    
    prompt = base_prompt + " Statement prompt is: '" + query + "'"
    result = llm.invoke(prompt)
    response = result.content

    if response.startswith("ACTION_"):
        print(f"Executing action: {response}")
        return response
    else:
        prompt = query
        result = llm.invoke(prompt)
        response = result.content
        cleaned_response = remove_punctuation(response)
        print("Conversational response:", cleaned_response)
        return cleaned_response


if __name__ == '__main__':
    converse("Where is Kerala")