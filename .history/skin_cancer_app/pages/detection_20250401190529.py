import streamlit as st
import os
import time
import numpy as np
from PIL import Image
from datetime import datetime
import matplotlib.pyplot as plt
import io
import base64
import random

# Define skin cancer classes and information
SKIN_CLASSES = {
    "melanoma": "Melanoma",
    "basal_cell_carcinoma": "Basal Cell Carcinoma",
    "squamous_cell_carcinoma": "Squamous Cell Carcinoma",
    "actinic_keratosis": "Actinic Keratosis",
    "nevus": "Benign Nevus (Mole)",
    "seborrheic_keratosis": "Seborrheic Keratosis",
    "dermatofibroma": "Dermatofibroma"
}

CLASS_INFO = {
    "melanoma": {
        "risk_level": "High",
        "description": "Melanoma is the most dangerous form of skin cancer. It develops in melanocytes, the cells that produce melanin. Melanomas often resemble moles and some develop from moles.",
        "recommendation": "Immediate referral to a dermatologist for biopsy and treatment planning. Melanoma can be life-threatening if not treated early."
    },
    "basal_cell_carcinoma": {
        "risk_level": "Medium",
        "description": "Basal cell carcinoma is the most common form of skin cancer. It rarely spreads to other parts of the body but can be locally destructive if not treated.",
        "recommendation": "Referral to a dermatologist for removal. Various treatment options include surgical excision, Mohs surgery, or topical medications."
    },
    "squamous_cell_carcinoma": {
        "risk_level": "Medium-High",
        "description": "Squamous cell carcinoma is the second most common form of skin cancer. It's more likely to spread than basal cell carcinoma but still has a good prognosis when caught early.",
        "recommendation": "Prompt referral to a dermatologist for biopsy and treatment. May require excision, radiation therapy, or topical treatments."
    },
    "actinic_keratosis": {
        "risk_level": "Medium-Low",
        "description": "Actinic keratosis is a precancerous lesion that may develop into squamous cell carcinoma if left untreated. It appears as a rough, scaly patch on skin frequently exposed to the sun.",
        "recommendation": "Dermatologist evaluation within 1-2 months. Treatment options include cryotherapy, topical medications, or photodynamic therapy."
    },
    "nevus": {
        "risk_level": "Low",
        "description": "A benign nevus (mole) is a common growth on the skin that develops when pigment cells grow in clusters. Most are harmless, but some may develop into melanoma.",
        "recommendation": "Regular self-monitoring for changes in size, shape, color, or symptoms. Follow up with dermatologist during regular skin checks."
    },
    "seborrheic_keratosis": {
        "risk_level": "Low",
        "description": "Seborrheic keratosis is a benign skin growth that appears as a waxy, scaly, slightly raised growth. They are very common and not cancerous.",
        "recommendation": "No treatment necessary unless for cosmetic reasons or if the lesion becomes irritated. Can be removed by freezing, curettage, or laser therapy if desired."
    },
    "dermatofibroma": {
        "risk_level": "Low",
        "description": "Dermatofibroma is a common benign skin growth that often appears as a small, firm bump. They are usually asymptomatic and harmless.",
        "recommendation": "No treatment necessary. Can be monitored for changes. Removal is an option if the lesion is bothersome or for cosmetic reasons."
    }
}

class RandomSkinCancerModel:
    """A mock model that randomly predicts skin cancer types"""

    def predict(self, image_path):
        """Simulate prediction with random values"""
        # List of possible classes
        classes = list(SKIN_CLASSES.keys())

        # Randomly select a class with weighted probabilities
        # Make benign conditions slightly more likely
        weights = [0.1, 0.1, 0.1, 0.15, 0.2, 0.2, 0.15]  # Sum = 1.0
        predicted_class = random.choices(classes, weights=weights, k=1)[0]

        # Generate a confidence score between 0.7 and 0.98
        confidence = random.uniform(0.7, 0.98)

        # Simulate processing time to make it feel realistic
        time.sleep(2)

        return predicted_class, confidence

    def get_class_info(self, class_name):
        """Return information about the given class"""
        return {
            "name": SKIN_CLASSES[class_name],
            "info": CLASS_INFO[class_name]
        }

def get_image_features(image_path):
    """Generate random image features for display"""
    # Random feature values that seem plausible
    return {
        "area": random.randint(10000, 50000),
        "perimeter": random.uniform(300, 1200),
        "circularity": random.uniform(0.5, 0.95),
        "asymmetry": random.uniform(0.1, 0.5)
    }

