import streamlit as st
import subprocess
import threading
import time
import queue
import sys
from io import StringIO

# Create a queue to capture output
output_queue = queue.Queue()

class OutputCapturer:
    def __init__(self, queue):
        self.queue = queue
    
    def write(self, text):
        self.queue.put(text)
    
    def flush(self):
        pass

# Redirect stdout to our capturer
sys.stdout = OutputCapturer(output_queue)

# Function to run the main BlindBot program
def run_blindbot():
    import speech
    import detect
    import datetime
    import functions
    import gemini
    from read import read_text_from_camera
    from ultralytics import YOLO

    subprocess.Popen(["python3", "Navigation.py"])

    # Load model
    model = YOLO("yolov8s.pt")

    project_id = "blindbot-4f356"
    engine = speech.speech_to_text()

    listening = False

    while True:
        if not listening:
            resp = engine.recognize_speech_from_mic()
            print(f"You said: {resp}")

            if resp and "alexa" in resp.lower():
                engine.text_speech("Hi my name is Alexa. How can I assist you?")
                listening = True

        else:
            resp = engine.recognize_speech_from_mic()
            intent, text = None, None

            if resp:
                print(f"User said: {resp}")

                try:
                    intent, text = detect.detect_intent_texts(project_id, 0, [resp], 'en')
                    print(f"Detected Intent: {intent}, Detected Text: {text}")
                except Exception as e:
                    print(f"Error detecting intent: {e}")
                    engine.text_speech("I could not process that, please try again.")
                    continue

                if intent:
                    if intent == "Describe":
                        engine.text_speech("Describing scene")
                        detect.describe_scene(model, engine)
                    elif intent == "Brightness":
                        brightness = functions.get_brightness()
                        engine.text_speech(f"It is {brightness} outside")
                    elif intent == "Read":
                        engine.text_speech("I will capture an image and read any text I find.")
                        read_text_from_camera()
                    elif intent == "Time":
                        currentDT = datetime.datetime.now()
                        engine.text_speech(f"The time is {currentDT.hour} hours and {currentDT.minute} minutes")
                    elif intent == "GeneralQuery":
                        description = gemini.fetch_description(text)
                        engine.text_speech(description)

                        engine.text_speech("Would you like more details?")
                        follow_up = engine.recognize_speech_from_mic()

                        if follow_up and "yes" in follow_up.lower():
                            additional_info = gemini.ask_gemini(text)
                            engine.text_speech(additional_info)
                    elif intent == "Navigate":
                        functions.handle_navigation(engine)
                else:
                    engine.text_speech("Sorry, I could not understand.")

# Streamlit UI
st.title("BlindBot Assistant")
st.write("Voice-controlled assistant for the visually impaired")

# Status area
status_container = st.empty()
output_container = st.empty()

# Start/Stop buttons
if 'running' not in st.session_state:
    st.session_state.running = False

def start_bot():
    st.session_state.running = True
    thread = threading.Thread(target=run_blindbot)
    thread.daemon = True
    thread.start()

def stop_bot():
    st.session_state.running = False
    status_container.warning("Stopping... (may take a moment)")

col1, col2 = st.columns(2)
with col1:
    if st.button("Start Assistant", disabled=st.session_state.running):
        start_bot()
with col2:
    if st.button("Stop Assistant", disabled=not st.session_state.running):
        stop_bot()

# Display output
if st.session_state.running:
    status_container.success("Assistant is running... Speak 'Alexa' to activate.")
else:
    status_container.info("Assistant is stopped. Press 'Start Assistant' to begin.")

# Continuously update the output display
output_text = ""
while True:
    try:
        new_output = output_queue.get_nowait()
        output_text += new_output
        output_container.text_area("Conversation Log", value=output_text, height=300)
    except queue.Empty:
        pass
    
    time.sleep(0.1)
