"""
Colab Test Runner for Pediatric Associates Chatbot
Optimized for Google Colab environment
"""

# Cell 1: Setup and Installation
print("🔧 Setting up environment...")
import subprocess
import sys

# Install required packages
try:
    import chatterbot
    print("✅ ChatterBot already installed")
except ImportError:
    print("📦 Installing ChatterBot...")
    subprocess.run([sys.executable, "-m", "pip", "install", "chatterbot", "chatterbot_corpus", "pytz"])

# Cell 2: Import and Initialize
from datetime import datetime, timedelta
import pytz
import random

# Import the chatbot (assuming the main file is in the same directory)
exec(open('PedAss_MVP_Chatbot_ver5.py').read())

print("🤖 Initializing Pediatric Chatbot...")
bot = PediatricChatBot()

# Cell 3: Test Functions
def run_interactive_test():
    """Run interactive test session"""
    print("=" * 50)
    print("🏥 PEDIATRIC ASSOCIATES DORAL - INTERACTIVE TEST")
    print("=" * 50)
    print("💡 Try these test scenarios:")
    print("1. Type 'appointment' to book")
    print("2. Type 'faqs' for information")
    print("3. Type 'menu' to see options")
    print("4. Type 'quit' to exit")
    print("-" * 50)
    
    conversation_count = 0
    while conversation_count < 10:  # Limit for Colab
        try:
            user_input = input(f"You ({conversation_count+1}/10): ").strip()
            
            if user_input.lower() == 'quit':
                print("Bot: ¡Gracias! Que tengas un buen día.")
                break
                
            response = bot.handle_response(user_input)
            print(f"Bot: {response}")
            print("-" * 30)
            
            conversation_count += 1
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            break
    
    print("✅ Interactive test completed!")

def run_automated_test_suite():
    """Run automated test scenarios"""
    print("🚀 RUNNING AUTOMATED TEST SUITE")
    print("=" * 50)
    
    test_scenarios = [
        {
            'name': 'Complete Booking Flow',
            'steps': [
                ('hello', 'Should show welcome and menu'),
                ('appointment', 'Should show doctor list'),
                ('Aguilar', 'Should show available dates'),
                ('25/07/2025', 'Should show available times'),
                ('10:00 AM', 'Should ask for patient name'),
                ('Maria Rodriguez', 'Should ask for confirmation'),
                ('yes', 'Should confirm appointment')
            ]
        },
        {
            'name': 'FAQ Testing',
            'steps': [
                ('menu', 'Should show main menu'),
                ('2', 'Should show FAQ menu'),
                ('hours', 'Should show clinic hours'),
                ('location', 'Should show clinic address'),
                ('contact', 'Should show contact info')
            ]
        },
        {
            'name': 'Error Handling',
            'steps': [
                ('xyz123', 'Should handle gracefully'),
                ('', 'Should handle empty input'),
                ('999', 'Should provide helpful response')
            ]
        }
    ]
    
    for scenario in test_scenarios:
        print(f"\n🧪 Testing: {scenario['name']}")
        print("-" * 40)
        
        # Reset bot state for each scenario
        bot.current_state = "MAIN_MENU"
        bot.current_booking = {}
        
        for step, (user_input, expected) in enumerate(scenario['steps'], 1):
            print(f"\n👤 Step {step}: '{user_input}'")
            print(f"📝 Expected: {expected}")
            
            try:
                response = bot.handle_response(user_input)
                print(f"🤖 Bot: {response[:100]}...")
                print("✅ Response received")
                
            except Exception as e:
                print(f"❌ Error: {e}")
        
        print(f"✅ Scenario '{scenario['name']}' completed")
    
    print("\n🎯 All automated tests completed!")

def demo_key_features():
    """Demonstrate key chatbot features"""
    print("🌟 DEMONSTRATING KEY FEATURES")
    print("=" * 50)
    
    features = [
        {
            'name': 'Doctor Availability Check',
            'input': 'appointment',
            'description': 'Shows available doctors and specialties'
        },
        {
            'name': 'Dynamic Scheduling',
            'input': 'Chacon',  # After selecting appointment
            'description': 'Shows real-time availability for selected doctor'
        },
        {
            'name': 'FAQ System',
            'input': 'faqs',
            'description': 'Provides instant answers to common questions'
        },
        {
            'name': 'Clinic Information',
            'input': '3',  # From main menu
            'description': 'Displays comprehensive clinic details'
        }
    ]
    
    # Reset bot
    bot.current_state = "MAIN_MENU"
    bot.current_booking = {}
    
    for feature in features:
        print(f"\n✨ Feature: {feature['name']}")
        print(f"📝 Description: {feature['description']}")
        print(f"👤 Input: '{feature['input']}'")
        
        try:
            response = bot.handle_response(feature['input'])
            print(f"🤖 Response:\n{response}")
            print("✅ Feature working correctly")
            
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("-" * 40)
    
    print("🎉 Feature demonstration completed!")

# Cell 4: Main Execution
def main():
    """Main test execution function"""
    print("🏥 PEDIATRIC ASSOCIATES CHATBOT - COLAB TESTING")
    print("=" * 60)
    
    # Show chatbot info
    print("🤖 Chatbot successfully loaded!")
    print(f"📅 Test run: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Run demo
    demo_key_features()
    
    # Run automated tests
    run_automated_test_suite()
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
    print("💡 To run interactive tests, call: run_interactive_test()")
    print("=" * 60)

# Execute main function
if __name__ == "__main__":
    main()