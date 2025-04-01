import re
import random
import json
import os
from google.cloud import translate_v2 as translate

# Load FAQ data
def load_faq_data():
    """Load FAQ data from JSON file, or return default data if file not found"""
    try:
        with open(os.path.join('assets', 'metadata', 'faq_data.json'), 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Return default FAQ data if file not found or invalid
        return {
            "faqs": [
                {
                    "question": "What are the warning signs of melanoma?",
                    "answer": "Look for the ABCDE warning signs: Asymmetry, Border irregularity, Color variation, Diameter larger than 6mm, and Evolving size, shape, or color. If you notice any of these signs, consult a dermatologist promptly."
                },
                {
                    "question": "How often should I check my skin?",
                    "answer": "It's recommended to perform a self-examination once a month. Additionally, people with higher risk factors should have a professional skin examination by a dermatologist at least once a year."
                },
                {
                    "question": "What SPF sunscreen should I use?",
                    "answer": "Dermatologists recommend using a broad-spectrum sunscreen with an SPF of at least 30, which blocks 97% of UVB rays. Apply it generously and reapply every two hours, or more frequently if swimming or sweating."
                },
                {
                    "question": "How does the SkinScan app work?",
                    "answer": "SkinScan uses deep learning algorithms to analyze images of skin lesions. After you upload a photo, our AI model processes it and provides a prediction about the potential diagnosis, along with a confidence score and recommendations."
                },
                {
                    "question": "Can SkinScan diagnose my condition?",
                    "answer": "No, SkinScan cannot provide a medical diagnosis. It's designed as a supportive tool for healthcare professionals. All results should be reviewed by a qualified medical professional, and the app should not replace a consultation with a doctor."
                }
            ],
            "general_responses": [
                "I'm here to provide information about skin cancer and help you navigate the SkinScan app. For medical concerns, please consult a healthcare professional.",
                "That's an interesting question. While I can provide general information about skin health, I recommend discussing specific concerns with a dermatologist.",
                "I can help answer general questions about skin cancer and skin health, but remember that I'm not a replacement for professional medical advice."
            ],
            "navigation_help": {
                "detection": "To use the detection feature, go to the 'Skin Cancer Detection' page from the main menu. There you can upload an image of a skin lesion for analysis.",
                "patient_info": "You can manage patient information on the 'Patient Information' page. This allows you to add new patients or select existing ones before performing a detection.",
                "history": "The 'Detection History' page shows all previous analyses for the current patient or all patients. You can filter and sort the history as needed."
            }
        }

# FAQ data cache
_faq_data = None

def get_faq_data():
    """Get FAQ data with caching"""
    global _faq_data
    if _faq_data is None:
        _faq_data = load_faq_data()
    return _faq_data

def preprocess_query(query):
    """Preprocess user query for better matching"""
    query = query.lower()
    query = re.sub(r'[^\w\s]', '', query)  # Remove punctuation
    query = ' '.join(query.split())  # Remove extra whitespace
    return query

def get_best_match_faq(query):
    """Find the best matching FAQ for a query"""
    preprocessed_query = preprocess_query(query)
    faq_data = get_faq_data()

    best_match = None
    best_score = 0

    for faq in faq_data["faqs"]:
        faq_question = preprocess_query(faq["question"])
        words_in_query = set(preprocessed_query.split())
        words_in_faq = set(faq_question.split())
        common_words = words_in_query.intersection(words_in_faq)

        score = len(common_words) / len(words_in_query) if words_in_query else 0

        skin_cancer_terms = ["melanoma", "basal", "carcinoma", "squamous", "skin", "cancer",
                             "mole", "lesion", "sunscreen", "spf", "uv", "abcde"]
        for term in skin_cancer_terms:
            if term in preprocessed_query and term in faq_question:
                score += 0.2

        if score > best_score:
            best_score = score
            best_match = faq

    return best_match["answer"] if best_score > 0.4 else None

def get_navigation_help(query):
    """Provide navigation help based on user query"""
    preprocessed_query = preprocess_query(query)
    faq_data = get_faq_data()

    navigation_terms = {
        "detection": ["detection", "analyze", "scan", "upload", "image", "photo"],
        "patient_info": ["patient", "information", "profile", "register"],
        "history": ["history", "previous", "past", "record"]
    }

    for nav_type, terms in navigation_terms.items():
        if any(term in preprocessed_query for term in terms):
            return faq_data["navigation_help"].get(nav_type, "Use the navigation menu to explore the app.")

    return None

def get_faq_response(query):
    """Get response from FAQ database"""
    response = get_best_match_faq(query)
    return response if response else get_navigation_help(query) or random.choice(get_faq_data()["general_responses"])

def get_chatbot_response(query):
    """Generate a response for the user query"""
    greetings = ["hello", "hi", "hey", "greetings"]
    if preprocess_query(query) in greetings:
        return "Hello! How can I help you with skin cancer information or using the SkinScan app today?"

    if any(term in preprocess_query(query) for term in ["skinscan", "app", "application"]):
        if "how" in query.lower() and any(word in query.lower() for word in ["use", "work"]):
            return "SkinScan works by analyzing images of skin lesions using AI. Upload an image in the Detection page to get a result."
        if "accurate" in query.lower():
            return "SkinScan achieves around 85-90% accuracy on validation datasets, but should be used as a supportive tool for doctors."

    return get_faq_response(query)