import tensorflow as tf
import numpy as np
import cv2
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Define class names based on HAM10000 dataset
SKIN_CLASSES = {
    'akiec': 'Actinic Keratoses and Intraepithelial Carcinoma',
    'bcc': 'Basal Cell Carcinoma',
    'bkl': 'Benign Keratosis-like Lesions',
    'df': 'Dermatofibroma',
    'mel': 'Melanoma',
    'nv': 'Melanocytic Nevi',
    'vasc': 'Vascular Lesions'
}

# Class descriptions with risk levels and recommendations
CLASS_INFO = {
    'akiec': {
        "description": "Actinic Keratoses (Solar Keratoses) and Intraepithelial Carcinoma (Bowen's disease) are common non-melanoma skin cancers or pre-cancers.",
        "risk_level": "Medium-High",
        "recommendation": "Immediate dermatologist consultation. Early treatment is important to prevent progression."
    },
    # Other class definitions...
}
    'bcc': {
        'description': 'Basal Cell Carcinoma is the most common type of skin cancer. It rarely metastasizes but can cause significant local damage if left untreated.',
        'risk_level': 'Medium',
        'recommendation': 'Needs dermatologist consultation. Several treatment options are available depending on size and location.'
    },
    'bkl': {
        'description': 'Benign Keratosis-like Lesions include seborrheic keratoses, solar lentigo, and lichen-planus like keratosis. These are non-cancerous growths.',
        'risk_level': 'Low',
        'recommendation': 'Generally benign, but monitoring is recommended. Consult a dermatologist if changes occur.'
    },
    'df': {
        'description': 'Dermatofibroma is a common benign skin tumor that most often appears on the legs.',
        'risk_level': 'Very Low',
        'recommendation': 'Typically benign and requires no treatment unless causing discomfort.'
    },
    'mel': {
        'description': 'Melanoma is the most dangerous form of skin cancer. It develops from the pigment-producing cells known as melanocytes.',
        'risk_level': 'High',
        'recommendation': 'Immediate medical attention required. Early detection and treatment are crucial for survival.'
    },
    'nv': {
        'description': 'Melanocytic Nevi are benign moles. Most people have several, and they're usually harmless.',
        'risk_level': 'Very Low',
        'recommendation': 'Generally benign, but regular monitoring for changes in size, shape, or color is recommended.'
    },
    'vasc': {
        'description': 'Vascular Lesions include cherry angiomas, angiokeratomas, and pyogenic granulomas. Most are benign.',
        'risk_level': 'Low',
        'recommendation': 'Usually benign, but consult a dermatologist if they bleed or change rapidly.'
    }
}

# Handle model loading and prediction
class SkinCancerModel:
    def __init__(self, model_path='models/skin_cancer_model.h5'):
        self.model = None
        self.model_path = model_path
        self.img_size = (224, 224)  # Standard size for many CNN models
    
    def load_model(self):
        try:
            self.model = load_model(self.model_path)
            return True
        except Exception as e:
            print(f"Error loading model: {e}")
            return False
    
    def preprocess_image(self, img_path):
        # Read and preprocess the image
        img = cv2.imread(img_path)
        img = cv2.resize(img, self.img_size)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Normalize the image
        img = img / 255.0
        
        # Add batch dimension
        img = np.expand_dims(img, axis=0)
        return img
    
    def predict(self, img_path):
        if self.model is None:
            success = self.load_model()
            if not success:
                return None, None
        
        # Preprocess image
        processed_img = self.preprocess_image(img_path)
        
        # Make prediction
        predictions = self.model.predict(processed_img)
        
        # Get class with highest probability
        predicted_class_index = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_class_index])
        
        # Map index to class name
        class_keys = list(SKIN_CLASSES.keys())
        predicted_class = class_keys[predicted_class_index]
        
        # Return class name and confidence
        return predicted_class, confidence
    
    def get_class_info(self, class_name):
        return {
            'name': SKIN_CLASSES.get(class_name, "Unknown"),
            'info': CLASS_INFO.get(class_name, {
                'description': 'Information not available',
                'risk_level': 'Unknown',
                'recommendation': 'Please consult a medical professional'
            })
        }
