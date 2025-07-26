# 🏗️ Diagramas de Arquitectura - Medical Chatbot

## 📋 Vista General del Sistema

```mermaid
graph TB
    subgraph "Frontend Interface"
        A[Usuario] --> B[Chat Interface]
        B --> C[Google Colab / Web Interface]
    end
    
    subgraph "Core Chatbot Engine"
        D[Message Processor] --> E[NLP Pipeline]
        E --> F[Conversation State Manager]
        F --> G[Response Generator]
    end
    
    subgraph "NLP & AI Layer"
        H[BioClinicalBERT] --> I[Medical Entity Extraction]
        J[Rule-based Fallback] --> I
        I --> K[Intent Classification]
        K --> L[Medical Context Analysis]
    end
    
    subgraph "Data Layer"
        M[(SQLite Database)]
        N[Doctors Table]
        O[Appointments Table]
        P[Specialties Table]
        M --> N
        M --> O
        M --> P
    end
    
    subgraph "External Integrations"
        Q[Botpress API]
        R[Emergency Services Alert]
        S[External Calendar Systems]
    end
    
    C --> D
    D --> H
    D --> J
    F --> M
    G --> Q
    L --> R
    G --> B
    
    style H fill:#e1f5fe,stroke:#0277bd
    style M fill:#f3e5f5,stroke:#7b1fa2
    style Q fill:#e8f5e8,stroke:#388e3c
    style R fill:#ffebee,stroke:#d32f2f
```

## 🧠 Arquitectura del NLP Pipeline

```mermaid
graph LR
    subgraph "Input Processing"
        A[Raw User Input] --> B[Text Preprocessing]
        B --> C[Language Detection]
    end
    
    subgraph "Primary NLP Engine"
        D[BioClinicalBERT Tokenizer] --> E[Medical Term Recognition]
        E --> F[Contextualized Embeddings]
    end
    
    subgraph "Fallback NLP Engine"
        G[Rule-Based Parser] --> H[Pattern Matching]
        H --> I[Medical Dictionary Lookup]
    end
    
    subgraph "Entity Extraction"
        J[Medical Specialties] --> K[Entity Consolidation]
        L[Symptoms & Conditions] --> K
        M[Doctor Names] --> K
        N[Urgency Indicators] --> K
    end
    
    subgraph "Intent Analysis"
        O[Appointment Booking] --> P[Intent Classification]
        Q[Information Request] --> P
        R[Emergency Detection] --> P
        S[Greeting/Chitchat] --> P
    end
    
    subgraph "Output Generation"
        T[Structured NLP Result] --> U[Medical Context]
        U --> V[Conversation Routing]
    end
    
    C --> D
    C --> G
    
    F --> J
    F --> L
    I --> J
    I --> L
    
    F --> M
    F --> N
    I --> M
    I --> N
    
    K --> O
    K --> Q
    K --> R
    K --> S
    
    P --> T
    
    style D fill:#bbdefb
    style G fill:#c8e6c9
    style K fill:#fff3e0
    style P fill:#fce4ec
```

## 🔄 Flujo de Estados de Conversación

```mermaid
stateDiagram-v2
    [*] --> Idle
    
    Idle --> Emergency : emergency_keywords_detected
    Idle --> CollectingSpecialty : book_appointment_intent
    Idle --> ProvidingInfo : info_request_intent
    Idle --> CheckingAppointment : check_appointment_intent
    
    CollectingSpecialty --> CollectingDoctor : specialty_provided
    CollectingSpecialty --> CollectingSpecialty : specialty_unclear
    
    CollectingDoctor --> CollectingPatientInfo : doctor_selected
    CollectingDoctor --> CollectingDoctor : doctor_unclear
    
    CollectingPatientInfo --> CollectingPhone : patient_name_provided
    
    CollectingPhone --> CollectingDateTime : phone_validated
    CollectingPhone --> CollectingPhone : phone_invalid
    
    CollectingDateTime --> ConfirmingAppointment : time_selected
    CollectingDateTime --> CollectingDateTime : time_unclear
    
    ConfirmingAppointment --> BookingComplete : confirmation_yes
    ConfirmingAppointment --> Idle : confirmation_no
    
    BookingComplete --> Idle : appointment_booked
    
    Emergency --> Idle : emergency_handled
    ProvidingInfo --> Idle : info_provided
    CheckingAppointment --> Idle : appointment_info_provided
    
    note right of Emergency
        🚨 Immediate redirect to
        emergency services
        No appointment booking
    end note
    
    note right of CollectingPhone
        📱 Validates multiple formats:
        - 3054569878
        - 305-456-9878  
        - +1 305 456 9878
    end note
```

