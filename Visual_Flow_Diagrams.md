# Visual Flow Diagrams for Baptist Health Hospital Doral Chatbot
## To be copied into Word presentation

---

## DIAGRAM 1: SYSTEM ARCHITECTURE FLOW
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   User Input    │───▶│  Botpress API    │───▶│ NLP Processing  │
│   (Patient)     │    │  Integration     │    │ BioClinicalBERT │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                         │
                                                         ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│ Response to     │◀───│ State Management │◀───│ Intent & Entity │
│    Patient      │    │ & Flow Control   │    │  Classification │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │ SQLite Database │
                       │ (Appointments & │
                       │    Doctors)     │
                       └─────────────────┘
```

---

## DIAGRAM 2: CONVERSATION STATE FLOW
```
START
  │
  ▼
┌─────────┐     user says     ┌──────────────────┐
│  IDLE   │ ────"appointment"──▶│ COLLECTING_      │
│ (Menu)  │                   │   SPECIALTY      │
└─────────┘                   └──────────────────┘
  │   ▲                              │
  │   │                              ▼
  │   │                       ┌──────────────────┐
  │   │                       │ COLLECTING_      │
  │   │                       │   DOCTOR         │
  │   │                       └──────────────────┘
  │   │                              │
  │   │                              ▼
  │   │                       ┌──────────────────┐
  │   │                       │ COLLECTING_      │
  │   │◀─── "appointment" ─────│ PATIENT_INFO     │
  │   │     "completed"        └──────────────────┘
  │   │                              │
  │   │                              ▼
  │   │                       ┌──────────────────┐
  │   │                       │ COLLECTING_      │
  │   │                       │    PHONE         │
  │   │                       └──────────────────┘
  │   │                              │
  │   │                              ▼
  │   │                       ┌──────────────────┐
  │   │                       │ COLLECTING_      │
  │   │                       │  DATE_TIME       │
  │   │                       └──────────────────┘
  │   │                              │
  │   │                              ▼
  │   │                       ┌──────────────────┐
  │   └───────────────────────│   CONFIRMING_    │
                              │  APPOINTMENT     │
                              └──────────────────┘
```

---

## DIAGRAM 3: EMERGENCY DETECTION FLOW
```
User Message Input
        │
        ▼
┌─────────────────┐
│ NLP Analysis    │
│ (BioClinicalBERT│
│ + Rule-based)   │
└─────────────────┘
        │
        ▼
┌─────────────────────────────────────┐
│   Emergency Keyword Detection?      │
│                                     │
│ Level 1: "emergency", "heart attack"│
│ Level 2: Specialty emergencies      │
│ Level 3: Symptom + urgency combo    │
└─────────────────────────────────────┘
        │                      │
    YES │                      │ NO
        ▼                      ▼
┌─────────────────┐    ┌─────────────────┐
│ 🚨 EMERGENCY    │    │ Continue Normal │
│   PROTOCOL      │    │ Appointment     │
│                 │    │     Flow        │
│ • Show alert    │    └─────────────────┘
│ • Redirect 911  │
│ • Baptist Health│
│   Emergency     │
│ • Stop booking  │
└─────────────────┘
```

---

## DIAGRAM 4: CUSTOMER SERVICE INTERACTION SAMPLE
```
Patient: "Hello, I need an appointment with cardiology"
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│ Bot: "Welcome to Baptist Health Hospital Doral!        │
│      I found you need cardiology. Available doctors:   │
│      • Dr. Garcia - Available: Mon, Tue, Wed          │
│      • Dr. Martinez - Available: Tue, Wed, Thu        │
│      Which doctor would you prefer?"                   │
└─────────────────────────────────────────────────────────┘
    │
    ▼
Patient: "Dr. Garcia"
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│ Bot: "Excellent! Dr. Garcia specializes in cardiology. │
│      What's the patient's full name?"                  │
└─────────────────────────────────────────────────────────┘
    │
    ▼
Patient: "Maria Rodriguez"
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│ Bot: "Thank you, Maria. What's your phone number?"     │
└─────────────────────────────────────────────────────────┘
    │
    ▼
Patient: "786-595-3900"
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│ Bot: "Perfect! Dr. Garcia's available times:           │
│      • 09:00 AM  • 10:00 AM                           │
│      • 11:00 AM  • 2:00 PM                            │
│      Which time works best?"                           │
└─────────────────────────────────────────────────────────┘
    │
    ▼
Patient: "10:00 AM"
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│ ✅ APPOINTMENT CONFIRMED!                              │
│ • Patient: Maria Rodriguez                             │
│ • Doctor: Dr. Garcia (Cardiology)                     │
│ • Date: February 15, 2024                             │
│ • Time: 10:00 AM                                      │
│ • Location: Baptist Health Hospital Doral             │
│ • Appointment ID: #1234                               │
│ • Confirmation call within 24 hours                   │
└─────────────────────────────────────────────────────────┘
```

---

## DIAGRAM 5: TECHNOLOGY STACK ARCHITECTURE
```
┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │Google Colab │  │   Web UI    │  │ Botpress    │         │
│  │ Interface   │  │ Interface   │  │   Cloud     │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      NLP LAYER                              │
│  ┌─────────────────┐              ┌─────────────────┐      │
│  │ BioClinicalBERT │              │ Rule-based NLP  │      │
│  │ (Primary AI)    │     +        │ (Fallback)      │      │
│  │ 87.5% Accuracy  │              │ 85% Accuracy    │      │
│  └─────────────────┘              └─────────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   BUSINESS LOGIC LAYER                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │Conversation │  │ Emergency   │  │ Appointment │         │
│  │State Manager│  │ Detection   │  │ Management  │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                     DATA LAYER                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   SQLite    │  │   Doctors   │  │Appointments │         │
│  │  Database   │  │    Table    │  │    Table    │         │
│  │(Bulletproof)│  │             │  │             │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
```

---

## DIAGRAM 6: BAPTIST HEALTH HOSPITAL DORAL INFORMATION FLOW
```
Patient Query: "What are your hours?" / "Where are you located?" / "Billing info?"
                                    │
                                    ▼
                          ┌─────────────────┐
                          │ Intent Analysis │
                          │ (get_info)      │
                          └─────────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
           ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
           │   HOURS     │ │  LOCATION   │ │   BILLING   │
           │             │ │             │ │             │
           │ Emergency:  │ │ Address:    │ │ Main Billing│
           │ 24/7        │ │ 9500 NW 58th│ │ 786-596-6507│
           │             │ │ Street      │ │             │
           │ Outpatient: │ │ Doral, FL   │ │ Insurance:  │
           │ Mon-Fri     │ │ 33178       │ │ 786-662-7667│
           │ 8AM-6PM     │ │             │ │             │
           │             │ │ Free Parking│ │ Email:      │
           │ Visitors:   │ │ Available   │ │ insurance@  │
           │ 7AM-9PM     │ │             │ │ BaptistHealth│
           └─────────────┘ └─────────────┘ └─────────────┘
                    │               │               │
                    └───────────────┼───────────────┘
                                    ▼
                    ┌─────────────────────────────────┐
                    │ Formatted Response to Patient   │
                    │ with Baptist Health branding    │
                    └─────────────────────────────────┘
```

These diagrams can be easily copied and pasted into your Word document to enhance the visual presentation of the chatbot's functionality and architecture.