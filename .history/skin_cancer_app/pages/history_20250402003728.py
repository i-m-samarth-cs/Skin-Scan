import streamlit as st
import pandas as pd
from utils.model_handler import SkinCancerModel
from utils.db_manager import get_all_detection_history, get_patient_detection_history, get_all_patients, get_patient

def show():
    """Display the detection history page"""
    st.markdown("<h1 style='text-align: center;'>Detection History</h1>", unsafe_allow_html=True)
    
    # Initialize CSS for styling
    init_css()
    
    # Option to view all history or filter by patient
    view_mode = st.radio("View mode:", ["All Patients", "Single Patient"])
    
    if view_mode == "All Patients":
        # Fetch all detection history from the database
        history = get_all_detection_history()
        if not history:
            st.info("No detection history available.")
            return
        
        display_all_history(history)
    else:
        # Get list of patients for selection
        patients = get_all_patients()
        if not patients:
            st.info("No patients available in the system.")
            return
        
        # Create a list of patient options
        patient_options = [(p['id'], f"{p['name']} (ID: {p['id']})") for p in patients]
        
        # Patient selection
        selected_patient_id = st.selectbox(
            "Select Patient:",
            options=[p[0] for p in patient_options],
            format_func=lambda x: next((p[1] for p in patient_options if p[0] == x), f"Patient {x}")
        )
        
        # Get patient details
        patient = get_patient(selected_patient_id)
        
        # Display patient info card
        if patient:
            st.markdown(f"""
            <div class="patient-card">
                <h3>{patient['name']}</h3>
                <p><strong>Age:</strong> {patient['age']}</p>
                <p><strong>Gender:</strong> {patient['gender']}</p>
                <p><strong>Contact:</strong> {patient['contact']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Fetch patient-specific history
        patient_history = get_patient_detection_history(selected_patient_id)
        
        if not patient_history:
            st.info(f"No detection history available for this patient.")
            return
        
        st.subheader(f"Detection History")
        display_patient_history(patient_history)

def display_patient_history(history):
    """Display detection history for a specific patient"""
    model = SkinCancerModel()
    
    # Create a DataFrame for better display
    history_data = []
    for record in history:
        class_info = model.get_class_info(record['diagnosis'])
        history_data.append({
            'ID': record['id'],
            'Diagnosis': class_info['name'],
            'Confidence': f"{record['confidence'] * 100:.1f}%",
            'Risk': class_info['info']['risk_level'],
            'Location': record['lesion_location'],
            'Date': record['created_at'],
            'Notes': record['notes'] if record['notes'] else "N/A"
        })
    
    # Convert to DataFrame
    df = pd.DataFrame(history_data)
    
    # Add filtering options
    risk_filter = st.multiselect("Filter by Risk Level", 
                               options=["Low", "Medium", "High", "Very High"],
                               default=[])
    
    # Apply filters
    filtered_df = df
    if risk_filter:
        filtered_df = filtered_df[filtered_df['Risk'].isin(risk_filter)]
    
    # Display table
    if not filtered_df.empty:
        st.dataframe(filtered_df, use_container_width=True)
        
        # Allow detailed view of selected record
        selected_id = st.selectbox("Select record to view details", 
                                 options=filtered_df['ID'].tolist(),
                                 format_func=lambda x: f"Record {x} - {filtered_df[filtered_df['ID'] == x]['Date'].values[0]}")
        
        if selected_id:
            record = next((r for r in history if r['id'] == selected_id), None)
            if record:
                st.subheader(f"Test Details (ID: {selected_id})")
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    try:
                        st.image(record['image_path'], caption="Analyzed Image", width=200)
                    except:
                        st.error("Image not found")
                
                with col2:
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
    else:
        st.info("No records match the selected filters.")

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
    
    # Convert to DataFrame
    df = pd.DataFrame(history_data)
    
    # Add filtering options
    col1, col2, col3 = st.columns(3)
    with col1:
        risk_filter = st.multiselect("Filter by Risk Level", 
                                   options=["Low", "Medium", "High", "Very High"],
                                   default=[])
    with col2:
        diagnosis_filter = st.multiselect("Filter by Diagnosis", 
                                        options=list(set([d['Diagnosis'] for d in history_data])),
                                        default=[])
    with col3:
        patient_filter = st.multiselect("Filter by Patient", 
                                      options=list(set([d['Patient'] for d in history_data])),
                                      default=[])
    
    # Apply filters
    filtered_df = df
    if risk_filter:
        filtered_df = filtered_df[filtered_df['Risk'].isin(risk_filter)]
    if diagnosis_filter:
        filtered_df = filtered_df[filtered_df['Diagnosis'].isin(diagnosis_filter)]
    if patient_filter:
        filtered_df = filtered_df[filtered_df['Patient'].isin(patient_filter)]
    
    # Display table
    if not filtered_df.empty:
        st.dataframe(filtered_df, use_container_width=True)
        
        # Allow detailed view of selected record
        selected_id = st.selectbox("Select record to view details", 
                                 options=filtered_df['ID'].tolist(),
                                 format_func=lambda x: f"Record {x} - {filtered_df[filtered_df['ID'] == x]['Patient'].values[0]}")
        
        if selected_id:
            record = next((r for r in history if r['id'] == selected_id), None)
            if record:
                st.subheader(f"Details for {filtered_df[filtered_df['ID'] == selected_id]['Patient'].values[0]}")
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    try:
                        st.image(record['image_path'], caption="Analyzed Image", width=200)
                    except:
                        st.error("Image not found")
                
                with col2:
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
    else:
        st.info("No records match the selected filters.")

def get_result_class(risk_level):
    """Return CSS class based on risk level"""
    if risk_level == "Low":
        return "result-low"
    elif risk_level == "Medium":
        return "result-medium"
    elif risk_level == "High":
        return "result-high"
    elif risk_level == "Very High":
        return "result-very-high"
    else:
        return "result-unknown"

# Initialize CSS for styling
def init_css():
    st.markdown("""
    <style>
        .card {
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 10px;
            background-color: #f8f9fa;
        }
        .info-panel {
            padding: 10px;
            border-radius: 5px;
            margin-top: 10px;
            background-color: #e9ecef;
        }
        .result-low {
            padding: 10px;
            border-radius: 5px;
            background-color: #d4edda;
            margin-top: 10px;
        }
        .result-medium {
            padding: 10px;
            border-radius: 5px;
            background-color: #fff3cd;
            margin-top: 10px;
        }
        .result-high {
            padding: 10px;
            border-radius: 5px;
            background-color: #f8d7da;
            margin-top: 10px;
        }
        .result-very-high {
            padding: 10px;
            border-radius: 5px;
            background-color: #721c24;
            color: white;
            margin-top: 10px;
        }
        .result-unknown {
            padding: 10px;
            border-radius: 5px;
            background-color: #e9ecef;
            margin-top: 10px;
        }
        .patient-card {
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
            background-color: #e3f2fd;
            border-left: 4px solid #0d6efd;
        }
    </style>
    """, unsafe_allow_html=True)