## 🗄️ Modelo de Datos

```mermaid
erDiagram
    DOCTORS {
        int id PK
        string name
        string specialty
        string available_days
        string available_times
        int max_appointments_per_day
    }
    
    APPOINTMENTS {
        int id PK
        string patient_name
        string patient_phone
        string patient_email
        string doctor_name FK
        string specialty
        string appointment_date
        string appointment_time
        string status
        string symptoms
        string urgency_level
        datetime created_at
        datetime updated_at
    }
    
    SPECIALTIES {
        int id PK
        string name
        string description
        string common_conditions
    }
    
    CONVERSATION_SESSIONS {
        string session_id PK
        string current_state
        json appointment_data
        json context
        datetime created_at
        datetime last_activity
    }
    
    DOCTORS ||--o{ APPOINTMENTS : "has"
    SPECIALTIES ||--o{ DOCTORS : "belongs_to"
    APPOINTMENTS ||--o{ CONVERSATION_SESSIONS : "tracks"
```

## 🎯 Flujo de Procesamiento de Mensajes

```mermaid
sequenceDiagram
    participant U as Usuario
    participant I as Interface
    participant P as Message Processor
    participant N as NLP Pipeline
    participant S as State Manager
    participant D as Database
    participant B as Botpress API
    
    U->>I: Envía mensaje
    I->>P: process_message(input, session_id)
    
    P->>N: process_query(input)
    N->>N: BioClinicalBERT analysis
    N->>N: Extract medical entities
    N->>N: Classify intent
    N-->>P: NLP result
    
    P->>S: Get/update session state
    S-->>P: Current conversation state
    
    alt Emergency Detected
        P->>P: Handle emergency protocol
        P-->>I: Emergency response
    else Normal Flow
        P->>S: Update state based on intent
        
        alt Database Query Needed
            S->>D: Query doctors/appointments
            D-->>S: Results
        end
        
        S->>P: Generate appropriate response
    end
    
    P->>B: Log conversation (optional)
    P-->>I: Response with suggestions
    I-->>U: Display response
    
    Note over U,B: Full conversation context maintained
```

## 🚨 Sistema de Detección de Emergencias

```mermaid
flowchart TD
    A[Mensaje del Usuario] --> B[Análisis NLP]
    B --> C{Palabras clave de emergencia?}
    
    C -->|Sí| D[Verificación de Contexto]
    C -->|No| E[Análisis de Especialidades]
    
    D --> F{Nivel de urgencia}
    F -->|Crítico| G[🚨 EMERGENCIA INMEDIATA]
    F -->|Alto| H[⚠️ Urgente - Same Day]
    F -->|Medio| I[📋 Cita Prioritaria]
    
    E --> J{Síntomas de emergencia por especialidad?}
    J -->|Sí| H
    J -->|No| K[Flujo Normal de Citas]
    
    G --> L[Mensaje de emergencia]
    G --> M[Redirigir a 911]
    G --> N[Detener flujo de citas]
    
    H --> O[Mostrar opciones urgentes]
    H --> P[Ofrecer cita inmediata]
    
    I --> Q[Marcar como prioritario]
    I --> K
    
    K --> R[Continuar reserva normal]
    
    style G fill:#ffcdd2
    style L fill:#ffebee
    style M fill:#ffcdd2
    style H fill:#ffe0b2
    style O fill:#fff3e0
```

## 📱 Validación de Entrada

