"""
Advanced Medical Conversation Flows
Context-aware dialogue management with medical intelligence
"""

from typing import Dict, List, Optional, Tuple
import json
import re
from datetime import datetime, timedelta
from enum import Enum

class ConversationState(Enum):
    """Conversation states for medical chatbot"""
    IDLE = "idle"
    GREETING = "greeting"
    COLLECTING_SPECIALTY = "collecting_specialty"
    COLLECTING_DOCTOR = "collecting_doctor" 
    COLLECTING_PATIENT_INFO = "collecting_patient_info"
    COLLECTING_DATE_TIME = "collecting_date_time"
    CONFIRMING_APPOINTMENT = "confirming_appointment"
    HANDLING_EMERGENCY = "handling_emergency"
    PROVIDING_INFO = "providing_info"
    CHECKING_APPOINTMENTS = "checking_appointments"

class MedicalConversationEngine:
    def __init__(self, database, nlp_pipeline):
        """Initialize advanced conversation engine"""
        self.db = database
        self.nlp = nlp_pipeline
        self.sessions = {}
        
        # Medical conversation templates
        self.response_templates = {
            'greeting': [
                "👋 Hello! I'm your medical appointment assistant. I can help you:",
                "• Book new appointments",
                "• Check existing appointments", 
                "• Get clinic information",
                "• Answer medical facility questions",
                "",
                "How can I help you today?"
            ],
            'emergency_detected': [
                "🚨 IMPORTANT: For medical emergencies, please:",
                "• Call 911 immediately",
                "• Go to the nearest emergency room",
                "• Contact your doctor directly",
                "",
                "I can help you schedule regular appointments once your emergency is addressed."
            ],
            'specialty_request': [
                "I'd be happy to help you book an appointment! 🏥",
                "",
                "Which medical specialty do you need?"
            ],
            'doctor_selection': [
                "Great choice! Here are our available {specialty} doctors:",
                "",
                "{doctor_list}",
                "",
                "Which doctor would you prefer?"
            ],
            'patient_info_request': [
                "Perfect! Now I need some information to book your appointment.",
                "",
                "What's your full name?"
            ],
            'phone_request': [
                "Thank you! What's your phone number?"
            ],
            'time_selection': [
                "Excellent! Here are available time slots with {doctor}:",
                "",
                "{time_slots}",
                "",
                "Which time works best for you?"
            ],
            'appointment_confirmed': [
                "✅ Appointment booked successfully!",
                "",
                "📋 **Appointment Details:**",
                "• Patient: {patient_name}",
                "• Doctor: {doctor_name}",
                "• Specialty: {specialty}",
                "• Date: {date}",
                "• Time: {time}",
                "• Appointment ID: #{appointment_id}",
                "",
                "You'll receive a confirmation call within 24 hours.",
                "Is there anything else I can help you with?"
            ]
        }
        
        # Medical specialties with intelligent routing
        self.specialty_routing = {
            'cardiology': {
                'keywords': ['heart', 'chest pain', 'cardiac', 'palpitations', 'blood pressure'],
                'emergency_keywords': ['heart attack', 'chest pain severe', 'cardiac arrest'],
                'description': 'Heart and cardiovascular system'
            },
            'dermatology': {
                'keywords': ['skin', 'rash', 'acne', 'mole', 'eczema', 'dermatitis'],
                'emergency_keywords': ['severe burn', 'severe allergic reaction'],
                'description': 'Skin, hair, and nail conditions'
            },
            'pediatrics': {
                'keywords': ['child', 'baby', 'kid', 'infant', 'vaccination', 'fever in child'],
                'emergency_keywords': ['child emergency', 'baby not breathing', 'high fever child'],
                'description': 'Medical care for children and adolescents'
            },
            'neurology': {
                'keywords': ['headache', 'migraine', 'seizure', 'memory', 'dizziness', 'brain'],
                'emergency_keywords': ['stroke', 'severe head injury', 'loss of consciousness'],
                'description': 'Brain and nervous system disorders'
            },
            'orthopedics': {
                'keywords': ['bone', 'joint', 'fracture', 'back pain', 'arthritis', 'sports injury'],
                'emergency_keywords': ['severe fracture', 'compound fracture', 'spinal injury'],
                'description': 'Bones, joints, muscles, and ligaments'
            },
            'gynecology': {
                'keywords': ['pregnancy', 'menstrual', 'pap smear', 'women health', 'gynecological'],
                'emergency_keywords': ['pregnancy emergency', 'severe bleeding'],
                'description': 'Women\'s reproductive health'
            },
            'psychiatry': {
                'keywords': ['depression', 'anxiety', 'mental health', 'therapy', 'stress', 'mood'],
                'emergency_keywords': ['suicidal thoughts', 'severe depression', 'psychiatric emergency'],
                'description': 'Mental health and behavioral disorders'
            },
            'internal_medicine': {
                'keywords': ['general', 'checkup', 'physical', 'diabetes', 'hypertension', 'wellness'],
                'emergency_keywords': ['severe illness', 'multiple symptoms'],
                'description': 'General adult medical care and prevention'
            }
        }
        
        print("🧠 Advanced Medical Conversation Engine initialized!")
    
    def process_message(self, user_input: str, session_id: str = "default") -> Dict:
        """Process user message with advanced medical intelligence"""
        # Initialize or get session
        session = self._get_or_create_session(session_id)
        
        # Log conversation
        session['conversation_history'].append({
            'timestamp': datetime.now().isoformat(),
            'user_input': user_input,
            'user_type': 'user'
        })
        
        # Process with NLP
        nlp_result = self.nlp.process_query(user_input)
        
        # Update session context
        session['last_nlp_result'] = nlp_result
        session['context'].update(nlp_result['medical_context'])
        
        # Check for emergency first
        if self._is_emergency(nlp_result):
            return self._handle_emergency(session)
        
        # Route based on current state and intent
        response = self._route_conversation(session, nlp_result, user_input)
        
        # Log response
        session['conversation_history'].append({
            'timestamp': datetime.now().isoformat(),
            'bot_response': response['response'],
            'response_type': response['type'],
            'user_type': 'bot'
        })
        
        return response
    
    def _get_or_create_session(self, session_id: str) -> Dict:
        """Get or create conversation session"""
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                'state': ConversationState.IDLE,
                'appointment_data': {},
                'context': {},
                'conversation_history': [],
                'created_at': datetime.now().isoformat(),
                'last_activity': datetime.now().isoformat()
            }
        
        # Update last activity
        self.sessions[session_id]['last_activity'] = datetime.now().isoformat()
        return self.sessions[session_id]
    
    def _is_emergency(self, nlp_result: Dict) -> bool:
        """Detect medical emergencies"""
        user_input = nlp_result['user_input'].lower()
        
        # Emergency keywords
        emergency_indicators = [
            'emergency', 'urgent', 'can\\'t breathe', 'chest pain severe',
            'heart attack', 'stroke', 'unconscious', 'severe bleeding',
            'suicidal', 'overdose', 'poisoning', 'severe pain',
            'call 911', 'ambulance'
        ]
        
        # Check for emergency indicators
        for indicator in emergency_indicators:
            if indicator in user_input:
                return True
        
        # Check specialty-specific emergencies
        for specialty, info in self.specialty_routing.items():
            for emergency_keyword in info['emergency_keywords']:
                if emergency_keyword.lower() in user_input:
                    return True
        
        return False
    
    def _handle_emergency(self, session: Dict) -> Dict:
        """Handle emergency situations"""
        session['state'] = ConversationState.HANDLING_EMERGENCY
        
        response_text = \"\\n\".join(self.response_templates['emergency_detected'])
        
        return {
            'response': response_text,
            'type': 'emergency_response',
            'priority': 'high',
            'suggestions': ['Call 911', 'Find nearest ER', 'Contact doctor']
        }
    
    def _route_conversation(self, session: Dict, nlp_result: Dict, user_input: str) -> Dict:
        """Route conversation based on state and intent"""
        current_state = session['state']
        intent = nlp_result['intent']
        entities = nlp_result['entities']
        
        # Handle greetings
        if intent == 'greeting' or current_state == ConversationState.IDLE:
            return self._handle_greeting(session)
        
        # Handle information requests
        if intent == 'get_info':
            return self._handle_info_request(session, user_input)
        
        # Handle appointment checking
        if intent == 'check_appointment':
            return self._handle_check_appointment(session)
        
        # Handle appointment booking flow
        if intent == 'book_appointment' or current_state in [
            ConversationState.COLLECTING_SPECIALTY,
            ConversationState.COLLECTING_DOCTOR,
            ConversationState.COLLECTING_PATIENT_INFO,
            ConversationState.COLLECTING_DATE_TIME
        ]:\n            return self._handle_booking_flow(session, nlp_result, user_input)\n        \n        # Handle cancellation\n        if intent == 'cancel_appointment':\n            return self._handle_cancel_appointment(session)\n        \n        # Default fallback\n        return self._handle_fallback(session, user_input)\n    \n    def _handle_greeting(self, session: Dict) -> Dict:\n        \"\"\"Handle greeting and welcome\"\"\"\n        session['state'] = ConversationState.GREETING\n        \n        response_text = \"\\n\".join(self.response_templates['greeting'])\n        \n        return {\n            'response': response_text,\n            'type': 'greeting',\n            'suggestions': ['Book appointment', 'Check appointments', 'Clinic hours', 'Location']\n        }\n    \n    def _handle_booking_flow(self, session: Dict, nlp_result: Dict, user_input: str) -> Dict:\n        \"\"\"Handle complex appointment booking flow\"\"\"\n        entities = nlp_result['entities']\n        current_state = session['state']\n        appointment_data = session['appointment_data']\n        \n        # Extract entities and update appointment data\n        if entities['specialties']:\n            appointment_data['specialty'] = entities['specialties'][0]\n        if entities['doctors']:\n            appointment_data['doctor'] = entities['doctors'][0] \n        if entities['symptoms']:\n            appointment_data['symptoms'] = ', '.join(entities['symptoms'])\n        \n        # Intelligent specialty detection\n        if 'specialty' not in appointment_data:\n            detected_specialty = self._detect_specialty_from_context(user_input, entities)\n            if detected_specialty:\n                appointment_data['specialty'] = detected_specialty\n        \n        # State machine for booking flow\n        if 'specialty' not in appointment_data:\n            return self._request_specialty(session)\n        elif 'doctor' not in appointment_data:\n            return self._request_doctor(session)\n        elif 'patient_name' not in appointment_data:\n            return self._request_patient_name(session)\n        elif 'patient_phone' not in appointment_data:\n            return self._request_phone(session, user_input)\n        elif 'time' not in appointment_data:\n            return self._request_time(session, user_input)\n        else:\n            return self._confirm_appointment(session)\n    \n    def _detect_specialty_from_context(self, user_input: str, entities: Dict) -> Optional[str]:\n        \"\"\"Intelligently detect specialty from context\"\"\"\n        user_lower = user_input.lower()\n        \n        # Check symptoms against specialties\n        for specialty, info in self.specialty_routing.items():\n            for keyword in info['keywords']:\n                if keyword.lower() in user_lower:\n                    return specialty\n        \n        # Check entities for clues\n        if entities['symptoms']:\n            symptom_text = ' '.join(entities['symptoms']).lower()\n            for specialty, info in self.specialty_routing.items():\n                for keyword in info['keywords']:\n                    if keyword.lower() in symptom_text:\n                        return specialty\n        \n        return None\n    \n    def _request_specialty(self, session: Dict) -> Dict:\n        \"\"\"Request specialty selection with intelligent suggestions\"\"\"\n        session['state'] = ConversationState.COLLECTING_SPECIALTY\n        \n        # Create specialty list with descriptions\n        specialty_list = []\n        for specialty, info in self.specialty_routing.items():\n            specialty_list.append(f\"• **{specialty.title()}**: {info['description']}\")\n        \n        response_text = \"\\n\".join(self.response_templates['specialty_request']) + \"\\n\\n\" + \"\\n\".join(specialty_list[:5])\n        \n        return {\n            'response': response_text,\n            'type': 'specialty_selection',\n            'suggestions': list(self.specialty_routing.keys())[:5]\n        }\n    \n    def _request_doctor(self, session: Dict) -> Dict:\n        \"\"\"Request doctor selection\"\"\"\n        session['state'] = ConversationState.COLLECTING_DOCTOR\n        specialty = session['appointment_data']['specialty']\n        \n        # Get available doctors\n        doctors = self.db.get_available_doctors(specialty)\n        if not doctors:\n            return {\n                'response': f\"Sorry, we don't have doctors available for {specialty} right now. Please try another specialty.\",\n                'type': 'error'\n            }\n        \n        # Format doctor list\n        doctor_list = []\n        for doc in doctors[:3]:\n            days = ', '.join(doc['available_days'][:3])\n            doctor_list.append(f\"• **{doc['name']}** - Available: {days}\")\n        \n        response_text = self.response_templates['doctor_selection'][0].format(specialty=specialty) + \"\\n\\n\" + \"\\n\".join(doctor_list) + \"\\n\\n\" + self.response_templates['doctor_selection'][-1]\n        \n        return {\n            'response': response_text,\n            'type': 'doctor_selection',\n            'suggestions': [doc['name'] for doc in doctors[:3]]\n        }\n    \n    def _request_patient_name(self, session: Dict) -> Dict:\n        \"\"\"Request patient name\"\"\"\n        session['state'] = ConversationState.COLLECTING_PATIENT_INFO\n        \n        response_text = \"\\n\".join(self.response_templates['patient_info_request'])\n        \n        return {\n            'response': response_text,\n            'type': 'patient_info_collection',\n            'collecting': 'name'\n        }\n    \n    def _request_phone(self, session: Dict, user_input: str) -> Dict:\n        \"\"\"Request phone number\"\"\"\n        # Store the name\n        session['appointment_data']['patient_name'] = user_input.strip()\n        \n        response_text = \"\\n\".join(self.response_templates['phone_request'])\n        \n        return {\n            'response': response_text,\n            'type': 'patient_info_collection',\n            'collecting': 'phone'\n        }\n    \n    def _request_time(self, session: Dict, user_input: str) -> Dict:\n        \"\"\"Request appointment time\"\"\"\n        session['state'] = ConversationState.COLLECTING_DATE_TIME\n        \n        # Store phone number\n        session['appointment_data']['patient_phone'] = user_input.strip()\n        \n        # Get doctor's available times\n        appointment_data = session['appointment_data']\n        doctors = self.db.get_available_doctors(appointment_data['specialty'])\n        selected_doctor = next((d for d in doctors if d['name'] == appointment_data.get('doctor')), doctors[0] if doctors else None)\n        \n        if not selected_doctor:\n            return {\n                'response': \"Sorry, there was an error finding available times. Please try again.\",\n                'type': 'error'\n            }\n        \n        # Format time slots\n        time_slots = [f\"• {time}\" for time in selected_doctor['available_times'][:4]]\n        \n        response_text = self.response_templates['time_selection'][0].format(doctor=selected_doctor['name']) + \"\\n\\n\" + \"\\n\".join(time_slots) + \"\\n\\n\" + self.response_templates['time_selection'][-1]\n        \n        return {\n            'response': response_text,\n            'type': 'time_selection',\n            'suggestions': selected_doctor['available_times'][:4]\n        }\n    \n    def _confirm_appointment(self, session: Dict) -> Dict:\n        \"\"\"Confirm and book appointment\"\"\"\n        session['state'] = ConversationState.CONFIRMING_APPOINTMENT\n        appointment_data = session['appointment_data']\n        \n        # Book the appointment\n        booking_result = self.db.book_appointment({\n            'name': appointment_data.get('patient_name'),\n            'phone': appointment_data.get('patient_phone'),\n            'doctor': appointment_data.get('doctor'),\n            'specialty': appointment_data.get('specialty'),\n            'date': '2024-02-15',  # Mock date for demo\n            'time': appointment_data.get('time'),\n            'symptoms': appointment_data.get('symptoms', ''),\n            'urgency': 'normal'\n        })\n        \n        if booking_result['success']:\n            # Reset session\n            session['state'] = ConversationState.IDLE\n            session['appointment_data'] = {}\n            \n            # Format confirmation\n            response_text = \"\\n\".join(self.response_templates['appointment_confirmed']).format(\n                patient_name=appointment_data.get('patient_name'),\n                doctor_name=appointment_data.get('doctor'),\n                specialty=appointment_data.get('specialty'),\n                date='February 15, 2024',\n                time=appointment_data.get('time'),\n                appointment_id=booking_result['appointment_id']\n            )\n            \n            return {\n                'response': response_text,\n                'type': 'booking_confirmation',\n                'appointment_id': booking_result['appointment_id'],\n                'suggestions': ['Book another appointment', 'Check appointments', 'Clinic info']\n            }\n        else:\n            return {\n                'response': f\"❌ Sorry, there was an error booking your appointment: {booking_result.get('error')}. Please try again.\",\n                'type': 'booking_error'\n            }\n    \n    def _handle_info_request(self, session: Dict, user_input: str) -> Dict:\n        \"\"\"Handle information requests\"\"\"\n        session['state'] = ConversationState.PROVIDING_INFO\n        user_lower = user_input.lower()\n        \n        if any(word in user_lower for word in ['hours', 'time', 'open', 'close']):\n            return {\n                'response': \"🕒 **Clinic Hours:**\\n\\n• Monday - Friday: 8:00 AM - 6:00 PM\\n• Saturday: 9:00 AM - 4:00 PM\\n• Sunday: Closed\\n\\n📞 For emergencies outside hours, call 911\",\n                'type': 'hours_info'\n            }\n        elif any(word in user_lower for word in ['location', 'address', 'where']):\n            return {\n                'response': \"📍 **Clinic Location:**\\n\\n🏥 Medical Center Plaza\\n123 Healthcare Drive\\nWellness City, WC 12345\\n\\n🚗 Free parking available\\n🚌 Bus routes: 15, 22, 45\\n🚇 Metro: Health Station (Blue Line)\",\n                'type': 'location_info'\n            }\n        elif any(word in user_lower for word in ['phone', 'contact', 'call']):\n            return {\n                'response': \"📞 **Contact Information:**\\n\\n• Main Line: (555) 123-4567\\n• Appointments: (555) 123-APPT (2778)\\n• Emergency: 911\\n• After Hours: (555) 123-URGENT\\n\\n✉️ Email: appointments@medicalcenter.com\\n🌐 Website: www.medicalcenter.com\",\n                'type': 'contact_info'\n            }\n        else:\n            return {\n                'response': \"ℹ️ **Medical Center Information:**\\n\\n🏥 **Our Services:**\\n• 8 Medical Specialties\\n• 10+ Experienced Doctors\\n• Modern Diagnostic Equipment\\n• Same-day Appointments Available\\n\\n💳 **Insurance:** Most major plans accepted\\n🌟 **Rating:** 4.8/5 stars (1,200+ reviews)\\n\\nWhat specific information would you like?\",\n                'type': 'general_info',\n                'suggestions': ['Hours', 'Location', 'Phone', 'Specialties', 'Insurance']\n            }\n    \n    def _handle_check_appointment(self, session: Dict) -> Dict:\n        \"\"\"Handle appointment checking\"\"\"\n        session['state'] = ConversationState.CHECKING_APPOINTMENTS\n        \n        return {\n            'response': \"I can help you check your appointments! 📅\\n\\nTo look up your appointments, I'll need:\\n• Your full name\\n• Phone number used for booking\\n\\nWhat's your full name?\",\n            'type': 'appointment_lookup_start'\n        }\n    \n    def _handle_cancel_appointment(self, session: Dict) -> Dict:\n        \"\"\"Handle appointment cancellation\"\"\"\n        return {\n            'response': \"I can help you cancel or reschedule your appointment. 📅\\n\\nPlease provide:\\n• Your full name\\n• Phone number\\n• Appointment date (if known)\\n\\nNote: Cancellations must be made at least 24 hours in advance.\",\n            'type': 'cancellation_start'\n        }\n    \n    def _handle_fallback(self, session: Dict, user_input: str) -> Dict:\n        \"\"\"Handle unrecognized inputs\"\"\"\n        return {\n            'response': \"I'm not sure how to help with that request. 🤔\\n\\nI can assist you with:\\n• 📅 **Booking appointments** - Schedule with our medical specialists\\n• 🔍 **Checking appointments** - View your existing bookings\\n• ℹ️ **Clinic information** - Hours, location, contact details\\n• ❌ **Canceling/rescheduling** - Modify existing appointments\\n\\nWhat would you like to do?\",\n            'type': 'fallback',\n            'suggestions': ['Book appointment', 'Check appointments', 'Clinic hours', 'Location']\n        }\n    \n    def get_session_summary(self, session_id: str) -> Dict:\n        \"\"\"Get conversation session summary\"\"\"\n        if session_id not in self.sessions:\n            return {'error': 'Session not found'}\n        \n        session = self.sessions[session_id]\n        return {\n            'session_id': session_id,\n            'state': session['state'].value,\n            'conversation_length': len(session['conversation_history']),\n            'appointment_data': session['appointment_data'],\n            'created_at': session['created_at'],\n            'last_activity': session['last_activity']\n        }\n\nif __name__ == \"__main__\":\n    print(\"🧠 Medical Conversation Engine - Advanced Flow Management\")\n    print(\"Features: Emergency detection, intelligent routing, context awareness\")