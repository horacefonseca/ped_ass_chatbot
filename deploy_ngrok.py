#!/usr/bin/env python3
"""
NGrok Deployment Script for Baptist Health Hospital Doral Medical Chatbot
Streamlit Web Application Deployment

This script automatically deploys the Streamlit chatbot using ngrok for public access.
"""

import subprocess
import sys
import time
import os
from pathlib import Path

def install_requirements():
    """Install required packages"""
    requirements = [
        'streamlit>=1.28.0',
        'pyngrok>=6.0.0',
        'requests>=2.31.0',
        'python-dateutil>=2.8.2'
    ]
    
    print("🔧 Installing required packages...")
    for package in requirements:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"✅ Installed {package}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {package}: {e}")
            return False
    
    print("✅ All packages installed successfully!")
    return True

def setup_ngrok():
    """Setup ngrok tunnel"""
    try:
        from pyngrok import ngrok, conf
        
        # Kill any existing ngrok processes
        print("🔄 Cleaning up existing ngrok processes...")
        try:
            ngrok.kill()
        except:
            pass
        
        # Start ngrok tunnel on port 8501 (Streamlit default)
        print("🚀 Starting ngrok tunnel...")
        tunnel = ngrok.connect(8501, "http")
        
        public_url = tunnel.public_url
        print(f"🌐 Public URL: {public_url}")
        print(f"📱 Share this URL to access the Baptist Health chatbot!")
        
        return tunnel, public_url
        
    except ImportError:
        print("❌ pyngrok not available. Installing...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyngrok'])
        return setup_ngrok()
    except Exception as e:
        print(f"❌ Error setting up ngrok: {e}")
        return None, None

def run_streamlit():
    """Run the Streamlit application"""
    app_path = Path(__file__).parent / "streamlit_app.py"
    
    if not app_path.exists():
        print(f"❌ Streamlit app not found at {app_path}")
        return False
    
    print("🎯 Starting Streamlit application...")
    print(f"📂 App location: {app_path}")
    
    # Run Streamlit
    cmd = [
        sys.executable, '-m', 'streamlit', 'run', str(app_path),
        '--server.port=8501',
        '--server.address=0.0.0.0',
        '--server.headless=true',
        '--browser.gatherUsageStats=false'
    ]
    
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n👋 Deployment stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running Streamlit: {e}")
        return False
    
    return True

def main():
    """Main deployment function"""
    print("🏥 Baptist Health Hospital Doral - Medical Chatbot Deployment")
    print("=" * 60)
    print("🚀 Starting deployment with ngrok...")
    
    # Step 1: Install requirements
    if not install_requirements():
        print("❌ Failed to install requirements. Exiting.")
        return
    
    # Step 2: Setup ngrok tunnel
    tunnel, public_url = setup_ngrok()
    if not tunnel:
        print("❌ Failed to setup ngrok tunnel. Exiting.")
        return
    
    # Step 3: Display deployment information
    print("\n" + "=" * 60)
    print("✅ DEPLOYMENT SUCCESSFUL!")
    print("=" * 60)
    print(f"🌐 Public URL: {public_url}")
    print(f"🏥 Baptist Health Hospital Doral Medical Chatbot")
    print(f"📱 Share this URL with patients and staff")
    print("=" * 60)
    print("\n⚙️ Starting Streamlit server...")
    print("⚠️  Press Ctrl+C to stop the deployment")
    print("\n🔄 Waiting for Streamlit to start...")
    
    # Give ngrok a moment to fully initialize
    time.sleep(3)
    
    # Step 4: Run Streamlit
    try:
        run_streamlit()
    finally:
        # Cleanup
        print("\n🧹 Cleaning up...")
        try:
            from pyngrok import ngrok
            ngrok.kill()
            print("✅ NGrok tunnel closed")
        except:
            pass
        print("👋 Deployment ended")

if __name__ == "__main__":
    main()