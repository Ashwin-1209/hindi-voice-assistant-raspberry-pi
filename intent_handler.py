#!/usr/bin/env python3
"""
Intent Handler Module - Command Parsing and Action Execution
Processes Hindi text and maps to actions

This module:
- Parses recognized Hindi text
- Identifies user intent
- Executes appropriate actions
- Generates response text
"""

import re
from datetime import datetime
import random
import subprocess

class IntentHandler:
    """
    Handles intent recognition and command execution
    """
    
    def __init__(self):
        """Initialize the intent handler with command mappings"""
        print("🧠 Initializing Intent Handler...")
        
        # Define supported commands with Hindi patterns
        self.commands = {
            'greeting': {
                'patterns': ['नमस्ते', 'हैलो', 'प्रणाम', 'हाय'],
                'action': self._greet
            },
            'time': {
                'patterns': ['समय', 'टाइम', 'बजे', 'क्या समय'],
                'action': self._tell_time
            },
            'date': {
                'patterns': ['तारीख', 'डेट', 'दिन', 'आज'],
                'action': self._tell_date
            },
            'thanks': {
                'patterns': ['धन्यवाद', 'शुक्रिया', 'थैंक्स'],
                'action': self._respond_thanks
            },
            'exit': {
                'patterns': ['बंद', 'बाहर', 'बाय', 'रुको'],
                'action': self._exit
            },
            'weather': {
                'patterns': ['मौसम', 'वेदर', 'बारिश'],
                'action': self._tell_weather
            },
            'battery': {
                'patterns': ['बैटरी', 'चार्ज'],
                'action': self._check_battery
            },
            'volume_up': {
                'patterns': ['वॉल्यूम बढ़ाओ', 'आवाज़ बढ़ाओ', 'तेज'],
                'action': self._volume_up
            },
            'volume_down': {
                'patterns': ['वॉल्यूम घटाओ', 'आवाज़ कम', 'धीमा'],
                'action': self._volume_down
            },
            'joke': {
                'patterns': ['मज़ाक', 'जोक', 'हंसाओ'],
                'action': self._tell_joke
            },
            'help': {
                'patterns': ['मदद', 'हेल्प', 'क्या कर सकते'],
                'action': self._help
            },
            'identity': {
                'patterns': ['तुम कौन', 'आप कौन', 'नाम'],
                'action': self._tell_identity
            },
            'calculate': {
                'patterns': ['जोड़', 'गणना', 'गुणा', 'भाग'],
                'action': self._calculate
            },
            'reboot': {
                'patterns': ['रीबूट', 'रीस्टार्ट'],
                'action': self._reboot
            },
        }
        
        # Statistics
        self.command_count = {}
        for cmd in self.commands.keys():
            self.command_count[cmd] = 0
        
        print(f"   ✅ Loaded {len(self.commands)} command categories")
    
    def process(self, text):
        """
        Process recognized text and execute appropriate action
        
        Args:
            text (str): Hindi text from ASR
            
        Returns:
            tuple: (intent_name, response_text)
        """
        
        if not text:
            return 'no_input', 'मुझे कुछ सुनाई नहीं दिया'
        
        # Convert to lowercase for matching
        text_lower = text.lower().strip()
        
        # Try to match intent
        intent = self._match_intent(text_lower)
        
        if intent:
            # Update statistics
            self.command_count[intent] += 1
            
            # Execute the action
            response = self.commands[intent]['action'](text_lower)
            return intent, response
        else:
            # Unknown command
            return 'unknown', self._handle_unknown(text_lower)
    
    def _match_intent(self, text):
        """
        Match input text to an intent using pattern matching
        
        Args:
            text (str): Input text
            
        Returns:
            str: Intent name or None
        """
        
        # Check each command's patterns
        for intent_name, intent_data in self.commands.items():
            patterns = intent_data['patterns']
            
            for pattern in patterns:
                if pattern in text:
                    return intent_name
        
        return None
    
    # ==================== ACTION FUNCTIONS ====================
    
    def _greet(self, text):
        """Respond to greeting"""
        responses = [
            'नमस्ते! मैं आपकी कैसे मदद कर सकता हूं?',
            'हैलो! मुझे बताएं मैं क्या कर सकता हूं?',
            'प्रणाम! आपके लिए क्या करूं?'
        ]
        return random.choice(responses)
    
    def _tell_time(self, text):
        """Tell current time"""
        now = datetime.now()
        hour = now.hour
        minute = now.minute
        
        # Convert to 12-hour format
        if hour == 0:
            hour_12 = 12
            period = 'रात'
        elif hour < 12:
            hour_12 = hour
            period = 'सुबह'
        elif hour == 12:
            hour_12 = 12
            period = 'दोपहर'
        else:
            hour_12 = hour - 12
            period = 'शाम'
        
        return f'अभी {hour_12} बजकर {minute} मिनट {period} के हैं'
    
    def _tell_date(self, text):
        """Tell current date"""
        now = datetime.now()
        
        # Hindi months
        months_hindi = [
            'जनवरी', 'फरवरी', 'मार्च', 'अप्रैल', 'मई', 'जून',
            'जुलाई', 'अगस्त', 'सितंबर', 'अक्टूबर', 'नवंबर', 'दिसंबर'
        ]
        
        # Hindi days
        days_hindi = [
            'सोमवार', 'मंगलवार', 'बुधवार', 'गुरुवार', 
            'शुक्रवार', 'शनिवार', 'रविवार'
        ]
        
        day = now.day
        month = months_hindi[now.month - 1]
        year = now.year
        weekday = days_hindi[now.weekday()]
        
        return f'आज {weekday} है, {day} {month} {year}'
    
    def _respond_thanks(self, text):
        """Respond to thanks"""
        responses = [
            'आपका स्वागत है!',
            'कोई बात नहीं!',
            'खुशी हुई मदद करके!'
        ]
        return random.choice(responses)
    
    def _exit(self, text):
        """Handle exit command"""
        return 'अच्छा, नमस्ते! फिर मिलेंगे!'
    
    def _tell_weather(self, text):
        """Tell weather (offline - simulated data)"""
        # Since we're offline, we can't get real weather
        # Provide simulated response
        responses = [
            'मौसम सुहावना है आज',
            'आज धूप है',
            'थोड़ी बदली है आज',
            'मैं ऑफलाइन हूं, असली मौसम नहीं बता सकता'
        ]
        return random.choice(responses)
    
    def _check_battery(self, text):
        """Check battery status (for laptop Pi setups)"""
        try:
            # Try to get battery info (works on laptops/some Pis)
            result = subprocess.run(
                ['cat', '/sys/class/power_supply/BAT0/capacity'],
                capture_output=True,
                text=True,
                timeout=1
            )
            
            if result.returncode == 0:
                battery = result.stdout.strip()
                return f'बैटरी {battery} प्रतिशत है'
            else:
                return 'बैटरी की जानकारी नहीं मिली'
        except:
            return 'यह डिवाइस बैटरी पर नहीं चल रहा'
    
    def _volume_up(self, text):
        """Increase volume"""
        try:
            subprocess.run(['amixer', 'set', 'Master', '10%+'], 
                         capture_output=True, timeout=2)
            return 'वॉल्यूम बढ़ाया गया'
        except:
            return 'वॉल्यूम नहीं बदल सका'
    
    def _volume_down(self, text):
        """Decrease volume"""
        try:
            subprocess.run(['amixer', 'set', 'Master', '10%-'], 
                         capture_output=True, timeout=2)
            return 'वॉल्यूम घटाया गया'
        except:
            return 'वॉल्यूम नहीं बदल सका'
    
    def _tell_joke(self, text):
        """Tell a Hindi joke"""
        jokes = [
            'एक चूहा बोला दूसरे चूहे से, मैं प्रोग्रामर बनूंगा। दूसरा बोला क्यों? पहला बोला, चीज़ खाने के लिए!',
            'टीचर ने पूछा, पाई का मान क्या है? छात्र बोला, तीन पॉइंट वन फोर... टीचर बोला, पूरा बोलो! छात्र बोला, यही काफी है सर, पूरा पाई खाने से मोटा हो जाऊंगा!',
            'कंप्यूटर ने मोबाइल से पूछा, तुम इतने पतले कैसे हो? मोबाइल बोला, मैं रोज़ चार्ज होता हूं!'
        ]
        return random.choice(jokes)
    
    def _help(self, text):
        """List available commands"""
        return 'मैं ये काम कर सकता हूं: समय बताओ, तारीख बताओ, मौसम बताओ, मज़ाक सुनाओ, वॉल्यूम बदलो'
    
    def _tell_identity(self, text):
        """Tell who the assistant is"""
        return 'मैं एक हिंदी आवाज़ सहायक हूं। मैं रास्पबेरी पाई पर चलता हूं और पूरी तरह ऑफलाइन हूं।'
    
    def _calculate(self, text):
        """Simple calculation (basic example)"""
        # Very basic - can be enhanced
        # Example: "दो जोड़ तीन" (two plus three)
        
        numbers = {
            'एक': 1, 'दो': 2, 'तीन': 3, 'चार': 4, 'पांच': 5,
            'छह': 6, 'सात': 7, 'आठ': 8, 'नौ': 9, 'दस': 10
        }
        
        # Simple extraction (this is basic - improve as needed)
        result = 'मैं अभी सिर्फ आसान गणना कर सकता हूं'
        
        return result
    
    def _reboot(self, text):
        """Reboot system (use carefully!)"""
        return 'रीबूट करने के लिए मुझे और अधिकार चाहिए'
        # Uncomment below for actual reboot (dangerous!)
        # subprocess.run(['sudo', 'reboot'])
    
    def _handle_unknown(self, text):
        """Handle unknown commands"""
        responses = [
            'मुझे समझ नहीं आया। कृपया फिर से कहें।',
            'यह कमांड मुझे नहीं पता। मदद के लिए "मदद करो" कहें।',
            'मैं यह नहीं कर सकता। कुछ और पूछें।'
        ]
        return random.choice(responses)
    
    def get_statistics(self):
        """Get command usage statistics"""
        return self.command_count


def test_intent_handler():
    """
    Test function for intent handler
    Run: python3 intent_handler.py
    """
    
    print("\n" + "="*50)
    print("Intent Handler Test")
    print("="*50 + "\n")
    
    handler = IntentHandler()
    
    # Test various commands
    test_inputs = [
        'नमस्ते',
        'समय बताओ',
        'आज क्या तारीख है',
        'धन्यवाद',
        'मौसम कैसा है',
        'मज़ाक सुनाओ',
        'तुम कौन हो',
        'मदद करो',
        'यह कमांड नहीं है'  # Unknown command
    ]
    
    print("Testing commands:\n")
    
    for i, text in enumerate(test_inputs, 1):
        intent, response = handler.process(text)
        print(f"{i}. Input: '{text}'")
        print(f"   Intent: {intent}")
        print(f"   Response: {response}")
        print()
    
    # Print statistics
    print("="*50)
    print("Command Statistics:")
    stats = handler.get_statistics()
    for cmd, count in stats.items():
        if count > 0:
            print(f"   {cmd}: {count} times")
    print("="*50 + "\n")


if __name__ == "__main__":
    # Run test when this file is executed directly
    test_intent_handler()