```mermaid
graph TD
    A[Input del Usuario] --> B{Tipo de validación requerida}
    
    B -->|Teléfono| C[Validar Teléfono]
    B -->|Doctor| D[Validar Doctor]
    B -->|Especialidad| E[Validar Especialidad]
    B -->|Tiempo| F[Validar Tiempo]
    
    C --> G[Regex: eliminar no-dígitos]
    G --> H{7-15 dígitos?}
    H -->|Sí| I[✅ Teléfono válido]
    H -->|No| J[❌ Solicitar formato correcto]
    
    D --> K[Buscar en base de datos]
    K --> L{Doctor existe?}
    L -->|Sí| M[✅ Doctor válido]
    L -->|No| N[Buscar coincidencia parcial]
    N --> O{Coincidencia encontrada?}
    O -->|Sí| M
    O -->|No| P[❌ Mostrar doctores disponibles]
    
    E --> Q[Buscar en especialidades médicas]
    Q --> R{Especialidad reconocida?}
    R -->|Sí| S[✅ Especialidad válida]
    R -->|No| T[❌ Mostrar especialidades disponibles]
    
    F --> U[Parsear formato de tiempo]
    U --> V{Formato válido?}
    V -->|Sí| W[Verificar disponibilidad]
    V -->|No| X[❌ Solicitar formato correcto]
    W --> Y{Tiempo disponible?}
    Y -->|Sí| Z[✅ Tiempo válido]
    Y -->|No| AA[❌ Mostrar horarios disponibles]
    
    style I fill:#c8e6c9
    style M fill:#c8e6c9
    style S fill:#c8e6c9
    style Z fill:#c8e6c9
    style J fill:#ffcdd2
    style P fill:#ffcdd2
    style T fill:#ffcdd2
    style X fill:#ffcdd2
    style AA fill:#ffcdd2
```

## 🔗 Integración con Botpress

```mermaid
graph LR
    subgraph "Chatbot Internal"
        A[Conversation Engine] --> B[Response Generator]
        B --> C[Message Formatter]
    end
    
    subgraph "Botpress Integration Layer"
        D[Botpress API Client] --> E[Authentication Handler]
        E --> F[Message Queue]
        F --> G[Error Handling]
    end
    
    subgraph "External Botpress Cloud"
        H[Botpress API Endpoint]
        I[Conversation Management]
        J[Multi-channel Distribution]
    end
    
    subgraph "External Channels"
        K[WhatsApp]
        L[Telegram]
        M[Web Widget]
        N[Mobile App]
    end
    
    C --> D
    G --> H
    H --> I
    I --> J
    J --> K
    J --> L
    J --> M
    J --> N
    
    style D fill:#e8f5e8
    style H fill:#c8e6c9
    style J fill:#a5d6a7
```

## 📊 Métricas y Monitoreo

```mermaid
graph TB
    subgraph "Data Collection"
        A[Conversation Logs] --> B[NLP Performance Metrics]
        A --> C[User Interaction Patterns]
        A --> D[Error Tracking]
    end
    
    subgraph "Analysis Engine"
        E[Intent Accuracy Calculator] --> F[Performance Dashboard]
        G[Conversation Flow Analyzer] --> F
        H[Error Rate Monitor] --> F
    end
    
    subgraph "Alerting System"
        I[Performance Thresholds] --> J[Alert Generator]
        K[Error Thresholds] --> J
        J --> L[Notification System]
    end
    
    subgraph "Reporting"
        M[Daily Reports] --> N[Management Dashboard]
        O[Weekly Analysis] --> N
        P[Monthly Trends] --> N
    end
    
    B --> E
    C --> G
    D --> H
    
    F --> I
    F --> K
    F --> M
    F --> O
    F --> P
    
    style F fill:#e3f2fd
    style J fill:#fff3e0
    style N fill:#f3e5f5
```

---

## 🎯 Puntos Clave de la Arquitectura

### 1. **Modularidad**
- Cada componente tiene responsabilidades específicas
- Fácil mantenimiento y expansión
- Intercambio de componentes sin afectar el sistema

### 2. **Redundancia Inteligente**
- BioClinicalBERT como motor principal
- Sistema basado en reglas como respaldo
- Garantiza funcionamiento continuo

### 3. **Escalabilidad**
- Base de datos SQLite para desarrollo
- Fácil migración a PostgreSQL/MySQL
- Arquitectura preparada para múltiples instancias

### 4. **Seguridad Médica**
- Detección proactiva de emergencias
- Validación estricta de datos médicos
- Logging completo para auditorías

---

*Diagramas generados para Medical Chatbot v1.0*