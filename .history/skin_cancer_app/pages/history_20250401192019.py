import streamlit as st
import pandas as pd
from utils.model_handler import SkinCancerModel
from utils.db_manager import get_all_detection_history

def show():
    """Display the detection history page"""
    st.markdown("<h1 style='text-align: center;'>Detection History</h1>", unsafe_allow_html=True)
    
    # Fetch detection history from the database
    history = get_all_detection_history()  # Now properly imported
    
    if not history:
        st.info("No detection history available.")
        return
    
    display_all_history(history)

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
    col1, col2 = st.columns(2)
    with col1:
        risk_filter = st.multiselect("Filter by Risk Level", 
                                     options=["Low", "Medium", "High", "Very High"],
                                     default=[])
    with col2:
        diagnosis_filter = st.multiselect("Filter by Diagnosis", 
                                         options=list(set([d['Diagnosis'] for d in history_data])),
                                         default=[])
    
    # Apply filters
    filtered_df = df
    if risk_filter:
        filtered_df = filtered_df[filtered_df['Risk'].isin(risk_filter)]
    if diagnosis_filter:
        filtered_df = filtered_df[filtered_df['Diagnosis'].isin(diagnosis_filter)]
    
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
    </style>
    """, unsafe_allow_html=True)

# Call the CSS initializer
init_css()