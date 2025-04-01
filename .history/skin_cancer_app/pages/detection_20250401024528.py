import streamlit as st
import os
import time
import cv2
import numpy as np
from PIL import Image
from datetime import datetime
from utils.model_handler import SkinCancerModel, SKIN_CLASSES, CLASS_INFO
from utils.image_processor import enhance_image, segment_lesion, get_image_features, create_analysis_plots
from utils.db_manager import save_detection_result
import matplotlib.pyplot as plt
import io
import base64

def show():
    """Display the skin cancer detection page"""
    st.markdown("<h1 style='text-align: center;'>Skin Cancer Detection</h1>", unsafe_allow_html=True)
    
    # Check if a patient is selected
    if st.session_state.patient_id is None:
        st.warning("No patient selected. Please register or select a patient first.")
        if st.form_submit_button("Go to Patient Information"):
            st.session_state['page'] = "Patient Information"
            st.experimental_rerun()
        return
    
    # Initialize session states
    if 'uploaded_image' not in st.session_state:
        st.session_state.uploaded_image = None
    if 'analysis_complete' not in st.session_state:
        st.session_state.analysis_complete = False
    if 'prediction_result' not in st.session_state:
        st.session_state.prediction_result = None
    if 'confidence' not in st.session_state:
        st.session_state.confidence = None
    if 'lesion_location' not in st.session_state:
        st.session_state.lesion_location = ""
    if 'notes' not in st.session_state:
        st.session_state.notes = ""
    
    # Create tabs for different stages
    tab1, tab2, tab3 = st.tabs(["Upload Image", "Analysis Results", "Save & Report"])
    
    with tab1:
        st.subheader("Upload Skin Lesion Image")
        
        # Instructions
        st.markdown("""
        <div class="info-panel">
            <h3>📸 Image Guidelines:</h3>
            <ul>
                <li>Use good lighting to capture clear details</li>
                <li>Focus directly on the skin lesion</li>
                <li>Include some surrounding normal skin for contrast</li>
                <li>Use a ruler or coin for size reference if possible</li>
                <li>Avoid shadows or glare</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Upload image section
        uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])
        
        col1, col2 = st.columns(2)
        
        with col1:
            if uploaded_file is not None:
                # Create directory if it doesn't exist
                os.makedirs("data/uploaded_images", exist_ok=True)
                
                # Save the uploaded file
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                file_path = f"data/uploaded_images/{timestamp}_{uploaded_file.name}"
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Display the uploaded image
                image = Image.open(uploaded_file)
                st.image(image, caption="Uploaded Image", use_column_width=True)
                
                # Save to session state
                st.session_state.uploaded_image = file_path
                
                # Lesion location input
                st.session_state.lesion_location = st.selectbox(
                    "Lesion Location",
                    ["Select location", "Face", "Scalp", "Ear", "Neck", "Chest", "Back", 
                     "Abdomen", "Trunk", "Upper Extremity", "Lower Extremity", "Hand", "Foot", "Other"]
                )
                
                # Notes input
                st.session_state.notes = st.text_area("Additional Notes", height=100)
        
        with col2:
            if st.session_state.uploaded_image:
                st.markdown("""
                <div class="card">
                    <h3>Ready for Analysis</h3>
                    <p>Click the button below to analyze the uploaded image for skin cancer detection.</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.form_submit_button("Analyze Image", key="analyze_btn", type="primary"):
                    with st.spinner("Analyzing image..."):
                        # Simulate model loading time
                        progress_bar = st.progress(0)
                        for i in range(100):
                            time.sleep(0.02)
                            progress_bar.progress(i + 1)
                        
                        # Create model instance
                        model = SkinCancerModel()
                        
                        # Predict
                        predicted_class, confidence = model.predict(st.session_state.uploaded_image)
                        
                        # Save results to session state
                        st.session_state.prediction_result = predicted_class
                        st.session_state.confidence = confidence
                        st.session_state.analysis_complete = True
                        
                        # Switch to the Analysis Results tab
                        time.sleep(0.5)
                        st.experimental_rerun()
    
    with tab2:
        if st.session_state.analysis_complete and st.session_state.prediction_result:
            st.subheader("Analysis Results")
            
            # Get class information
            model = SkinCancerModel()
            class_info = model.get_class_info(st.session_state.prediction_result)
            
            # Display results in a nice format
            col1, col2 = st.columns([3, 2])
            
            with col1:
                st.markdown(f"""
                <div class="card">
                    <h2>Diagnosis Result</h2>
                    <h3>{class_info['name']}</h3>
                    <p><strong>Confidence:</strong> {st.session_state.confidence * 100:.1f}%</p>
                    <p><strong>Risk Level:</strong> {class_info['info']['risk_level']}</p>
                    <hr>
                    <p>{class_info['info']['description']}</p>
                    <div class="{get_result_class(class_info['info']['risk_level'])}">
                        <h4>Recommendation:</h4>
                        <p>{class_info['info']['recommendation']}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Create visualization of confidence for all classes
                st.markdown("<h3>Confidence Levels</h3>", unsafe_allow_html=True)
                confidence_chart = create_confidence_chart(st.session_state.prediction_result, st.session_state.confidence)
                st.markdown(f'<img src="{confidence_chart}" width="100%"/>', unsafe_allow_html=True)
            
            with col2:
                if st.session_state.uploaded_image:
                    # Display analysis images
                    analysis_plots = create_analysis_plots(st.session_state.uploaded_image)
                    st.markdown(f'<img src="{analysis_plots}" width="100%"/>', unsafe_allow_html=True)
                    
                    # Display extracted features
                    features = get_image_features(st.session_state.uploaded_image)
                    st.markdown("<h3>Image Analysis</h3>", unsafe_allow_html=True)
                    st.markdown(f"""
                    <div class="info-panel">
                        <p><strong>Lesion Area:</strong> {features['area']} pixels</p>
                        <p><strong>Perimeter:</strong> {features['perimeter']:.1f} pixels</p>
                        <p><strong>Circularity:</strong> {features['circularity']:.3f}</p>
                        <p><strong>Asymmetry Factor:</strong> {features['asymmetry']:.3f}</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Button to move to save tab
            if st.form_submit_button("Save Results", key="save_results_btn", type="primary"):
                st.experimental_rerun()
        else:
            st.info("No analysis results yet. Please upload and analyze an image first.")
    
    with tab3:
        if st.session_state.analysis_complete and st.session_state.prediction_result:
            st.subheader("Save Results & Generate Report")
            
            # Display summary
            model = SkinCancerModel()
            class_info = model.get_class_info(st.session_state.prediction_result)
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                if st.session_state.uploaded_image:
                    st.image(st.session_state.uploaded_image, caption="Analyzed Image", width=300)
            
            with col2:
                st.markdown(f"""
                <div class="card">
                    <h3>Result Summary</h3>
                    <p><strong>Diagnosis:</strong> {class_info['name']}</p>
                    <p><strong>Confidence:</strong> {st.session_state.confidence * 100:.1f}%</p>
                    <p><strong>Risk Level:</strong> {class_info['info']['risk_level']}</p>
                    <p><strong>Location:</strong> {st.session_state.lesion_location}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Additional notes section
            notes = st.text_area("Additional Notes for Report", st.session_state.notes, height=100)
            
            # Save button
            if st.form_submit_button("Save to Patient Record", key="final_save_btn", type="primary"):
                with st.spinner("Saving results..."):
                    # Save to database
                    result_id = save_detection_result(
                        st.session_state.patient_id,
                        st.session_state.uploaded_image,
                        st.session_state.prediction_result,
                        st.session_state.confidence,
                        st.session_state.lesion_location,
                        notes
                    )
                    
                    # Success message
                    st.success(f"Results saved successfully! Record ID: {result_id}")
                    
                    # Option to view history
                    if st.form_submit_button("View Patient History"):
                        st.session_state['page'] = "History"
                        st.experimental_rerun()
                    
                    # Reset for new analysis
                    if st.form_submit_button("New Analysis"):
                        st.session_state.uploaded_image = None
                        st.session_state.analysis_complete = False
                        st.session_state.prediction_result = None
                        st.session_state.confidence = None
                        st.session_state.lesion_location = ""
                        st.session_state.notes = ""
                        st.experimental_rerun()
        else:
            st.info("No analysis results yet. Please upload and analyze an image first.")

def get_result_class(risk_level):
    """Return the appropriate CSS class based on risk level"""
    if risk_level == "High":
        return "result-positive"
    elif risk_level == "Medium-High" or risk_level == "Medium":
        return "result-positive"
    else:
        return "result-negative"

def create_confidence_chart(predicted_class, confidence):
    """Create a confidence chart for all classes"""
    # Sample confidence values (would be replaced by actual model output)
    classes = list(SKIN_CLASSES.keys())
    confidence_values = [0.1, 0.05, 0.02, 0.03, 0.05, 0.02, 0.02]
    
    # Set the predicted class to have the actual confidence
    predicted_index = classes.index(predicted_class)
    confidence_values[predicted_index] = confidence
    
    # Normalize others to make sure sum is 1.0
    total = sum(confidence_values)
    if total > 1.0:
        for i in range(len(confidence_values)):
            if i != predicted_index:
                confidence_values[i] *= (1.0 - confidence) / (total - confidence)
    
    # Create the chart
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh([SKIN_CLASSES[c] for c in classes], confidence_values, color=['#3498DB' if c == predicted_class else '#AED6F1' for c in classes])
    
    # Add data labels
    for i, bar in enumerate(bars):
        width = bar.get_width()
        label_x_pos = width + 0.01
        ax.text(label_x_pos, bar.get_y() + bar.get_height()/2, f'{width:.1%}',
                va='center')
    
    ax.set_xlim(0, 1.0)
    ax.set_xlabel('Confidence')
    ax.set_title('Diagnosis Confidence Levels')
    plt.tight_layout()
    
    # Convert plot to image
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    
    # Encode to base64 for Streamlit
    data = base64.b64encode(buf.read()).decode('utf-8')
    return f"data:image/png;base64,{data}"