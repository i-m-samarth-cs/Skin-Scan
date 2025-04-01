import random
import re

# Define chatbot responses
GREETING_PATTERNS = [
    r'hello', r'hi', r'hey', r'greetings', r'good morning', r'good afternoon', r'good evening'
]

GREETING_RESPONSES = [
    "Hello! How can I help you with skin cancer detection today?",
    "Hi there! Do you have questions about skin cancer or our detection system?",
    "Greetings! I'm here to assist with your skin cancer detection needs.",
    "Hello! I'm your skin cancer detection assistant. How can I help?"
]

FAREWELL_PATTERNS = [
    r'goodbye', r'bye', r'see you', r'exit', r'quit'
]

FAREWELL_RESPONSES = [
    "Goodbye! Stay vigilant about your skin health!",
    "Take care! Remember to regularly check your skin for changes.",
    "Bye for now! Don't hesitate to return if you have more questions."
]

SKIN_CANCER_QUESTIONS = {
    r'what is (skin cancer|melanoma)': 
        "Skin cancer is an abnormal growth of skin cells, most often developed on skin exposed to the sun. Melanoma is the most serious type of skin cancer, developing from the pigment-producing cells known as melanocytes.",
    
    r'(symptoms|signs) of (skin cancer|melanoma)': 
        "Common signs of skin cancer include changes in the skin such as new growths or changes in existing moles. Remember the ABCDE rule: Asymmetry, Border irregularity, Color changes, Diameter growth, and Evolution or change over time.",
    
    r'how (accurate|reliable) is this (app|system|detection)': 
        "Our system uses deep learning trained on thousands of dermatological images. While it achieves good accuracy, it's designed to be a supportive tool and not a replacement for professional medical diagnosis. Always consult a dermatologist for proper evaluation.",
    
    r'(prevent|prevention) (skin cancer|melanoma)': 
        "Prevention strategies include: limiting sun exposure especially during peak hours (10am-4pm), wearing sunscreen (SPF 30+), wearing protective clothing, avoiding tanning beds, and performing regular skin self-exams.",
    
    r'(treatment|treat) (skin cancer|melanoma)': 
        "Treatment depends on the type, location, and stage of cancer, but may include: surgical removal, radiation therapy, chemotherapy, immunotherapy, targeted therapy, and photodynamic therapy. Early detection significantly improves treatment outcomes.",
    
    r'(risk factors|chances) (for|of) (skin cancer|melanoma)': 
        "Risk factors include: fair skin, history of sunburns, excessive sun exposure, tanning bed use, living in sunny or high-altitude climates, family history of skin cancer, personal history of skin cancer, weakened immune system, and exposure to radiation or certain substances.",
    
    r'(check|examine|self-exam) (skin|moles)': 
        "The ABCDE method helps identify suspicious moles: Asymmetry (uneven halves), Border (irregular, ragged edges), Color (varied shades), Diameter (larger than a pencil eraser), and Evolving (changing over time). Examine your entire body monthly and record any changes."
}

DEFAULT_RESPONSES = [
    "I'm not sure I understand. Could you rephrase your question about skin cancer or our detection system?",
    "I don't have information on that. Would you like to know about skin cancer types, prevention, or using our detection system?",
    "That's beyond my current knowledge. I can help with skin cancer detection, types of skin cancer, or preventive measures."
]

# Chatbot function
def get_chatbot_response(user_input):
    """Generate chatbot response based on user input"""
    user_input = user_input.lower()
    
    # Check for greetings
    for pattern in GREETING_PATTERNS:
        if re.search(pattern, user_input):
            return random.choice(GREETING_RESPONSES)
    
    # Check for farewells
    for pattern in FAREWELL_PATTERNS:
        if re.search(pattern, user_input):
            return random.choice(FAREWELL_RESPONSES)
    
    # Check for skin cancer questions
    for pattern, response in SKIN_CANCER_QUESTIONS.items():
        if re.search(pattern, user_input):
            return response
    
    # If user asks about using the app
    if re.search(r'(how to|how do I) (use|upload|scan|detect)', user_input):
        return "To use our skin cancer detection: 1) Go to the 'Skin Cancer Detection' page, 2) Upload a clear image of the skin lesion, 3) Click the 'Analyze' button, and 4) View the detailed results. For best results, ensure good lighting and focus on the lesion."
    
    # If user asks about accuracy or results interpretation
    if re.search(r'(interpret|understand|mean|accuracy|reliable) (results|prediction|diagnosis)', user_input):
        return "The results show the most likely skin condition based on visual patterns, with a confidence percentage. High risk conditions (especially melanoma) should be evaluated by a dermatologist regardless of confidence level. This tool is meant to assist, not replace, professional medical advice."
    
    # Default response
    return random.choice(DEFAULT_RESPONSES)
