import cv2
import functions  

def detect_intent_texts(project_id, session_id, texts, language_code):
    """
    Detects user intent from spoken text.
    """
    text = texts[0].lower() if texts else ""
    
    if "time" in text:
        return "Time", "Time query"
    elif "describe" in text:
        return "Describe", "Scene description"
    elif "brightness" in text:
        return "Brightness", "Light analysis"  
    elif "read" in text:
        return "Read", "Text recognition"
    elif "navigate" in text:
        return "Navigate", "Navigation request"
    else:
        return "GeneralQuery", text

def describe_scene(model, engine):
    """
    Captures image and analyzes surroundings.
    """
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    cam.release()

    if not ret:
        engine.text_speech("Camera access unavailable.")
        return

    results = model(frame)
    functions.process_results(results, engine)

def detect_text(engine):
    """
    Captures image and processes text recognition.
    """
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    cam.release()

    if not ret:
        engine.text_speech("Camera unavailable.")
        return

    functions.extract_text(frame, engine)
