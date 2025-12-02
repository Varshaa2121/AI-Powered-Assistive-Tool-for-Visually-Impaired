import speech_recognition as __sr
import pyttsx3 as __tts

class __AudioCore:
    def __init__(self):
        self.__recognizer = __sr.Recognizer()
        self.__engine = __tts.init()
        self.__engine.setProperty('voice', self.__engine.getProperty('voices')[0].id)
        self.__engine.setProperty('rate', 150)

    def __listen(self):
        with __sr.Microphone() as source:
            print("Awaiting input...")
            self.__recognizer.adjust_for_ambient_noise(source, duration=1)
            captured = self.__recognizer.listen(source)
        return captured

    def _fetch_input(self):
        try:
            audio_data = self.__listen()
            return self.__recognizer.recognize_google(audio_data)
        except __sr.UnknownValueError:
            return None
        except __sr.RequestError:
            return "Speech service error"

    def _speak(self, context):
        print(f"Vocalizing: {context}")
        self.__engine.say(context)
        self.__engine.runAndWait()

def __spawn_speech():
    return __AudioCore()

if __name__ == "__main__":
    core = __spawn_speech()
    text = core._fetch_input()
    if text:
        core._speak(f"You said: {text}")
    else:
        core._speak("Could not understand. Please try again.")
