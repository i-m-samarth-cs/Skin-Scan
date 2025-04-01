import streamlit as st
from PIL import Image
import os

def show():
    """Display the about page for the SkinScan application"""
    
    # Set custom page title and styles for better presentation
    #st.set_page_config(page_title="About SkinScan - Early Detection of Skin Cancer", page_icon="🩺", layout="wide")
    
    # Title
    st.markdown("<h1 style='text-align: center; color: #3b7bbf;'>Welcome to SkinScan</h1>", unsafe_allow_html=True)
    
    # App description
    st.markdown("""
    ## What is SkinScan?
    
    **SkinScan** is an innovative, AI-powered application designed to assist healthcare professionals in the early detection 
    and classification of skin lesions that may indicate skin cancer. Leveraging cutting-edge deep learning technology, 
    SkinScan analyzes skin lesion images and provides real-time predictions, aiding in faster and more accurate diagnosis.
    
    **Important Disclaimer:** SkinScan is a supplementary tool and is not a replacement for professional medical judgment. 
    The predictions provided by the app must always be verified by qualified healthcare providers.
    """)

    # Interactive image of skin cancer to grab attention
    try:
        image = Image.open("assets/images/skin-cancer-awareness.jpeg")  # You can replace the path with your image
        st.image(image, caption="Skin Cancer Awareness", use_column_width=True)
    except:
        st.write("Image not available")

    # About Skin Cancer Section
    st.markdown("""
    ## Understanding Skin Cancer
    
    Skin cancer is one of the most common cancers worldwide. Early detection can dramatically increase the chances of successful treatment. 
    Here are the main types of skin cancer and their warning signs:
    """)

    # Create columns for different types of skin cancer
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Melanoma
        The most dangerous type of skin cancer, melanoma develops in melanocytes (cells that produce pigment). 
        Early detection is critical for successful treatment.
        
        **Warning Signs (ABCDE rule):**
        - **A**symmetry
        - **B**order irregularity
        - **C**olor variation
        - **D**iameter larger than 6mm
        - **E**volving over time
        """)
        
        st.markdown("""
        ### Basal Cell Carcinoma (BCC)
        BCC is the most common type of skin cancer but typically does not spread. However, if untreated, it can cause significant damage to the skin.
        
        **Warning Signs:**
        - Pearly bump or flat scar-like lesion
        - Bleeding or scabbing sores
        """)

    with col2:
        st.markdown("""
        ### Squamous Cell Carcinoma (SCC)
        SCC is the second most common skin cancer and can spread to other parts if not treated early.
        
        **Warning Signs:**
        - Firm red nodule
        - Crusty, scaly lesion
        - Sores on old scars
        """)
        
        st.markdown("""
        ### Other Types
        Less common types include Merkel cell carcinoma and dermatofibrosarcoma protuberans, among others.
        """)

    # Risk Factors Section
    st.markdown("""
    ## Risk Factors
    
    Several factors can increase the likelihood of developing skin cancer:
    - **UV Exposure:** Excessive sun exposure or tanning beds
    - **Fair Skin:** Less protection from UV radiation
    - **History of Sunburns:** Especially early in life
    - **Family History:** Genetic predisposition
    - **Age:** Risk increases with age
    - **Unusual Moles:** Some moles can indicate higher risk
    - **Weak Immune System:** Due to disease or medications
    """)

    # Prevention Tips Section
    st.markdown("""
    ## Prevention Tips
    
    Preventing skin cancer involves simple but effective strategies:
    - **Sun Protection:** Use broad-spectrum sunscreen (SPF 30+)
    - **Avoid Peak Sun Hours:** Minimize exposure between 10 AM and 4 PM
    - **Wear Protective Clothing:** Hats, sunglasses, long sleeves
    - **Skip Tanning Beds:** Avoid artificial UV exposure
    - **Regular Checks:** Perform monthly self-examinations and annual dermatologist visits
    """)

    # Technology Behind SkinScan Section
    st.markdown("""
    ## Technology Behind SkinScan
    
    SkinScan uses a **deep convolutional neural network (CNN)** trained on thousands of dermatological images. 
    The model processes the images, learns from each new analysis, and provides predictions with a high level of accuracy.
    
    **How it Works:**
    1. **Image Upload:** Healthcare professionals upload skin lesion images
    2. **Image Preprocessing:** The app standardizes images for analysis
    3. **AI Analysis:** Our CNN model processes the image and predicts potential skin cancer types
    4. **Results Displayed:** Predictions with confidence levels and recommendations are shown
    5. **Follow-up:** Results can be saved to patient records
    """)

    # Team Information - Adding you to the team
    st.markdown("""
    ## Meet the Team
    
    SkinScan was developed by a passionate and multidisciplinary team of professionals. Here's a quick look at the team behind SkinScan:
    
    ### Samarth Shendre – AI/ML Lead
    Samarth is the AI/ML lead at SkinScan, bringing expertise in machine learning, deep learning, and predictive analytics. He spearheads the development of our advanced AI models, ensuring that SkinScan provides accurate predictions and helps in early detection of skin cancer.
    
    ### Other Team Members
    Our team includes dermatologists, software engineers, and data scientists working together to create a powerful tool that aids healthcare professionals in making faster, more accurate diagnoses.
    
    **Contact us**: info@skinscan-app.com
    """)

    # References Section
    st.markdown("""
    ## References and Further Reading
    
    1. American Academy of Dermatology. (2021). Skin cancer overview.
    2. Skin Cancer Foundation. (2021). Information on skin cancer.
    3. Esteva, A., et al. (2017). Dermatologist-level classification of skin cancer with deep neural networks. Nature.
    4. Codella, N.C., et al. (2018). Skin lesion analysis for melanoma detection.
    """)

if __name__ == "__main__":
    show()
