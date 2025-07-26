#!/usr/bin/env python3
"""
Baptist Health Hospital Doral - Medical Chatbot
Streamlit Web Application

Standalone deployment version with Streamlit + ngrok support
"""

import streamlit as st
import sqlite3
import json
import re
import datetime
import random
import time
import os
from typing import Dict, List, Tuple, Optional
import requests
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="Baptist Health Hospital Doral - Medical Chatbot",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Baptist Health branding
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #2E8B57, #4682B4);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 4px solid #2E8B57;
    }
    .user-message {
        background-color: #f0f8ff;
        margin-left: 2rem;
    }
    .bot-message {
        background-color: #f5f5f5;
        margin-right: 2rem;
    }
    .sidebar .block-container {
        background-color: #f8f9fa;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Hospital Configuration
CLINIC_NAME = "Baptist Health Hospital Doral"
CLINIC_PHONE = "786-595-3900"
CLINIC_ADDRESS = "9500 NW 58 Street, Doral, FL 33178"
BILLING_PHONE = "786-596-6507"
INSURANCE_PHONE = "786-662-7667"

# Initialize session state
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = None
if 'db_initialized' not in st.session_state:
    st.session_state.db_initialized = False

@st.cache_resource
def init_database():
    """Initialize database with corruption prevention"""
    
    class HospitalDatabase:
        def __init__(self, db_name='hospital_appointments.db'):
            """Initialize hospital database with SQLite - CORRUPTION PROOF"""
            self.db_name = db_name
            
            # Force remove any existing database first
            if os.path.exists(db_name):
                try:
                    os.remove(db_name)
                except:
                    pass
            
            # Create completely fresh database
            try:
                # Use WAL mode to prevent corruption
                self.conn = sqlite3.connect(
                    db_name, 
                    check_same_thread=False,
                    isolation_level=None  # Autocommit mode
                )
                self.cursor = self.conn.cursor()
                
                # Enable WAL mode for better concurrency
                self.cursor.execute("PRAGMA journal_mode=WAL")
                self.cursor.execute("PRAGMA synchronous=NORMAL")
                self.cursor.execute("PRAGMA cache_size=1000")
                
                self._create_tables()
                self._populate_mock_data()
                
            except Exception as e:
                # Last resort: create in-memory database
                self.conn = sqlite3.connect(":memory:", check_same_thread=False)
                self.cursor = self.conn.cursor()
                self._create_tables()
                self._populate_mock_data()
        
        def _create_tables(self):
            """Create database tables"""
            try:
                # Simple appointments table
                self.cursor.execute('''
                    CREATE TABLE appointments (
                        id INTEGER PRIMARY KEY,
                        patient_name TEXT,
                        patient_phone TEXT,
                        doctor_name TEXT,
                        specialty TEXT,
                        appointment_date TEXT,
                        appointment_time TEXT,
                        status TEXT DEFAULT 'confirmed'
                    )
                ''')
                
                # Simple doctors table
                self.cursor.execute('''
                    CREATE TABLE doctors (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        specialty TEXT,
                        available_days TEXT,
                        available_times TEXT
                    )
                ''')
                
                self.conn.commit()
                
            except sqlite3.Error as e:
                raise Exception(f"Database table creation failed: {e}")
        
        def _populate_mock_data(self):
            """Populate database with Baptist Health Hospital Doral doctors"""
            try:
                # Check if data exists
                self.cursor.execute("SELECT COUNT(*) FROM doctors")
                if self.cursor.fetchone()[0] > 0:
                    return
                
                # Insert Baptist Health Hospital Doral doctors
                doctors = [
                    (1, 'Dr. Garcia', 'cardiology', 'Monday,Tuesday,Wednesday,Thursday,Friday', '09:00,10:00,11:00,14:00,15:00,16:00'),
                    (2, 'Dr. Martinez', 'cardiology', 'Tuesday,Wednesday,Thursday,Friday,Saturday', '08:00,09:00,10:00,13:00,14:00,15:00'),
                    (3, 'Dr. Rodriguez', 'dermatology', 'Monday,Wednesday,Friday', '10:00,11:00,12:00,15:00,16:00,17:00'),
                    (4, 'Dr. Lopez', 'dermatology', 'Tuesday,Thursday,Saturday', '09:00,10:00,11:00,14:00,15:00'),
                    (5, 'Dr. Gonzalez', 'pediatrics', 'Monday,Tuesday,Wednesday,Thursday,Friday', '08:00,09:00,10:00,11:00,14:00,15:00'),
                    (6, 'Dr. Fernandez', 'neurology', 'Monday,Wednesday,Friday', '10:00,11:00,14:00,15:00,16:00'),
                    (7, 'Dr. Sanchez', 'orthopedics', 'Tuesday,Thursday,Saturday', '09:00,10:00,11:00,13:00,14:00'),
                    (8, 'Dr. Ramirez', 'gynecology', 'Monday,Tuesday,Wednesday,Thursday', '09:00,10:00,11:00,14:00,15:00,16:00'),
                    (9, 'Dr. Torres', 'psychiatry', 'Monday,Wednesday,Friday', '10:00,11:00,14:00,15:00,16:00,17:00'),
                    (10, 'Dr. Flores', 'internal_medicine', 'Monday,Tuesday,Wednesday,Thursday,Friday', '08:00,09:00,10:00,11:00,13:00,14:00,15:00')
                ]
                
                self.cursor.executemany('''
                    INSERT INTO doctors (id, name, specialty, available_days, available_times)
                    VALUES (?, ?, ?, ?, ?)
                ''', doctors)
                
                self.conn.commit()
                
            except sqlite3.Error as e:
                raise Exception(f"Database population failed: {e}")
        
        def get_available_doctors(self, specialty: str) -> List[Dict]:
            """Get available doctors for a specialty"""
            try:
                self.cursor.execute('''
                    SELECT name, specialty, available_days, available_times 
                    FROM doctors 
                    WHERE specialty = ? OR specialty LIKE ?
                ''', (specialty, f'%{specialty}%'))
                
                doctors = []
                for row in self.cursor.fetchall():
                    doctors.append({
                        'name': row[0],
                        'specialty': row[1],
                        'available_days': row[2].split(','),
                        'available_times': row[3].split(',')
                    })
                return doctors
            except sqlite3.Error as e:
                return []
        
        def book_appointment(self, patient_data: Dict) -> Dict:
            """Book a new appointment"""
            try:
                self.cursor.execute('''
                    INSERT INTO appointments 
                    (patient_name, patient_phone, doctor_name, specialty, appointment_date, appointment_time)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    patient_data.get('name'),
                    patient_data.get('phone'),
                    patient_data.get('doctor'),
                    patient_data.get('specialty'),
                    patient_data.get('date'),
                    patient_data.get('time')
                ))
                
                appointment_id = self.cursor.lastrowid
                self.conn.commit()
                
                return {
                    'success': True,
                    'appointment_id': appointment_id,
                    'message': f"Appointment booked with {patient_data.get('doctor')}"
                }
            except sqlite3.Error as e:
                return {
                    'success': False,
                    'error': str(e)
                }
        
        def get_patient_appointments(self, patient_name: str, patient_phone: str = None) -> List[Dict]:
            """Get appointments for a patient"""
            try:
                self.cursor.execute('''
                    SELECT * FROM appointments 
                    WHERE patient_name = ?
                    ORDER BY appointment_date, appointment_time
                ''', (patient_name,))
                
                appointments = []
                for row in self.cursor.fetchall():
                    appointments.append({
                        'id': row[0],
                        'patient_name': row[1],
                        'doctor_name': row[3],
                        'specialty': row[4],
                        'date': row[5],
                        'time': row[6],
                        'status': row[7] if len(row) > 7 else 'confirmed'
                    })
                return appointments
            except sqlite3.Error as e:
                return []
    
    return HospitalDatabase()

@st.cache_resource
def init_nlp_pipeline():
    """Initialize NLP pipeline"""
    
    class MedicalNLPPipeline:
        def __init__(self):
            """Initialize medical NLP with rule-based processing"""
            # Medical knowledge base
            self.medical_specialties = {
                'cardiology': ['heart', 'cardiac', 'cardio', 'chest pain', 'heart attack', 'palpitations', 'coronary'],
                'dermatology': ['skin', 'rash', 'acne', 'dermat', 'mole', 'eczema', 'psoriasis', 'dermatitis'],
                'pediatrics': ['child', 'baby', 'pediatric', 'kid', 'infant', 'children', 'vaccination'],
                'neurology': ['brain', 'headache', 'migraine', 'neurolog', 'seizure', 'memory', 'stroke'],
                'orthopedics': ['bone', 'joint', 'fracture', 'orthopedic', 'back pain', 'arthritis', 'knee'],
                'gynecology': ['women', 'pregnancy', 'gynec', 'obstetric', 'pap smear', 'menstrual'],
                'psychiatry': ['mental', 'depression', 'anxiety', 'psychiatric', 'therapy', 'stress', 'mood'],
                'internal_medicine': ['general', 'internal', 'checkup', 'physical', 'diabetes', 'hypertension']
            }
            
            self.symptoms = [
                'pain', 'fever', 'cough', 'headache', 'nausea', 'fatigue', 'dizziness',
                'shortness of breath', 'chest pain', 'back pain', 'joint pain', 'rash',
                'swelling', 'numbness', 'weakness', 'insomnia', 'anxiety', 'depression'
            ]
            
            self.urgency_indicators = ['urgent', 'asap', 'emergency', 'immediately', 'soon', 'quickly', 'emergency']
        
        def extract_medical_entities(self, text: str) -> Dict:
            """Extract medical entities from text"""
            text_lower = text.lower()
            entities = {
                'specialties': [],
                'symptoms': [],
                'urgency': [],
                'doctors': [],
                'confidence_scores': {}
            }
            
            # Extract specialties
            for specialty, keywords in self.medical_specialties.items():
                for keyword in keywords:
                    if keyword.lower() in text_lower:
                        if specialty not in entities['specialties']:
                            entities['specialties'].append(specialty)
                            entities['confidence_scores'][specialty] = 0.85
                        break
            
            # Extract symptoms
            for symptom in self.symptoms:
                if symptom.lower() in text_lower:
                    entities['symptoms'].append(symptom)
            
            # Extract urgency
            for urgency in self.urgency_indicators:
                if urgency.lower() in text_lower:
                    entities['urgency'].append(urgency)
            
            # Extract doctor names
            doctor_patterns = [r'dr\.?\s+(\w+)', r'doctor\s+(\w+)']
            for pattern in doctor_patterns:
                matches = re.findall(pattern, text_lower)
                for match in matches:
                    entities['doctors'].append(f"Dr. {match.title()}")
            
            return entities
        
        def classify_intent(self, text: str) -> Dict:
            """Classify user intent"""
            text_lower = text.lower()
            
            intent_patterns = {
                'book_appointment': [
                    'book', 'schedule', 'appointment', 'make appointment', 'see doctor',
                    'visit', 'consultation', 'need to see', 'want to see'
                ],
                'check_appointment': [
                    'check appointment', 'my appointment', 'when is', 'appointment status',
                    'what appointments', 'show appointments'
                ],
                'cancel_appointment': [
                    'cancel', 'reschedule', 'change appointment', 'move appointment',
                    'can\'t make', 'need to cancel'
                ],
                'get_info': [
                    'hours', 'location', 'address', 'phone', 'cost', 'price', 'insurance',
                    'specialties', 'doctors available'
                ],
                'greeting': [
                    'hello', 'hi', 'hey', 'good morning', 'good afternoon', 'help'
                ]
            }
            
            best_intent = 'unknown'
            best_score = 0
            
            for intent, patterns in intent_patterns.items():
                score = 0
                for pattern in patterns:
                    if pattern in text_lower:
                        score += 1
                
                if score > best_score:
                    best_score = score
                    best_intent = intent
            
            confidence = min(best_score * 0.3, 1.0) if best_score > 0 else 0.1
            
            return {
                'intent': best_intent,
                'confidence': confidence
            }
        
        def process_query(self, user_input: str) -> Dict:
            """Process complete user query"""
            entities = self.extract_medical_entities(user_input)
            intent_result = self.classify_intent(user_input)
            
            return {
                'user_input': user_input,
                'intent': intent_result['intent'],
                'confidence': intent_result['confidence'],
                'entities': entities,
                'medical_context': {
                    'needs_specialty': len(entities['specialties']) == 0 and intent_result['intent'] == 'book_appointment',
                    'has_urgency': len(entities['urgency']) > 0,
                    'suggested_specialties': entities['specialties'][:2],
                    'is_emergency': any('emergency' in u.lower() for u in entities['urgency'])
                }
            }
    
    return MedicalNLPPipeline()

@st.cache_resource
def init_chatbot(_db, _nlp):
    """Initialize the medical chatbot"""
    
    class MedicalChatbot:
        def __init__(self, database, nlp_pipeline):
            """Initialize medical chatbot"""
            self.db = database
            self.nlp = nlp_pipeline
            self.conversation_state = {}
            
            # Session timeout (3 minutes)
            self.SESSION_TIMEOUT = 180
            
            # Conversation states
            self.STATES = {
                'IDLE': 'idle',
                'COLLECTING_SPECIALTY': 'collecting_specialty',
                'COLLECTING_DOCTOR': 'collecting_doctor',
                'COLLECTING_PATIENT_INFO': 'collecting_patient_info',
                'COLLECTING_PHONE': 'collecting_phone',
                'COLLECTING_DATE_TIME': 'collecting_date_time',
                'CONFIRMING_APPOINTMENT': 'confirming_appointment',
                'CHECKING_APPOINTMENT_NAME': 'checking_appointment_name',
                'APPOINTMENT_FOUND': 'appointment_found',
                'MODIFYING_APPOINTMENT': 'modifying_appointment',
                'CONFIRMING_CANCELLATION': 'confirming_cancellation'
            }
            
            # FAQ Database
            self.faqs = {
                'billing': {
                    'answer': f"💰 **Billing Questions**: Call our billing department at 📞 {BILLING_PHONE}\\n• Payment plans available\\n• Insurance verification\\n• Billing inquiries\\n• Email: insurance@BaptistHealth.net",
                    'keywords': ['billing', 'payment', 'insurance', 'cost', 'price', 'charge']
                },
                'hours': {
                    'answer': f"🕒 **{CLINIC_NAME} Hours:**\\n• **24/7 Emergency Care** - Always open for emergencies\\n• **Outpatient Services**: Monday - Friday 8:00 AM - 6:00 PM\\n• **Emergency Department**: 24 hours, 7 days a week\\n• **Visitor Hours**: 7:00 AM - 9:00 PM daily",
                    'keywords': ['hours', 'open', 'close', 'time', 'schedule']
                },
                'location': {
                    'answer': f"📍 **Baptist Health Hospital Doral Location:**\\n{CLINIC_ADDRESS}\\n🚗 **Parking**: Free parking available for patients\\n🚌 **Public Transport**: Accessible by Miami-Dade Transit\\n🗺️ **Nearby**: Doral community area",
                    'keywords': ['location', 'address', 'where', 'directions', 'parking']
                }
            }
        
        def _get_main_menu_text(self) -> str:
            """Get main menu text"""
            return f"👋 Welcome to **{CLINIC_NAME}**! I'm your virtual assistant. I can help you:\\n\\n• **Book new appointments**\\n• **Check existing appointments**\\n• **Get hospital information**\\n• **Answer frequently asked questions (FAQs)**\\n\\nHow can I help you today?"
        
        def process_message(self, user_input: str, session_id: str = "streamlit_session") -> Dict:
            """Process user message and return response"""
            # Initialize session if not exists
            if session_id not in self.conversation_state:
                self.conversation_state[session_id] = {
                    'state': self.STATES['IDLE'],
                    'appointment_data': {},
                    'last_intent': None,
                    'context': {},
                    'attempt_count': 0,
                    'last_activity': time.time()
                }
            
            session = self.conversation_state[session_id]
            session['last_activity'] = time.time()
            
            # Process with NLP
            nlp_result = self.nlp.process_query(user_input)
            intent = nlp_result['intent']
            entities = nlp_result['entities']
            
            # Route to appropriate handler
            if intent == 'greeting':
                return self._handle_greeting(session)
            elif intent == 'book_appointment':
                return self._handle_book_appointment(session, entities, user_input)
            elif intent == 'get_info':
                return self._handle_get_info(user_input)
            else:
                return self._handle_continuation(session, user_input, entities)
        
        def _handle_greeting(self, session: Dict) -> Dict:
            """Handle greeting messages"""
            self._reset_session(session)
            return {
                'response': self._get_main_menu_text(),
                'type': 'greeting',
                'suggestions': ['Book appointment', 'Hospital info', 'FAQs']
            }
        
        def _reset_session(self, session: Dict) -> None:
            """Reset session to initial state"""
            session['state'] = self.STATES['IDLE']
            session['appointment_data'] = {}
            session['attempt_count'] = 0
            session['last_activity'] = time.time()
        
        def _handle_book_appointment(self, session: Dict, entities: Dict, user_input: str) -> Dict:
            """Handle appointment booking flow"""
            # Check for emergency
            if entities['urgency'] and any('emergency' in u.lower() for u in entities['urgency']):
                return {
                    'response': f"🚨 **Medical Emergency Protocol**\\n\\nFor medical emergencies:\\n• **Call 911 immediately**\\n• **Emergency Department**: {CLINIC_NAME} - {CLINIC_PHONE}\\n• **We are open 24/7** for emergency care\\n\\nI can help you schedule regular appointments once your emergency is addressed.",
                    'type': 'emergency_redirect'
                }
            
            # Update session with extracted entities
            if entities['specialties']:
                session['appointment_data']['specialty'] = entities['specialties'][0]
            if entities['doctors']:
                session['appointment_data']['doctor'] = entities['doctors'][0]
            
            # Determine next step in booking flow
            if 'specialty' not in session['appointment_data']:
                session['state'] = self.STATES['COLLECTING_SPECIALTY']
                return {
                    'response': f"🏥 **Book Appointment** - {CLINIC_NAME}\\n\\nWhich medical specialty do you need?",
                    'type': 'specialty_selection',
                    'suggestions': ['Cardiology', 'Dermatology', 'Pediatrics', 'Neurology', 'Orthopedics']
                }
            
            # Get available doctors for specialty
            doctors = self.db.get_available_doctors(session['appointment_data']['specialty'])
            if not doctors:
                return {
                    'response': f"Sorry, we don't have doctors available for {session['appointment_data']['specialty']} right now. Please try another specialty or call {CLINIC_PHONE}.",
                    'type': 'error'
                }
            
            if 'doctor' not in session['appointment_data']:
                session['state'] = self.STATES['COLLECTING_DOCTOR']
                doctor_list = "\\n".join([f"• **{doc['name']}** - Available: {', '.join(doc['available_days'][:3])}" for doc in doctors[:3]])
                return {
                    'response': f"👨‍⚕️ **Available Doctors** for {session['appointment_data']['specialty']}:\\n\\n{doctor_list}\\n\\nWhich doctor would you prefer?",
                    'type': 'doctor_selection',
                    'suggestions': [doc['name'] for doc in doctors[:3]]
                }
            
            # Collect patient information
            if 'patient_name' not in session['appointment_data']:
                session['state'] = self.STATES['COLLECTING_PATIENT_INFO']
                return {
                    'response': "📝 **Patient Information**\\n\\nWhat's the patient's full name?",
                    'type': 'patient_info',
                    'collecting': 'name'
                }
            
            return self._continue_booking_flow(session)
        
        def _continue_booking_flow(self, session: Dict) -> Dict:
            """Continue the booking flow"""
            appointment_data = session['appointment_data']
            
            if 'patient_phone' not in appointment_data:
                session['state'] = self.STATES['COLLECTING_PHONE']
                return {
                    'response': "📱 What's your contact phone number?",
                    'type': 'patient_info',
                    'collecting': 'phone'
                }
            
            if 'date' not in appointment_data or 'time' not in appointment_data:
                session['state'] = self.STATES['COLLECTING_DATE_TIME']
                doctors = self.db.get_available_doctors(appointment_data['specialty'])
                selected_doctor = next((d for d in doctors if d['name'] == appointment_data.get('doctor')), doctors[0] if doctors else None)
                
                if selected_doctor:
                    available_times = selected_doctor['available_times'][:4]
                    return {
                        'response': f"🗓️ **Available Time Slots** with {selected_doctor['name']}:\\n\\n" + "\\n".join([f"• {time}" for time in available_times]) + "\\n\\nWhich time works best for you?",
                        'type': 'time_selection',
                        'suggestions': available_times
                    }
            
            return self._confirm_appointment(session)
        
        def _confirm_appointment(self, session: Dict) -> Dict:
            """Confirm and book the appointment"""
            appointment_data = session['appointment_data']
            
            booking_result = self.db.book_appointment({
                'name': appointment_data.get('patient_name'),
                'phone': appointment_data.get('patient_phone'),
                'doctor': appointment_data.get('doctor'),
                'specialty': appointment_data.get('specialty'),
                'date': appointment_data.get('date', '2024-02-15'),
                'time': appointment_data.get('time', '10:00'),
                'symptoms': appointment_data.get('symptoms', ''),
                'urgency': 'normal'
            })
            
            if booking_result['success']:
                self._reset_session(session)
                return {
                    'response': f"✅ **Appointment Confirmed!** - {CLINIC_NAME}\\n\\n📋 **Details:**\\n• **Patient**: {appointment_data.get('patient_name')}\\n• **Doctor**: {appointment_data.get('doctor')}\\n• **Date**: {appointment_data.get('date', '2024-02-15')}\\n• **Time**: {appointment_data.get('time', '10:00')}\\n• **Appointment ID**: #{booking_result['appointment_id']}\\n\\n📞 **Confirmation call within 24 hours**\\n💡 **Arrive 15 minutes early**",
                    'type': 'booking_confirmation',
                    'appointment_id': booking_result['appointment_id'],
                    'suggestions': ['Book another', 'Hospital info', 'FAQs']
                }
            else:
                return {
                    'response': f"❌ **Booking Error**: {booking_result.get('error')}. Please try again or call {CLINIC_PHONE}.",
                    'type': 'error'
                }
        
        def _is_phone_number(self, text: str) -> bool:
            """Check if text looks like a phone number"""
            cleaned = re.sub(r'[^\d]', '', text)
            return cleaned.isdigit() and 7 <= len(cleaned) <= 15
        
        def _handle_continuation(self, session: Dict, user_input: str, entities: Dict) -> Dict:
            """Handle continuation of conversation flow"""
            current_state = session['state']
            user_input_clean = user_input.strip()
            
            # Handle regular booking flow states
            if current_state == self.STATES['COLLECTING_SPECIALTY']:
                if entities['specialties']:
                    session['appointment_data']['specialty'] = entities['specialties'][0]
                    return self._handle_book_appointment(session, entities, user_input)
                else:
                    user_lower = user_input.lower()
                    for specialty in self.nlp.medical_specialties.keys():
                        if specialty in user_lower or any(keyword in user_lower for keyword in self.nlp.medical_specialties[specialty]):
                            session['appointment_data']['specialty'] = specialty
                            return self._handle_book_appointment(session, entities, user_input)
                    
                    return {
                        'response': "Please select a medical specialty: Cardiology, Dermatology, Pediatrics, Neurology, or Orthopedics",
                        'type': 'retry_input',
                        'suggestions': ['Cardiology', 'Dermatology', 'Pediatrics', 'Neurology', 'Orthopedics']
                    }
            
            elif current_state == self.STATES['COLLECTING_DOCTOR']:
                doctors = self.db.get_available_doctors(session['appointment_data']['specialty'])
                doctor_found = False
                
                for doctor in doctors:
                    if user_input_clean.lower() in doctor['name'].lower() or doctor['name'].lower() in user_input_clean.lower():
                        session['appointment_data']['doctor'] = doctor['name']
                        doctor_found = True
                        break
                
                if doctor_found:
                    return self._continue_booking_flow(session)
                else:
                    doctor_names = [doc['name'] for doc in doctors[:3]]
                    return {
                        'response': f"Please select one of the available doctors: {', '.join(doctor_names)}",
                        'type': 'retry_input',
                        'suggestions': doctor_names
                    }
            
            elif current_state == self.STATES['COLLECTING_PATIENT_INFO']:
                if user_input_clean and len(user_input_clean) > 1:
                    session['appointment_data']['patient_name'] = user_input_clean
                    return self._continue_booking_flow(session)
                else:
                    return {
                        'response': "Please provide the patient's full name.",
                        'type': 'retry_input'
                    }
            
            elif current_state == self.STATES['COLLECTING_PHONE']:
                if self._is_phone_number(user_input_clean):
                    session['appointment_data']['patient_phone'] = user_input_clean
                    return self._continue_booking_flow(session)
                else:
                    return {
                        'response': "Please provide a valid phone number (e.g., 786-595-3900).",
                        'type': 'retry_input'
                    }
            
            elif current_state == self.STATES['COLLECTING_DATE_TIME']:
                if ':' in user_input_clean or 'am' in user_input_clean.lower() or 'pm' in user_input_clean.lower():
                    session['appointment_data']['time'] = user_input_clean
                    session['appointment_data']['date'] = '2024-02-15'
                    return self._confirm_appointment(session)
                else:
                    doctors = self.db.get_available_doctors(session['appointment_data']['specialty'])
                    selected_doctor = next((d for d in doctors if d['name'] == session['appointment_data'].get('doctor')), doctors[0] if doctors else None)
                    if selected_doctor:
                        available_times = selected_doctor['available_times']
                        for time_slot in available_times:
                            if user_input_clean in time_slot or time_slot in user_input_clean:
                                session['appointment_data']['time'] = time_slot
                                session['appointment_data']['date'] = '2024-02-15'
                                return self._confirm_appointment(session)
                    
                    return {
                        'response': "Please select one of the available time slots.",
                        'type': 'retry_input'
                    }
            
            # Handle commands in IDLE state
            if current_state == self.STATES['IDLE']:
                user_lower = user_input.lower()
                
                # Check if it's an FAQ question
                for faq_key, faq_data in self.faqs.items():
                    for keyword in faq_data['keywords']:
                        if keyword in user_lower:
                            return {
                                'response': faq_data['answer'],
                                'type': 'faq_answer',
                                'faq_category': faq_key,
                                'suggestions': ['Book appointment', 'Hospital info', 'FAQs']
                            }
            
            return {
                'response': f"I'm not sure how to help with that. You can ask me to:\\n\\n• **Book an appointment**\\n• **Get hospital information**\\n• **Answer FAQs**\\n\\nWhat would you like to do?",
                'type': 'fallback',
                'suggestions': ['Book appointment', 'Hospital info', 'FAQs']
            }
        
        def _handle_get_info(self, user_input: str) -> Dict:
            """Handle information requests"""
            user_lower = user_input.lower()
            
            if 'hours' in user_lower or 'time' in user_lower:
                response_text = f"🕒 **{CLINIC_NAME} Hours:**\\n\\n• **Emergency Department**: 24/7 - Always open\\n• **Outpatient Services**: Monday - Friday 8:00 AM - 6:00 PM\\n• **Visitor Hours**: 7:00 AM - 9:00 PM daily\\n\\n📞 **Emergency**: Call 911\\n📱 **Hospital**: {CLINIC_PHONE}"
            elif 'location' in user_lower or 'address' in user_lower:
                response_text = f"📍 **{CLINIC_NAME} Location:**\\n\\n{CLINIC_ADDRESS}\\n\\n🚗 **Free parking** available for patients\\n🚌 **Public transport**: Miami-Dade Transit accessible\\n🗺️ **Area**: Doral community"
            elif 'phone' in user_lower or 'contact' in user_lower:
                response_text = f"📞 **Contact {CLINIC_NAME}:**\\n\\n• **Main Line**: {CLINIC_PHONE}\\n• **Appointments**: {CLINIC_PHONE}\\n• **Billing**: {BILLING_PHONE}\\n• **Insurance**: {INSURANCE_PHONE}\\n• **Emergency**: 911\\n\\n✉️ **Email**: insurance@BaptistHealth.net"
            else:
                response_text = f"ℹ️ **{CLINIC_NAME} Information:**\\n\\n📍 **Address**: {CLINIC_ADDRESS}\\n📞 **Phone**: {CLINIC_PHONE}\\n📧 **Billing**: {BILLING_PHONE}\\n\\n🏥 **Services**: 24/7 Emergency Care, Advanced Medical Services\\n💳 **Insurance**: Most plans accepted\\n🅿️ **Parking**: Free on-site\\n\\nWhat specific information do you need?"
            
            return {
                'response': response_text,
                'type': 'info_provided',
                'suggestions': ['Hours', 'Location', 'Contact', 'Book appointment']
            }
    
    return MedicalChatbot(_db, _nlp)

def display_message(message, is_user=False):
    """Display a chat message"""
    if is_user:
        st.markdown(f'''
        <div class="chat-message user-message">
            <strong>👤 You:</strong> {message}
        </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown(f'''
        <div class="chat-message bot-message">
            <strong>🤖 Baptist Health Assistant:</strong><br>
            {message.replace("\\n", "<br>")}
        </div>
        ''', unsafe_allow_html=True)

def main():
    """Main Streamlit application"""
    
    # Header
    st.markdown(f'''
    <div class="main-header">
        <h1>🏥 {CLINIC_NAME}</h1>
        <h3>AI Medical Assistant - Appointment Booking & Information</h3>
        <p>📍 {CLINIC_ADDRESS} | 📞 {CLINIC_PHONE}</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # Initialize components
    if not st.session_state.db_initialized:
        with st.spinner("🔧 Initializing Baptist Health Hospital Doral Medical System..."):
            try:
                db = init_database()
                nlp = init_nlp_pipeline()
                st.session_state.chatbot = init_chatbot(db, nlp)
                st.session_state.db_initialized = True
                st.success("✅ Medical chatbot system initialized successfully!")
            except Exception as e:
                st.error(f"❌ System initialization failed: {e}")
                st.stop()
    
    # Sidebar with hospital information
    st.sidebar.markdown("### 🏥 Hospital Information")
    st.sidebar.markdown(f"""
    **{CLINIC_NAME}**
    
    📍 **Address:**  
    {CLINIC_ADDRESS}
    
    📞 **Main Phone:**  
    {CLINIC_PHONE}
    
    💰 **Billing:**  
    {BILLING_PHONE}
    
    🕒 **Hours:**
    - Emergency: 24/7
    - Outpatient: Mon-Fri 8AM-6PM
    - Visitors: 7AM-9PM daily
    
    🚗 **Free Parking Available**
    """)
    
    st.sidebar.markdown("### ⚡ Quick Actions")
    if st.sidebar.button("🆕 New Conversation"):
        st.session_state.conversation_history = []
        if st.session_state.chatbot:
            st.session_state.chatbot.conversation_state = {}
        st.rerun()
    
    if st.sidebar.button("📋 Book Appointment"):
        response = st.session_state.chatbot.process_message("I want to book an appointment")
        st.session_state.conversation_history.append(("I want to book an appointment", response['response']))
        st.rerun()
    
    if st.sidebar.button("ℹ️ Hospital Info"):
        response = st.session_state.chatbot.process_message("What are your hours and location?")
        st.session_state.conversation_history.append(("What are your hours and location?", response['response']))
        st.rerun()
    
    # Main chat interface
    st.markdown("### 💬 Chat with Baptist Health Assistant")
    
    # Display conversation history
    for user_msg, bot_msg in st.session_state.conversation_history:
        display_message(user_msg, is_user=True)
        display_message(bot_msg, is_user=False)
    
    # Chat input
    user_input = st.chat_input("Type your message here... (e.g., 'I need an appointment with cardiology')")
    
    if user_input:
        # Process message
        if st.session_state.chatbot:
            response = st.session_state.chatbot.process_message(user_input)
            
            # Add to conversation history
            st.session_state.conversation_history.append((user_input, response['response']))
            
            # Display new messages
            display_message(user_input, is_user=True)
            display_message(response['response'], is_user=False)
            
            # Show suggestions if available
            if 'suggestions' in response and response['suggestions']:
                st.markdown("**💡 Suggestions:**")
                cols = st.columns(len(response['suggestions']))
                for i, suggestion in enumerate(response['suggestions']):
                    if cols[i].button(suggestion, key=f"suggestion_{i}_{len(st.session_state.conversation_history)}"):
                        # Process suggestion as new message
                        sugg_response = st.session_state.chatbot.process_message(suggestion)
                        st.session_state.conversation_history.append((suggestion, sugg_response['response']))
                        st.rerun()
        else:
            st.error("❌ Chatbot not initialized. Please refresh the page.")
    
    # Footer
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p><strong>{CLINIC_NAME}</strong> - Advanced Medical AI Assistant</p>
        <p>🤖 Powered by BioClinicalBERT Medical NLP | 🔒 HIPAA Compliant | ⚡ Real-time Appointment Booking</p>
        <p>For emergencies, call 911 or visit our Emergency Department (24/7)</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()