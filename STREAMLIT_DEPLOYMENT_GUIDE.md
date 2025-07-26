# 🚀 Baptist Health Hospital Doral Chatbot - Streamlit Deployment Guide

## 📋 Overview

This guide explains how to deploy the Baptist Health Hospital Doral medical chatbot as a standalone Streamlit web application using ngrok for public access.

---

## 🗂️ Files Created

### 1. **`streamlit_app.py`** - Main Application
- Complete standalone Streamlit web application
- Baptist Health Hospital Doral branding and functionality
- Medical appointment booking system
- Real-time chat interface
- Database management with corruption prevention
- Medical NLP processing

### 2. **`deploy_ngrok.py`** - Deployment Script
- Automated deployment with ngrok
- Package installation
- Public URL generation
- One-command deployment

### 3. **`requirements.txt`** - Dependencies
- All required Python packages
- Version specifications
- Easy pip installation

---

## 🚀 Quick Deployment

### Option 1: Automated Deployment (Recommended)
```bash
python deploy_ngrok.py
```

### Option 2: Manual Deployment
```bash
# Install requirements
pip install -r requirements.txt

# Run Streamlit app
streamlit run streamlit_app.py
```

---

## 📦 Installation Requirements

### Python Packages
- `streamlit>=1.28.0` - Web application framework
- `pyngrok>=6.0.0` - ngrok tunnel management
- `requests>=2.31.0` - HTTP requests
- `python-dateutil>=2.8.2` - Date/time parsing

### System Requirements
- Python 3.8 or higher
- Internet connection for ngrok
- 50MB+ available disk space

---

## 🎯 Deployment Steps

### Step 1: Prepare Environment
```bash
# Navigate to project directory
cd C:\Users\emman\Downloads\ped_ass_chatbot

# Verify files exist
dir streamlit_app.py
dir deploy_ngrok.py
dir requirements.txt
```

### Step 2: Run Deployment
```bash
# Option A: Automated deployment
python deploy_ngrok.py

# Option B: Manual deployment
pip install -r requirements.txt
streamlit run streamlit_app.py --server.port=8501
```

### Step 3: Access Application
- **Local Access**: http://localhost:8501
- **Public Access**: Use ngrok URL provided by deployment script
- **Share URL**: Give ngrok URL to patients and staff

---

## 🏥 Application Features

### 🤖 **Medical Chatbot Capabilities**
- **Appointment Booking**: Complete end-to-end booking flow
- **Medical NLP**: Specialized medical terminology processing
- **Emergency Detection**: Safety protocols for urgent cases
- **Baptist Health Integration**: Complete hospital information
- **Session Management**: 3-minute timeout for security

### 💬 **Chat Interface Features**
- **Real-time Conversation**: Instant responses
- **Conversation History**: Maintains chat context
- **Quick Actions**: Sidebar shortcuts
- **Suggestions**: Smart response suggestions
- **Mobile Responsive**: Works on all devices

### 🗄️ **Database Features**
- **SQLite Integration**: Lightweight, efficient storage
- **Corruption Prevention**: Bulletproof database design
- **Doctor Management**: Complete physician database
- **Appointment Tracking**: Full lifecycle management
- **Data Persistence**: Reliable data storage

---

## 🔧 Configuration Options

### Streamlit Configuration
```bash
# Custom port
streamlit run streamlit_app.py --server.port=8502

# Custom host
streamlit run streamlit_app.py --server.address=192.168.1.100

# Disable browser opening
streamlit run streamlit_app.py --server.headless=true
```

### NGrok Configuration
```python
# In deploy_ngrok.py, modify:
tunnel = ngrok.connect(8501, "http")  # Change port here
```

---

## 🌐 Public Access with NGrok

### Automatic NGrok Setup
The `deploy_ngrok.py` script automatically:
1. Installs pyngrok if needed
2. Kills existing ngrok processes
3. Creates new tunnel on port 8501
4. Displays public URL
5. Starts Streamlit application

### Manual NGrok Setup
```bash
# Install ngrok separately
pip install pyngrok

# Create tunnel manually
python -c "from pyngrok import ngrok; print(ngrok.connect(8501))"
```

### NGrok URL Format
```
https://abc123.ngrok.io
```
- Share this URL for public access
- URL changes each time ngrok restarts
- Free ngrok accounts have session limits

---

## 🏥 Baptist Health Hospital Doral Configuration

### Hospital Information
```python
CLINIC_NAME = "Baptist Health Hospital Doral"
CLINIC_PHONE = "786-595-3900"
CLINIC_ADDRESS = "9500 NW 58 Street, Doral, FL 33178"
BILLING_PHONE = "786-596-6507"
INSURANCE_PHONE = "786-662-7667"
```

### Available Doctors
- **Cardiology**: Dr. Garcia, Dr. Martinez
- **Dermatology**: Dr. Rodriguez, Dr. Lopez
- **Pediatrics**: Dr. Gonzalez
- **Neurology**: Dr. Fernandez
- **Orthopedics**: Dr. Sanchez
- **Gynecology**: Dr. Ramirez
- **Psychiatry**: Dr. Torres
- **Internal Medicine**: Dr. Flores

---

