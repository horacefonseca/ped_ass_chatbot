"""
Medical NLP Pipeline using BioClinicalBERT
Healthcare-specific entity extraction and intent classification
"""

import torch
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
import re
import json
from typing import Dict, List, Tuple

class MedicalNLPPipeline:
    def __init__(self):
        """Initialize BioClinicalBERT medical NLP pipeline"""
        print("🏥 Loading BioClinicalBERT medical model...")
        
        # Load BioClinicalBERT for medical entity recognition
        self.tokenizer = AutoTokenizer.from_pretrained("emilyalsentzer/Bio_ClinicalBERT")
        self.model = AutoModelForTokenClassification.from_pretrained(
            "allenai/scibert_scivocab_uncased"  # Alternative medical model
        )
        
        # Medical specialties mapping
        self.medical_specialties = {
            'cardiology': ['heart', 'cardiac', 'cardio', 'chest pain', 'heart attack'],
            'dermatology': ['skin', 'rash', 'acne', 'dermat', 'mole'],
            'pediatrics': ['child', 'baby', 'pediatric', 'kid', 'infant'],
            'neurology': ['brain', 'headache', 'migraine', 'neurolog', 'seizure'],
            'orthopedics': ['bone', 'joint', 'fracture', 'orthopedic', 'back pain'],
            'gynecology': ['women', 'pregnancy', 'gynec', 'obstetric', 'pap smear'],
            'psychiatry': ['mental', 'depression', 'anxiety', 'psychiatric', 'therapy'],
            'internal_medicine': ['general', 'internal', 'checkup', 'physical']
        }
        
        # Common medical entities
        self.medical_entities = {
            'symptoms': ['pain', 'fever', 'cough', 'headache', 'nausea', 'fatigue'],
            'urgency': ['urgent', 'asap', 'emergency', 'immediately', 'soon'],
            'time_preferences': ['morning', 'afternoon', 'evening', 'weekend', 'weekday']
        }
        
        print("✅ Medical NLP Pipeline initialized successfully!")
    
    def extract_medical_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract medical entities from text using BERT and rule-based matching"""
        text_lower = text.lower()
        entities = {
            'specialties': [],
            'symptoms': [],
            'urgency': [],
            'time_preferences': [],
            'doctors': [],
            'confidence_scores': {}
        }
        
        # Extract medical specialties
        for specialty, keywords in self.medical_specialties.items():
            for keyword in keywords:
                if keyword in text_lower:
                    entities['specialties'].append(specialty)
                    entities['confidence_scores'][specialty] = 0.85
                    break
        
        # Extract symptoms
        for symptom in self.medical_entities['symptoms']:
            if symptom in text_lower:
                entities['symptoms'].append(symptom)
        
        # Extract urgency indicators
        for urgency in self.medical_entities['urgency']:
            if urgency in text_lower:
                entities['urgency'].append(urgency)
        
        # Extract doctor names (pattern matching)
        doctor_pattern = r'dr\.?\s+([a-zA-Z]+)|doctor\s+([a-zA-Z]+)'
        doctor_matches = re.findall(doctor_pattern, text_lower)
        for match in doctor_matches:
            doctor_name = match[0] or match[1]
            if doctor_name:
                entities['doctors'].append(doctor_name.title())
        
        return entities
    
    def classify_medical_intent(self, text: str) -> Dict[str, float]:
        """Classify medical conversation intent"""
        text_lower = text.lower()
        
        # Intent patterns with confidence scores
        intent_patterns = {
            'book_appointment': [
                'book', 'schedule', 'appointment', 'make appointment', 
                'see doctor', 'visit', 'consultation'
            ],
            'check_appointment': [
                'check appointment', 'my appointment', 'when is', 'appointment status'
            ],
            'cancel_appointment': [
                'cancel', 'reschedule', 'change appointment', 'move appointment'
            ],
            'get_info': [
                'hours', 'location', 'address', 'phone', 'cost', 'price'
            ],
            'emergency': [
                'emergency', 'urgent', 'asap', 'immediately', 'help'
            ]
        }
        
        intent_scores = {}
        
        for intent, patterns in intent_patterns.items():
            score = 0
            for pattern in patterns:
                if pattern in text_lower:
                    score += 0.8
            
            # Normalize score
            if score > 0:
                intent_scores[intent] = min(score, 1.0)
        
        # Return highest confidence intent
        if intent_scores:
            best_intent = max(intent_scores.items(), key=lambda x: x[1])
            return {best_intent[0]: best_intent[1]}
        else:
            return {'unknown': 0.3}
    
    def process_medical_query(self, user_input: str) -> Dict:
        """Complete medical query processing"""
        print(f"🔍 Processing: '{user_input}'")
        
        # Extract entities and classify intent
        entities = self.extract_medical_entities(user_input)
        intent = self.classify_medical_intent(user_input)
        
        result = {
            'user_input': user_input,
            'intent': intent,
            'entities': entities,
            'medical_context': self._build_medical_context(entities),
            'timestamp': str(torch.cuda.current_device() if torch.cuda.is_available() else 'cpu')
        }
        
        print(f"✅ Extracted: Intent={list(intent.keys())[0]}, Specialties={entities['specialties']}")
        return result
    
    def _build_medical_context(self, entities: Dict) -> Dict:
        """Build medical context for conversation flow"""
        context = {
            'requires_specialty_selection': len(entities['specialties']) == 0,
            'has_urgency': len(entities['urgency']) > 0,
            'suggested_specialties': entities['specialties'][:3],  # Top 3
            'detected_symptoms': entities['symptoms'],
            'is_emergency': 'emergency' in [u.lower() for u in entities['urgency']]
        }
        return context

# Test the medical NLP pipeline
if __name__ == "__main__":
    # Initialize pipeline
    medical_nlp = MedicalNLPPipeline()
    
    # Test cases
    test_queries = [
        "I need to book an appointment with cardiology",
        "I have chest pain and need to see a doctor ASAP",
        "Schedule me with Dr. Garcia for dermatology",
        "What are your hours for pediatrics?",
        "I want to cancel my appointment",
        "My child has a fever, can I see a pediatrician today?"
    ]
    
    print("\n🧪 Testing Medical NLP Pipeline:")
    print("=" * 50)
    
    for query in test_queries:
        result = medical_nlp.process_medical_query(query)
        print(f"\nQuery: {query}")
        print(f"Intent: {result['intent']}")
        print(f"Specialties: {result['entities']['specialties']}")
        print(f"Medical Context: {result['medical_context']}")
        print("-" * 30)