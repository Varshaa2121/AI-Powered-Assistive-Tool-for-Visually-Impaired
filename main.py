import speech
import detect
import datetime
import functions
import gemini
from read import read_text_from_camera
from ultralytics import YOLO

import subprocess
subprocess.Popen(["python3", "Navigation.py"])

model = YOLO("yolov8s\.pt")

project_id = "your-project-id"
engine = speech.speech_to_text()
listening = False

while True:
    if not listening:
        resp = engine.recognize_speech_from_mic()
        if resp and "wakeword" in resp.lower():
            engine.text_speech("Assistant activated.")
            listening = True
    else:
        resp = engine.recognize_speech_from_mic()
        intent, text = None, None

        if resp:
            try:
                intent, text = detect.detect_intent_texts(project_id, 0, [resp], 'en')
            except Exception:
                engine.text_speech("Please try again.")
                continue

        if intent:
            if intent == "Describe":
                engine.text_speech("Processing scene description.")
                detect.describe_scene(model, engine)

            elif intent == "Brightness":
                brightness = functions.get_brightness()
                engine.text_speech(f"Brightness level: {brightness}")

            elif intent == "Read":
                engine.text_speech("Reading text.")
                read_text_from_camera()

            elif intent == "Time":
                now = datetime.datetime.now()
                engine.text_speech(f"The time is {now.hour}:{now.minute}")

            elif intent == "GeneralQuery":
                response = gemini.fetch_description(text)
                engine.text_speech(response)

                engine.text_speech("Do you want more details?")
                follow_up = engine.recognize_speech_from_mic()
                if follow_up and "yes" in follow_up.lower():
                    additional = gemini.ask_gemini(text)
                    engine.text_speech(additional)

            elif intent == "Navigate":
                engine.text_speech("Where would you like to go?")
                destination = engine.recognize_speech_from_mic()
                if destination:
                    engine.text_speech(f"Searching for {destination}")
                    engine.text_speech("Navigation started.")
        else:
            engine.text_speech("Sorry, I could not understand.")