def create_analysis_plots(image_path):
    """Create a visualization of the image analysis"""
    # Create a figure with 2x2 subplots
    fig, axes = plt.subplots(2, 2, figsize=(8, 8))

    # Load the original image
    img = Image.open(image_path)
    img_array = np.array(img)

    # Plot original image
    axes[0, 0].imshow(img_array)
    axes[0, 0].set_title("Original Image")
    axes[0, 0].axis("off")

    # Create a simulated segmented image (grayscale version with threshold)
    try:
        gray_img = np.mean(img_array, axis=2).astype(np.uint8)
    except:
        # Handle grayscale images
        gray_img = img_array.astype(np.uint8)

    # Apply random threshold
    threshold = random.randint(100, 150)
    binary_img = (gray_img > threshold).astype(np.uint8) * 255

    # Plot segmented image
    axes[0, 1].imshow(binary_img, cmap='gray')
    axes[0, 1].set_title("Lesion Segmentation")
    axes[0, 1].axis("off")

    # Plot a heatmap (random data)
    heatmap_data = np.random.rand(img_array.shape[0], img_array.shape[1])
    axes[1, 0].imshow(heatmap_data, cmap='hot')
    axes[1, 0].set_title("Feature Heatmap")
    axes[1, 0].axis("off")

    # Plot a feature histogram
    feature_values = np.random.normal(0.5, 0.15, 1000)
    axes[1, 1].hist(feature_values, bins=20, color='skyblue', edgecolor='black')
    axes[1, 1].set_title("Feature Distribution")
    axes[1, 1].set_xlabel("Feature Value")
    axes[1, 1].set_ylabel("Frequency")

    plt.tight_layout()

    # Convert plot to image
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)

    # Encode to base64 for Streamlit
    data = base64.b64encode(buf.read()).decode('utf-8')
    return f"data:image/png;base64,{data}"

def save_detection_result(patient_id, image_path, prediction, confidence, location, notes):
    """Mock function to save detection results"""
    # Generate a random ID for the record
    result_id = f"RES{random.randint(10000, 99999)}"

    # In a real implementation, this would save to a database
    # For now, just return the ID to simulate saving
    return result_id

def create_confidence_chart(predicted_class, confidence):
    """Create a confidence chart for all classes"""
    # All possible classes
    classes = list(SKIN_CLASSES.keys())

    # Generate random confidence values for other classes
    confidence_values = []
    remaining = 1.0 - confidence

    for cls in classes:
        if cls == predicted_class:
            confidence_values.append(confidence)
        else:
            # Assign random portion of remaining confidence
            if len(confidence_values) < len(classes) - 1:
                random_conf = random.uniform(0.01, remaining * 0.8)
                confidence_values.append(random_conf)
                remaining -= random_conf
            else:
                # Last class gets what's left
                confidence_values.append(remaining)

    # Create the chart
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(
        [SKIN_CLASSES[c] for c in classes],
        confidence_values,
        color=['#3498DB' if c == predicted_class else '#AED6F1' for c in classes]
    )

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

def get_result_class(risk_level):
    """Return the appropriate CSS class based on risk level"""
    if risk_level == "High":
        return "result-positive"
    elif risk_level == "Medium-High" or risk_level == "Medium":
        return "result-positive"
    else:
        return "result-negative"

def show():
    """Display the skin cancer detection page"""
    st.markdown("<h1 style='text-align: center;'>Skin Cancer Detection</h1>", unsafe_allow_html=True)

    # Check if a patient is selected
    if st.session_state.patient_id is None:
        st.warning("No patient selected. Please register or select a patient first.")
        with st.form(key="go_to_patient_form"):
            if st.form_submit_button("Go to Patient Information"):
                st.session_state['page'] = "Patient Information"
                st.rerun()
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
                st.image(image, caption="Uploaded Image", use_container_width=True)

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

                with st.form(key="analyze_form"):
                    if st.form_submit_button("Analyze Image"):
                        with st.spinner("Analyzing image..."):
                            # Simulate model loading time
                            progress_bar = st.progress(0)
                            for i in range(100):
                                time.sleep(0.02)
                                progress_bar.progress(i + 1)

                            # Create model instance
                            model = RandomSkinCancerModel()

                            # Predict
                            predicted_class, confidence = model.predict(st.session_state.uploaded_image)

                            # Save results to session state
                            st.session_state.prediction_result = predicted_class
                            st.session_state.confidence = confidence
                            st.session_state.analysis_complete = True

                            # Switch to the Analysis Results tab
                            time.sleep(0.5)
                            st.rerun()

    with tab2:
        if st.session_state.analysis_complete and st.session_state.prediction_result:
            st.subheader("Analysis Results")

            # Get class information
            model = RandomSkinCancerModel()
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
            with st.form(key="save_results_form"):
                if st.form_submit_button("Save Results"):
                    st.rerun()
        else:
            st.info("No analysis results yet. Please upload and analyze an image first.")

    with tab3:
        if st.session_state.analysis_complete and st.session_state.prediction_result:
            st.subheader("Save Results & Generate Report")

            # Display summary
            model = RandomSkinCancerModel()
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
            with st.form(key="save_to_patient_record_form"):
                if st.form_submit_button("Save to Patient Record"):
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
                        if st.button("View Patient History"):
                            st.session_state['page'] = "History"
                            st.rerun()

                        # Reset for new analysis
                        if st.button("New Analysis"):
                            st.session_state.uploaded_image = None
                            st.session_state.analysis_complete = False
                            st.session_state.prediction_result = None
                            st.session_state.confidence = None
                            st.session_state.lesion_location = ""
                            st.session_state.notes = ""
                            st.rerun()
        else:
            st.info("No analysis results yet. Please upload and analyze an image first.")