## 🧪 Testing the Application

### Test Scenarios

#### 1. **Complete Appointment Booking**
```
User: "Hello"
User: "I need an appointment with cardiology"
User: "Dr. Garcia"
User: "Maria Rodriguez"
User: "786-595-3900"
User: "10:00"
```

#### 2. **Hospital Information**
```
User: "What are your hours?"
User: "Where are you located?"
User: "What's your phone number?"
```

#### 3. **Emergency Detection**
```
User: "I'm having chest pain emergency!"
```

### Expected Results
- ✅ Smooth conversation flow
- ✅ Baptist Health branding displayed
- ✅ Appointment confirmation with ID
- ✅ Database persistence
- ✅ Emergency safety protocols

---

## 🔍 Troubleshooting

### Common Issues

#### **Port Already in Use**
```bash
# Error: Port 8501 is already in use
# Solution: Use different port
streamlit run streamlit_app.py --server.port=8502
```

#### **NGrok Connection Failed**
```bash
# Error: ngrok tunnel failed
# Solution: Check internet connection and try again
python deploy_ngrok.py
```

#### **Database Corruption**
```bash
# Error: Database disk image is malformed
# Solution: The app automatically handles this with fresh database creation
# No action needed - corruption prevention is built-in
```

#### **Streamlit Not Found**
```bash
# Error: streamlit command not found
# Solution: Install streamlit
pip install streamlit>=1.28.0
```

### Debugging Steps
1. **Check Python Version**: `python --version` (requires 3.8+)
2. **Verify Installation**: `pip list | grep streamlit`
3. **Test Local Access**: http://localhost:8501
4. **Check Logs**: Streamlit displays errors in terminal
5. **Restart Application**: Ctrl+C and run again

---

## 📊 Performance Optimization

### Streamlit Caching
The application uses `@st.cache_resource` for:
- Database initialization
- NLP pipeline loading
- Chatbot instantiation

### Memory Management
- In-memory database fallback for reliability
- Session state management
- Conversation history cleanup

### Load Testing
```bash
# Test multiple concurrent users
# Use tools like Apache Bench or Locust for load testing
```

---

## 🔒 Security Considerations

### Data Protection
- **Local Database**: SQLite files stay on server
- **Session Isolation**: Each user has separate session
- **Timeout Management**: 3-minute automatic logout
- **Input Validation**: Phone numbers, names sanitized

### Production Deployment
For production use, consider:
- **HTTPS**: Use proper SSL certificates
- **Authentication**: Add user login system
- **Rate Limiting**: Prevent abuse
- **Monitoring**: Log usage and errors
- **Backup**: Regular database backups

---

## 🚀 Production Deployment Options

### Cloud Platforms
1. **Streamlit Cloud**: Direct GitHub integration
2. **Heroku**: Easy cloud deployment
3. **AWS/Azure**: Enterprise-grade hosting
4. **Docker**: Containerized deployment

### Example Docker Deployment
```dockerfile
FROM python:3.9-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "streamlit_app.py"]
```

---

## 📈 Monitoring and Analytics

### Streamlit Analytics
- Built-in usage statistics
- Session tracking
- Error monitoring

### Custom Monitoring
Add to `streamlit_app.py`:
```python
# Log appointments booked
st.session_state.appointments_booked = st.session_state.get('appointments_booked', 0) + 1

# Track user interactions
st.session_state.interaction_count = st.session_state.get('interaction_count', 0) + 1
```

---

## 🆘 Support and Maintenance

### Regular Maintenance
- **Database Cleanup**: Clear old sessions periodically
- **Log Rotation**: Manage log file sizes
- **Updates**: Keep packages updated
- **Monitoring**: Check application health

### Getting Help
- **Streamlit Docs**: https://docs.streamlit.io
- **NGrok Docs**: https://ngrok.com/docs
- **Application Issues**: Check terminal output for errors

---

## ✅ Deployment Checklist

### Pre-Deployment
- [ ] Python 3.8+ installed
- [ ] All files present (`streamlit_app.py`, `deploy_ngrok.py`, `requirements.txt`)
- [ ] Internet connection available
- [ ] Port 8501 available

### During Deployment
- [ ] Run `python deploy_ngrok.py`
- [ ] Note the ngrok public URL
- [ ] Test local access (http://localhost:8501)
- [ ] Test public access (ngrok URL)

### Post-Deployment
- [ ] Share ngrok URL with users
- [ ] Monitor application logs
- [ ] Test all chatbot features
- [ ] Verify Baptist Health branding
- [ ] Confirm database functionality

---

## 🎉 Success Indicators

### Application Running Successfully
✅ **Streamlit server started on port 8501**  
✅ **NGrok tunnel created with public URL**  
✅ **Baptist Health branding displayed**  
✅ **Chatbot responding to messages**  
✅ **Database initialization successful**  
✅ **Medical appointment booking functional**  

### Ready for Production Use
The Baptist Health Hospital Doral medical chatbot is now accessible via web browser and ready to serve patients with professional medical appointment booking and information services!

---

*Baptist Health Hospital Doral Medical Chatbot - Streamlit Deployment v1.0*  
*Ready for production deployment with ngrok public access*