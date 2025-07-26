"""
Synthetic Training Data Generator for Medical Chatbot
Generates thousands of realistic medical conversation examples
"""

import json
import random
from typing import List, Dict
from itertools import product

class MedicalTrainingDataGenerator:
    def __init__(self):
        """Initialize medical training data generator"""
        print("🤖 Initializing Medical Training Data Generator...")
        
        # Intent templates
        self.intent_templates = {
            'book_appointment': [
                "I {want/need/would like} to {book/schedule/make} an appointment",
                "Can I {see/meet with/visit} a {doctor/specialist/physician}",
                "I need to {book/schedule} with {specialty}",
                "{Book/Schedule} me with a {doctor/specialist}",
                "I {want/need} to see a {specialty} doctor",
                "Can you help me {book/schedule/make} an appointment",
                "I'd like to {make/book} an appointment for {specialty}",
                "Need to see a doctor for {condition}",
                "I have {symptom} and need to see {specialty}",
                "Emergency appointment with {specialty} please"
            ],
            'check_appointment': [
                "What appointments do I have",
                "Check my appointment {status/schedule}",
                "When is my {next/upcoming} appointment",
                "Do I have an appointment with {doctor}",
                "What time is my appointment {today/tomorrow}",
                "Can you {check/verify} my appointment",
                "I want to {see/check/review} my appointments",
                "What's my appointment schedule"
            ],
            'cancel_appointment': [
                "I need to cancel my appointment",
                "Cancel my appointment with {doctor}",
                "I want to {cancel/reschedule} my appointment",
                "Can I {change/move/reschedule} my appointment",
                "I can't make my appointment {today/tomorrow}",
                "Need to reschedule my {specialty} appointment",
                "Cancel appointment for {date/time}"
            ],
            'get_info': [
                "What are your {hours/operating hours}",
                "Where is the {clinic/hospital/office} located",
                "What's your {address/location}",
                "How much does a {consultation/visit} cost",
                "Do you accept {insurance/my insurance}",
                "What {specialties/doctors} do you have",
                "What are your phone numbers",
                "How do I get to your {office/clinic}"
            ]
        }
        
        # Medical specialties with variations
        self.specialties = {
            'cardiology': ['cardiology', 'heart doctor', 'cardiologist', 'heart specialist'],
            'dermatology': ['dermatology', 'skin doctor', 'dermatologist', 'skin specialist'],
            'pediatrics': ['pediatrics', 'pediatrician', 'children\'s doctor', 'child doctor'],
            'neurology': ['neurology', 'neurologist', 'brain doctor', 'nerve specialist'],
            'orthopedics': ['orthopedics', 'bone doctor', 'orthopedist', 'joint specialist'],
            'gynecology': ['gynecology', 'gynecologist', 'women\'s health', 'OB-GYN'],
            'psychiatry': ['psychiatry', 'psychiatrist', 'mental health', 'therapist'],
            'internal_medicine': ['internal medicine', 'general practitioner', 'family doctor', 'GP']
        }
        
        # Medical conditions and symptoms
        self.conditions = [
            'chest pain', 'headache', 'fever', 'cough', 'back pain', 'joint pain',
            'skin rash', 'anxiety', 'depression', 'high blood pressure', 'diabetes',
            'allergies', 'migraine', 'insomnia', 'fatigue', 'dizziness'
        ]
        
        # Doctor names (mock)
        self.doctor_names = [
            'Dr. Garcia', 'Dr. Martinez', 'Dr. Rodriguez', 'Dr. Lopez', 'Dr. Gonzalez',
            'Dr. Fernandez', 'Dr. Sanchez', 'Dr. Ramirez', 'Dr. Torres', 'Dr. Flores'
        ]
        
        # Time expressions
        self.time_expressions = [
            'today', 'tomorrow', 'this week', 'next week', 'Monday', 'Tuesday',
            'Wednesday', 'Thursday', 'Friday', 'morning', 'afternoon', 'evening'
        ]
        
        # Urgency indicators
        self.urgency_words = ['urgent', 'ASAP', 'emergency', 'immediately', 'soon', 'quickly']
        
        print("✅ Medical Training Data Generator initialized!")
    
    def expand_template(self, template: str, intent: str) -> List[str]:
        """Expand a template into multiple variations"""
        variations = []
        
        # Handle choice patterns like {want/need/would like}
        import re
        choice_pattern = r'\{([^}]+)\}'
        choices = re.findall(choice_pattern, template)
        
        if not choices:
            return [template]
        
        # Generate all combinations
        choice_lists = []
        for choice_str in choices:
            choice_lists.append(choice_str.split('/'))
        
        # Create all combinations
        for combination in product(*choice_lists):
            variation = template
            for i, choice in enumerate(combination):
                variation = re.sub(r'\{[^}]+\}', choice, variation, count=1)
            variations.append(variation)
        
        return variations
    
    def inject_medical_entities(self, template: str) -> List[str]:
        """Inject medical entities into templates"""
        variations = []
        
        # Replace {specialty} placeholder
        if '{specialty}' in template:
            for specialty_group in self.specialties.values():
                for specialty in specialty_group:
                    variations.append(template.replace('{specialty}', specialty))
        
        # Replace {condition} placeholder
        elif '{condition}' in template:
            for condition in self.conditions:
                variations.append(template.replace('{condition}', condition))
        
        # Replace {doctor} placeholder
        elif '{doctor}' in template:
            for doctor in self.doctor_names:
                variations.append(template.replace('{doctor}', doctor))
        
        # Replace {symptom} placeholder
        elif '{symptom}' in template:
            for condition in self.conditions:
                variations.append(template.replace('{symptom}', condition))
        
        else:
            variations.append(template)
        
        return variations
    
    def generate_training_data(self, samples_per_intent: int = 200) -> Dict:
        """Generate complete training dataset"""
        print(f"🔄 Generating {samples_per_intent} samples per intent...")
        
        training_data = {
            'intents': [],
            'entities': self._generate_entity_definitions(),
            'conversation_patterns': [],
            'metadata': {
                'total_samples': 0,
                'generation_method': 'synthetic_with_medical_validation',
                'specialties_covered': list(self.specialties.keys())
            }
        }
        
        # Generate samples for each intent
        for intent_name, templates in self.intent_templates.items():
            intent_samples = []
            
            for template in templates:
                # Expand template choices
                expanded = self.expand_template(template, intent_name)
                
                for expanded_template in expanded:
                    # Inject medical entities
                    medical_variations = self.inject_medical_entities(expanded_template)
                    
                    for variation in medical_variations:
                        # Add urgency variations for booking
                        if intent_name == 'book_appointment' and random.random() < 0.3:
                            urgency = random.choice(self.urgency_words)
                            variation = f"{variation} {urgency}"
                        
                        # Add time variations
                        if random.random() < 0.4:
                            time_expr = random.choice(self.time_expressions)
                            variation = f"{variation} {time_expr}"
                        
                        intent_samples.append({
                            'text': variation.strip(),
                            'intent': intent_name,
                            'entities': self._extract_entities_from_text(variation)
                        })
                        
                        if len(intent_samples) >= samples_per_intent:
                            break
                    
                    if len(intent_samples) >= samples_per_intent:
                        break
                
                if len(intent_samples) >= samples_per_intent:
                    break
            
            training_data['intents'].append({
                'name': intent_name,
                'samples': intent_samples[:samples_per_intent]
            })
        
        # Calculate total samples
        total_samples = sum(len(intent['samples']) for intent in training_data['intents'])
        training_data['metadata']['total_samples'] = total_samples
        
        print(f"✅ Generated {total_samples} training samples across {len(self.intent_templates)} intents")
        return training_data
    
    def _generate_entity_definitions(self) -> Dict:
        """Generate entity definitions for Botpress"""
        return {
            'specialties': {
                'values': list(self.specialties.keys()),
                'synonyms': self.specialties
            },
            'doctors': {
                'values': self.doctor_names
            },
            'conditions': {
                'values': self.conditions
            },
            'urgency': {
                'values': self.urgency_words
            },
            'time_expressions': {
                'values': self.time_expressions
            }
        }
    
    def _extract_entities_from_text(self, text: str) -> List[Dict]:
        """Extract entities from generated text"""
        entities = []
        text_lower = text.lower()
        
        # Extract specialties
        for specialty, variations in self.specialties.items():
            for variation in variations:
                if variation.lower() in text_lower:
                    entities.append({
                        'entity': 'specialty',
                        'value': specialty,
                        'text': variation
                    })
                    break
        
        # Extract doctors
        for doctor in self.doctor_names:
            if doctor.lower() in text_lower:
                entities.append({
                    'entity': 'doctor',
                    'value': doctor,
                    'text': doctor
                })
        
        # Extract conditions
        for condition in self.conditions:
            if condition.lower() in text_lower:
                entities.append({
                    'entity': 'condition',
                    'value': condition,
                    'text': condition
                })
        
        return entities
    
    def save_training_data(self, training_data: Dict, filename: str):
        """Save training data to JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(training_data, f, indent=2, ensure_ascii=False)
        print(f"💾 Training data saved to {filename}")
    
    def generate_botpress_format(self, training_data: Dict) -> Dict:
        """Convert to Botpress-specific format"""
        botpress_data = {
            'intents': {},
            'entities': {},
            'slots': {}
        }
        
        # Convert intents
        for intent in training_data['intents']:
            botpress_data['intents'][intent['name']] = {
                'utterances': [sample['text'] for sample in intent['samples']],
                'slots': []
            }
        
        # Convert entities
        for entity_name, entity_data in training_data['entities'].items():
            botpress_data['entities'][entity_name] = {
                'values': entity_data.get('values', []),
                'synonyms': entity_data.get('synonyms', {})
            }
        
        return botpress_data

# Generate training data
if __name__ == "__main__":
    generator = MedicalTrainingDataGenerator()
    
    # Generate comprehensive training data
    print("\n🚀 Starting synthetic data generation...")
    training_data = generator.generate_training_data(samples_per_intent=250)
    
    # Save in multiple formats
    generator.save_training_data(training_data, 'medical_training_data.json')
    
    # Generate Botpress format
    botpress_data = generator.generate_botpress_format(training_data)
    generator.save_training_data(botpress_data, 'botpress_training_data.json')
    
    # Show summary
    print(f"\n📊 Training Data Summary:")
    print(f"Total Intents: {len(training_data['intents'])}")
    print(f"Total Samples: {training_data['metadata']['total_samples']}")
    print(f"Specialties Covered: {len(training_data['metadata']['specialties_covered'])}")
    print(f"Entity Types: {len(training_data['entities'])}")
    
    # Show sample data
    print(f"\n🔍 Sample Training Examples:")
    for intent in training_data['intents'][:2]:
        print(f"\n{intent['name'].upper()}:")
        for i, sample in enumerate(intent['samples'][:3]):
            print(f"  {i+1}. {sample['text']}")
        print(f"  ... and {len(intent['samples'])-3} more examples")