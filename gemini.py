import google.generativeai as genai

genai.configure(api_key="AIzaSyA0evdRguiOGlIQ0JgIzwrx-Bb0JVtcjLY")
model = genai.GenerativeModel("gemini-2.0-flash")

def fetch_description(query):
    """Fetch brief description from Gemini AI"""
    pass

def fetch_additional_info(query):
    """Fetch additional information from Gemini AI"""
    pass

def ask_gemini(query):
    """Fetch a human-like response from Gemini AI"""
    pass

def fetch_sentence(ocr_text):
    """Convert extracted OCR text into a meaningful sentence while keeping the original intent."""
    pass
