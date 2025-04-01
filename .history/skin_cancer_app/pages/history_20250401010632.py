import streamlit as st
import pandas as pd
from utils.db_manager import get_patient_detection_history, get_all_detection_history, get_patient
from utils.model_handler import SkinCancerModel, SKIN_CLASSES

def show():
    """Display the detection history page"""
    st.markdown("<h1 style='text-align: center;'>Detection History</h1>", unsafe_allow_html=True)
    
    # Create tabs for current patient and all patients
    tab1, tab2 = st.tabs(["Current Patient", "All Patients"])
    
    with tab1:
        # Check if a patient is selected
        if st.session_state.patient_id is None:
            st.warning("No patient selected. Please register or select a patient first.")
            if st.button("Go to Patient Information"):
                st.session_state['page'] = "Patient Information"
                st.experimental_rerun()
        else:
            # Get patient info
            patient = get_patient(st.session_state.patient_id)
            if patient:
                st.subheader(f"Detection History for {patient['name']}")
                
                # Get patient history
                history = get_patient_detection_history(st.session_state.patient_id)
                
                if not history:
                    st.info("No detection history found for this patient.")
                    if st.button("Go to Detection"):
                        st.session_state['page'] = "Skin Cancer Detection"
                        st.experimental_rerun()
                else:
                    # Display history
                    display_history(history)
    
    with tab2:
        st.subheader("All Patients Detection History")
        
        # Get all history
        all_history = get_all_detection_history()
        
        if not all_history:
            st.info("No detection history found.")
        else:
            # Add search/filter functionality
            search_query = st.text_input("Search by patient name or diagnosis")
            
            # Filter history based on search query
            if search_query:
                filtered_history = [h for h in all_history if (
                    search_query.lower() in h['patient_name'].lower() if h['patient_name'] else False) or 
                    search_query.lower() in SKIN_CLASSES.get(h['diagnosis'], "").lower()
                ]
            else:
                filtered_history = all_history
            
            # Display history
            display_all_history(filtered_history)

def display_history(history):
    """Display detection history for a single patient"""
    model = SkinCancerModel()
    
    # Filter and sort options
    col1, col2 = st.columns([1, 2])
    
    with col1:
        sort_by = st.selectbox("Sort by", ["Most Recent", "Oldest", "Diagnosis"])
    
    # Sort history
    if sort_by == "Most Recent":
        history = sorted(history, key=lambda x: x['created_at'], reverse=True)
    elif sort_by == "Oldest":
        history = sorted(history, key=lambda x: x['created_at'])
    elif sort_by == "Diagnosis":
        history = sorted(history, key=lambda x: SKIN_CLASSES.get(x['diagnosis'], "Unknown"))
    
    # Display history cards
    for i, record in enumerate(history):
        with st.expander(f"Detection #{len(history)-i}: {SKIN_CLASSES.get(record['diagnosis'], 'Unknown')} - {record['created_at']}"):
            col1, col2 = st.columns([1, 2])
            
            with col1:
                try:
                    st.image(record['image_path'], caption="Analyzed Image", width=200)
                except:
                    st.error("Image not found")
            
            with col2:
                # Get class information
                class_info = model.get_class_info(record['diagnosis'])
                
                st.markdown(f"""
                <div class="card">
                    <h3>Diagnosis: {class_info['name']}</h3>
                    <p><strong>Confidence:</strong> {record['confidence'] * 100:.1f}%</p>
                    <p><strong>Risk Level:</strong> {class_info['info']['risk_level']}</p>
                    <p><strong>Location:</strong> {record['lesion_location']}</p>
                    <p><strong>Date:</strong> {record['created_at']}</p>
                </div>
                
                <div class="{get_result_class(class_info['info']['risk_level'])}">
                    <h4>Recommendation:</h4>
                    <p>{class_info['info']['recommendation']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if record['notes']:
                    st.markdown(f"""
                    <div class="info-panel">
                        <h4>Notes:</h4>
                        <p>{record['notes']}</p>
                    </div>
                    """, unsafe_allow_html=True)

def display_all_history(history):
    """Display detection history for all patients"""
    model = SkinCancerModel()
    
    # Create a DataFrame for better display
    history_data = []
    for record in history:
        class_info = model.get_class_info(record['diagnosis'])
        history_data.append({
            'ID': record['id'],
            'Patient': record['patient_name'] if record['patient_name'] else f"Patient {record['patient_id']}",
            'Diagnosis': class_info['name'],
            'Confidence': f"{record['confidence'] * 100:.1f}%",
            'Risk': class_info['info']['risk_level'],
            'Location': record['lesion_location'],
            'Date': record['created_at'],
            'Notes': record['notes'] if record['notes'] else "N/A"
        })
        