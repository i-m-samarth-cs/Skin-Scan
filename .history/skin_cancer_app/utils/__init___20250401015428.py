# utils/__init__.py

# Import all utility modules for easier access
from utils.model_handler import SkinCancerModel, SKIN_CLASSES
from utils.image_processor import preprocess_image, augment_image, crop_lesion
from utils.db_manager import (
    init_db, 
    add_patient, 
    get_patient, 
    get_all_patients, 
    update_patient, 
    add_detection_record, 
    get_patient_detection_history, 
    get_all_detection_history
)
from utils.chatbot_utils import get_chatbot_response, preprocess_query, get_faq_response

# Version information
__version__ = '1.0.0'
