import cv2
import numpy as np
import brightness_analyzer

def get_brightness():
    """Capture an image from the webcam and determine brightness level."""
    cam = cv2.VideoCapture(0)

    if not cam.isOpened():
        print("Error: Could not open camera.")
        return "unknown"

    ret, frame = cam.read()
    cam.release()

    if not ret:
        print("Error: Could not capture frame.")
        return "unknown"

    return brightness_analyzer.analyze_frame(frame)

def process_results(results, engine):
    """Process model results and generate audio response."""
    response_generator.create_description(results, engine)

def handle_navigation(engine):
    """Handle navigation requests and routing."""
    navigation_handler.process_request(engine)
