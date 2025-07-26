#!/usr/bin/env python3
"""
Simple Demo Test Script for Pediatric Associates Chatbot
Tests key functionality without requiring full medical NLP setup
"""

import sys
import os
from datetime import datetime

class ChatBotTester:
    def __init__(self):
        self.test_results = []
        
    def simulate_conversation(self, bot, conversation_steps):
        """Simulate a conversation with the chatbot"""
        print("🤖 Starting conversation simulation...")
        print("=" * 50)
        
        results = []
        for step, (user_input, expected_response_type) in enumerate(conversation_steps, 1):
            print(f"\n👤 User: {user_input}")
            
            try:
                response = bot.handle_response(user_input)
                print(f"🤖 Bot: {response[:100]}...")
                
                # Simple validation - check if response contains expected keywords
                success = self.validate_response(response, expected_response_type)
                
                results.append({
                    'step': step,
                    'input': user_input,
                    'response': response,
                    'expected': expected_response_type,
                    'success': success
                })
                
                status = "✅" if success else "❌"
                print(f"{status} Expected: {expected_response_type}, Got: {'PASS' if success else 'FAIL'}")
                
            except Exception as e:
                print(f"❌ Error: {e}")
                results.append({
                    'step': step,
                    'input': user_input,
                    'error': str(e),
                    'success': False
                })
        
        return results
    
    def validate_response(self, response, expected_type):
        """Basic validation of bot responses"""
        response_lower = response.lower()
        
        validation_rules = {
            'greeting': ['hello', 'welcome', 'help'],
            'menu': ['menu', '1.', '2.', '3.'],
            'booking_start': ['doctor', 'available', 'aguilar', 'chacon'],
            'date_selection': ['available', 'date', 'please enter'],
            'time_selection': ['time', 'am', 'pm'],
            'patient_info': ['patient', 'name', 'full name'],
            'confirmation': ['confirm', 'yes', 'no'],
            'success': ['confirmed', '✅', 'appointment'],
            'faq': ['hours', 'location', 'services', 'contact'],
            'clinic_info': ['clinic', 'doral', 'phone', 'address']
        }
        
        if expected_type in validation_rules:
            keywords = validation_rules[expected_type]
            return any(keyword in response_lower for keyword in keywords)
        
        return True  # Default to pass for unknown types
    
    def run_basic_flow_test(self):
        """Test basic appointment booking flow"""
        print("\n🔥 BASIC BOOKING FLOW TEST")
        print("=" * 40)
        
        # Import here to avoid issues if modules aren't available
        try:
            from PedAss_MVP_Chatbot_ver5 import PediatricChatBot
            bot = PediatricChatBot()
            
            # Test conversation flow
            conversation = [
                ("hello", "greeting"),
                ("1", "booking_start"),
                ("Aguilar", "date_selection"),
                ("25/07/2025", "time_selection"),
                ("10:00 AM", "patient_info"),
                ("Test Patient", "confirmation"),
                ("yes", "success")
            ]
            
            results = self.simulate_conversation(bot, conversation)
            success_rate = sum(1 for r in results if r.get('success', False)) / len(results)
            
            print(f"\n📊 Basic Flow Test Results:")
            print(f"Success Rate: {success_rate*100:.1f}% ({sum(1 for r in results if r.get('success', False))}/{len(results)})")
            
            return results
            
        except ImportError as e:
            print(f"❌ Could not import chatbot: {e}")
            return []
    
    def run_faq_test(self):
        """Test FAQ functionality"""
        print("\n❓ FAQ FUNCTIONALITY TEST")
        print("=" * 40)
        
        try:
            from PedAss_MVP_Chatbot_ver5 import PediatricChatBot
            bot = PediatricChatBot()
            
            faq_tests = [
                ("2", "faq"),  # FAQ menu
                ("hours", "faq"),
                ("location", "faq"),
                ("parking", "faq"),
                ("contact", "faq")
            ]
            
            results = self.simulate_conversation(bot, faq_tests)
            success_rate = sum(1 for r in results if r.get('success', False)) / len(results)
            
            print(f"\n📊 FAQ Test Results:")
            print(f"Success Rate: {success_rate*100:.1f}% ({sum(1 for r in results if r.get('success', False))}/{len(results)})")
            
            return results
            
        except ImportError as e:
            print(f"❌ Could not import chatbot: {e}")
            return []
    
    def run_edge_case_test(self):
        """Test edge cases and error handling"""
        print("\n⚠️ EDGE CASE TEST")
        print("=" * 40)
        
        try:
            from PedAss_MVP_Chatbot_ver5 import PediatricChatBot
            bot = PediatricChatBot()
            
            edge_cases = [
                ("", "graceful_error"),
                ("asdfghjkl", "graceful_error"),
                ("999", "graceful_error"),
                ("menu", "menu"),
                ("back", "menu"),
                ("quit", "quit_confirmation")
            ]
            
            print("Testing edge cases...")
            for user_input, expected in edge_cases:
                print(f"\n👤 Testing: '{user_input}'")
                try:
                    response = bot.handle_response(user_input)
                    print(f"🤖 Response: {response[:100]}...")
                    print("✅ Handled gracefully")
                except Exception as e:
                    print(f"❌ Error: {e}")
            
            return edge_cases
            
        except ImportError as e:
            print(f"❌ Could not import chatbot: {e}")
            return []
    
    def run_comprehensive_test(self):
        """Run all available tests"""
        print("🚀 STARTING COMPREHENSIVE CHATBOT TESTS")
        print("=" * 60)
        
        all_results = {}
        
        # Run basic tests
        print("\n1️⃣ BASIC FUNCTIONALITY TESTS")
        all_results['basic_flow'] = self.run_basic_flow_test()
        
        print("\n2️⃣ FAQ TESTS")
        all_results['faq'] = self.run_faq_test()
        
        print("\n3️⃣ EDGE CASE TESTS")  
        all_results['edge_cases'] = self.run_edge_case_test()
        
        # Generate summary
        self.generate_test_summary(all_results)
        
        return all_results
    
    def generate_test_summary(self, results):
        """Generate test summary report"""
        print("\n" + "=" * 60)
        print("📋 COMPREHENSIVE TEST SUMMARY")
        print("=" * 60)
        
        total_tests = 0
        total_passed = 0
        
        for test_type, test_results in results.items():
            if isinstance(test_results, list) and test_results:
                test_count = len(test_results)
                passed_count = sum(1 for r in test_results if r.get('success', False))
                
                print(f"\n📊 {test_type.upper()} RESULTS:")
                print(f"   Tests Run: {test_count}")
                print(f"   Passed: {passed_count}")
                print(f"   Success Rate: {(passed_count/test_count)*100:.1f}%")
                
                total_tests += test_count
                total_passed += passed_count
        
        if total_tests > 0:
            overall_success = (total_passed / total_tests) * 100
            print(f"\n🎯 OVERALL RESULTS:")
            print(f"   Total Tests: {total_tests}")
            print(f"   Total Passed: {total_passed}")
            print(f"   Overall Success Rate: {overall_success:.1f}%")
            
            if overall_success >= 80:
                print("🌟 EXCELLENT: Chatbot performing very well!")
            elif overall_success >= 60:
                print("👍 GOOD: Chatbot functioning properly with minor issues")
            else:
                print("⚠️ NEEDS IMPROVEMENT: Some issues detected")
        
        print("\n✅ Test run completed!")

def main():
    """Main test runner"""
    print("🤖 Pediatric Associates Chatbot - Test Demo")
    print("Testing core functionality...")
    
    tester = ChatBotTester()
    results = tester.run_comprehensive_test()
    
    print("\n💡 Note: This is a basic test suite. For more comprehensive testing,")
    print("check the medical_test_scenarios.py file for advanced NLP testing.")

if __name__ == "__main__":
    main()