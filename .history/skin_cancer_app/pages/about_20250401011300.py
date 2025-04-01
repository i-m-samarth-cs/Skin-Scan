import streamlit as st
from PIL import Image
import os

def show():
    """Display the about page for the SkinScan application"""
    st.markdown("<h1 style='text-align: center;'>About SkinScan</h1>", unsafe_allow_html=True)
    
    # App description
    st.markdown("""
    ## What is SkinScan?
    
    SkinScan is an AI-powered application designed to assist healthcare professionals in the early detection 
    and classification of skin lesions that may indicate skin cancer. By leveraging deep learning technology, 
    SkinScan can analyze images of skin lesions and provide predictions on potential diagnoses.
    
    **Important Disclaimer:** SkinScan is intended to be used as a supportive tool for healthcare professionals 
    and should not replace clinical judgment or professional medical advice. The predictions made by the 
    application should always be verified by qualified medical personnel.
    """)
    
    # Information about skin cancer
    st.markdown("""
    ## About Skin Cancer
    
    Skin cancer is one of the most common forms of cancer globally. Early detection significantly increases 
    the chances of successful treatment. There are several types of skin cancer, with the most common being:
    """)
    
    # Create columns for different types of skin cancer
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Melanoma
        Melanoma is the most dangerous form of skin cancer. It develops in the cells that produce melanin, 
        the pigment that gives skin its color. Melanoma can spread to other parts of the body if not treated early.
        
        **Warning Signs (ABCDE rule):**
        - **A**symmetry: One half of the mole doesn't match the other
        - **B**order: Irregular, ragged, notched, or blurred edges
        - **C**olor: Varied colors within the same mole
        - **D**iameter: Larger than 6mm (pencil eraser size)
        - **E**volving: Changes in size, shape, color, or elevation
        """)
        
        st.markdown("""
        ### Basal Cell Carcinoma (BCC)
        BCC is the most common type of skin cancer. It rarely metastasizes but can cause significant local damage 
        if left untreated.
        
        **Warning Signs:**
        - Pearly or waxy bump
        - Flat, flesh-colored or brown scar-like lesion
        - Bleeding or scabbing sore that heals and returns
        """)
    
    with col2:
        st.markdown("""
        ### Squamous Cell Carcinoma (SCC)
        SCC is the second most common type of skin cancer. It can spread to other parts of the body 
        if not treated early.
        
        **Warning Signs:**
        - Firm, red nodule
        - Flat lesion with a scaly, crusted surface
        - New sore or raised area on an old scar or ulcer
        """)
        
        st.markdown("""
        ### Other Types
        Other less common types include Merkel cell carcinoma, dermatofibrosarcoma protuberans, 
        sebaceous carcinoma, and various skin lymphomas.
        """)
    
    # Risk factors
    st.markdown("""
    ## Risk Factors
    
    Several factors can increase your risk of developing skin cancer:
    
    - **UV Exposure:** Excessive sun exposure or tanning beds
    - **Fair Skin:** Less melanin provides less protection from UV radiation
    - **History of Sunburns:** Especially severe sunburns early in life
    - **Family History:** Genetic predisposition
    - **Age:** Risk increases with age due to cumulative sun exposure
    - **Numerous or Unusual Moles:** Certain types of moles increase risk
    - **Weakened Immune System:** From disease or medications
    """)
    
    # Prevention
    st.markdown("""
    ## Prevention Tips
    
    Most skin cancers can be prevented by taking simple protective measures:
    
    - **Sun Protection:** Use broad-spectrum sunscreen (SPF 30+), reapply every 2 hours
    - **Avoid Peak Hours:** Minimize exposure between 10 AM and 4 PM
    - **Protective Clothing:** Wear hats, long sleeves, and sunglasses
    - **No Tanning Beds:** Avoid artificial UV radiation sources
    - **Regular Checks:** Perform monthly self-examinations
    - **Professional Screenings:** Get annual skin checks from a dermatologist, especially if high-risk
    """)
    
    # About the technology
    st.markdown("""
    ## Technology Behind SkinScan
    
    SkinScan utilizes a deep convolutional neural network (CNN) trained on thousands of labeled dermatological images. 
    The model has been validated against established datasets and continues to learn with each new analysis.
    
    ### Our Model
    
    - **Architecture:** EfficientNet/ResNet with custom classification layers
    - **Training Data:** Combined datasets including HAM10000, ISIC Archive, and PH2 Dataset
    - **Validation:** Cross-validated with dermatologist-confirmed diagnoses
    - **Accuracy:** Approximately 85-90% accuracy on validation data
    
    ### How It Works
    
    1. **Image Upload:** Healthcare provider uploads a clear image of the skin lesion
    2. **Preprocessing:** Images are standardized for analysis
    3. **AI Analysis:** Our model processes the image and generates predictions
    4. **Results:** Predictions are displayed with confidence levels and recommendations
    5. **Follow-up:** Results can be saved to patient records for tracking
    """)
    
    # Team information
    st.markdown("""
    ## Our Team
    
    SkinScan was developed by a multidisciplinary team of medical professionals, data scientists, and software engineers 
    dedicated to improving early detection of skin cancer.
    
    For more information or to contact the team, please email info@skinscan-app.com
    """)
    
    # References section
    st.markdown("""
    ## References and Further Reading
    
    1. American Academy of Dermatology. (2021). Skin cancer.
    2. Skin Cancer Foundation. (2021). Skin cancer information.
    3. World Health Organization. (2020). Skin cancers.
    4. Esteva, A., et al. (2017). Dermatologist-level classification of skin cancer with deep neural networks. Nature, 542(7639), 115-118.
    5. Codella, N.C., et al. (2018). Skin lesion analysis toward melanoma detection: A challenge at the 2017 International symposium on biomedical imaging (ISBI). In 2018 IEEE 15th International Symposium on Biomedical Imaging (ISBI 2018) (pp. 168-172).
    """)

if __name__ == "__main__":
    show()