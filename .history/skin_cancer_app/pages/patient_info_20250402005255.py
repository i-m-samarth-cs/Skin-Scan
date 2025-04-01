import streamlit as st
from utils.db_manager import add_patient, get_patient, get_all_patients

def show():
    """Display the patient information page"""
    st.markdown("<h1 style='text-align: center;'>Patient Information</h1>", unsafe_allow_html=True)

    # Create tabs for patient registration and selection
    tab1, tab2 = st.tabs(["Register New Patient", "Select Existing Patient"])

    with tab1:
        st.subheader("Register New Patient")

        # Patient registration form
        with st.form("patient_registration_form", clear_on_submit=True):
            st.markdown("""
            <div class="info-panel">
                <p>Fill in the patient details below. Fields marked with * are required.</p>
            </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns(2)

            with col1:
                name = st.text_input("Full Name *")
                age = st.number_input("Age *", min_value=0, max_value=120, step=1)
                gender = st.selectbox("Gender *", ["Select gender", "Male", "Female", "Other", "Prefer not to say"])

            with col2:
                contact = st.text_input("Contact Number")
                address = st.text_area("Address", height=100)

            # Medical history
            medical_history = st.text_area("Medical History", height=150,
                                        placeholder="Include relevant information such as:\n- Previous skin conditions\n- Family history of skin cancer\n- Sun exposure history\n- Previous treatments")

            # Consent checkbox
            consent = st.checkbox("I confirm that the patient has consented to store their information and images for diagnostic purposes.")

            # Submit button
            submitted = st.form_submit_button("Register Patient")

            if submitted:
                # Validate inputs
                if not name or age <= 0 or gender == "Select gender":
                    st.error("Please fill in all required fields.")
                elif not consent:
                    st.error("Please confirm patient consent before registration.")
                else:
                    # Add patient to database
                    patient_id = add_patient(name, age, gender, contact, address, medical_history)

                    # Success message
                    st.success(f"Patient registered successfully! Patient ID: {patient_id}")

                    # Set as current patient
                    st.session_state.patient_id = patient_id
                    st.session_state['registered_new_patient'] = True

        # Navigate to detection outside of form
        if st.session_state.get('registered_new_patient', False):
            with st.form(key="proceed_to_detection_form"):
                if st.form_submit_button("Proceed to Skin Cancer Detection"):
                    st.session_state['page'] = "Skin Cancer Detection"
                    st.session_state['registered_new_patient'] = False
                    st.rerun()

    with tab2:
        st.subheader("Select Existing Patient")

        # Get all patients
        patients = get_all_patients()

        if not patients:
            st.info("No patients registered yet. Please register a new patient.")
        else:
            # Search functionality
            search_query = st.text_input("Search patients by name")

            # Filter patients based on search query
            if search_query:
                filtered_patients = [p for p in patients if search_query.lower() in p['name'].lower()]
            else:
                filtered_patients = patients

            # Display patients as cards
            st.markdown(f"Found {len(filtered_patients)} patients")

            for i, patient in enumerate(filtered_patients):
                with st.form(f"select_patient_form_{i}"):
                    col1, col2, col3 = st.columns([3, 2, 1])

                    with col1:
                        st.markdown(f"""
                        <div class="card">
                            <h3>{patient['name']}</h3>
                            <p><strong>ID:</strong> {patient['id']}</p>
                            <p><strong>Age:</strong> {patient['age']} | <strong>Gender:</strong> {patient['gender']}</p>
                        </div>
                        """, unsafe_allow_html=True)

                    with col2:
                        st.markdown(f"""
                        <div class="info-panel">
                            <p><strong>Contact:</strong> {patient['contact'] or 'N/A'}</p>
                            <p><strong>Registered:</strong> {patient['created_at']}</p>
                        </div>
                        """, unsafe_allow_html=True)

                    with col3:
                        select_button = st.form_submit_button("Select")
                        view_details_button = st.form_submit_button("View Details")
                    
                    if select_button:
                        st.session_state.patient_id = patient['id']
                        st.success(f"Selected patient: {patient['name']}")
                        st.session_state['selected_existing_patient'] = True

                    if view_details_button:
                        st.session_state['view_patient_id'] = patient['id']
                        st.rerun()

            # Navigation to detection after selecting a patient
            if st.session_state.get('selected_existing_patient', False):
                with st.form(key="go_to_detection_form"):
                    if st.form_submit_button("Go to Detection"):
                        st.session_state['page'] = "Skin Cancer Detection"
                        st.session_state['selected_existing_patient'] = False
                        st.rerun()

            # Display patient details if a patient is selected for viewing
            if 'view_patient_id' in st.session_state and st.session_state['view_patient_id']:
                patient = get_patient(st.session_state['view_patient_id'])

                if patient:
                    st.markdown("<hr>", unsafe_allow_html=True)
                    st.subheader(f"Patient Details: {patient['name']}")

                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown(f"""
                        <div class="card">
                            <h3>Personal Information</h3>
                            <p><strong>Patient ID:</strong> {patient['id']}</p>
                            <p><strong>Full Name:</strong> {patient['name']}</p>
                            <p><strong>Age:</strong> {patient['age']}</p>
                            <p><strong>Gender:</strong> {patient['gender']}</p>
                            <p><strong>Contact:</strong> {patient['contact'] or 'N/A'}</p>
                            <p><strong>Address:</strong> {patient['address'] or 'N/A'}</p>
                        </div>
                        """, unsafe_allow_html=True)

                    with col2:
                        st.markdown(f"""
                        <div class="card">
                            <h3>Medical History</h3>
                            <p>{patient['medical_history'] or 'No medical history recorded.'}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Patient detail actions - using separate forms for each action
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        with st.form(key="select_viewed_patient_form"):
                            if st.form_submit_button("Select This Patient"):
                                st.session_state.patient_id = patient['id']
                                st.session_state.pop('view_patient_id', None)
                                st.success(f"Selected patient: {patient['name']}")
                                st.session_state['selected_existing_patient'] = True
                                st.rerun()
                    
                    with col2:
                        with st.form(key="go_to_detection_with_viewed_patient_form"):
                            if st.form_submit_button("Go to Detection"):
                                st.session_state.patient_id = patient['id']
                                st.session_state.pop('view_patient_id', None)
                                st.session_state['page'] = "Skin Cancer Detection"
                                st.rerun()
                    
                    with col3:
                        with st.form(key="close_viewed_patient_details_form"):
                            if st.form_submit_button("Close Details"):
                                st.session_state.pop('view_patient_id', None)
                                st.rerun()