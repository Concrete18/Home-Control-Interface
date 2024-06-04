import speech_recognition as sr
import os


def process_voice_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
        audio = recognizer.listen(source)

    try:
        # Recognize the audio and convert it to text
        command = recognizer.recognize_google(audio).lower()
        print("You said:", command)
        return command
    except sr.UnknownValueError:
        print("Sorry, I didn't understand that.")
        return ""
    except sr.RequestError:
        print("Sorry, there was an issue connecting to the service.")
        return ""


def on_key_press1():
    command = process_voice_command()

    if (
        "run" in command
        or "execute" in command
        or "open" in command
        or "start" in command
    ):
        if "explorer" in command and ("don't" or "not") not in command:
            os.system("explorer")
        elif "notepad" in command and ("don't" or "not") not in command:
            os.system("notepad")
        elif "chrome" in command and ("don't" or "not") not in command:
            os.system("chrome")
        elif "microsoft" in command and ("don't" or "not") not in command:
            os.system("start microsoft-edge:")
        elif "calculator" in command and ("don't" or "not") not in command:
            os.system("calc")
        else:
            print("Command not supported.")

    elif "goodbye" in command:
        print("Goodbye! Have a great day!")
        quit()  # Exit the program

    elif "stop" in command:
        print("Stopping the voice recognition system.")
        quit()  # Exit the program

    else:
        print("Command not supported.")


on_key_press1()
