#!/usr/bin/env python3
"""
Hindi Voice Assistant - Main Application
Raspberry Pi 4 - Offline Privacy Preserving System

This is the main entry point for the voice assistant.
It coordinates ASR, Intent Recognition, and TTS modules.
"""

import sys
import time
import json
from datetime import datetime

# Import our custom modules (we'll create these)
# from asr_module import SpeechRecognizer
# from intent_handler import IntentHandler
# from tts_module import TextToSpeech

class VoiceAssistant:
    """
    Main Voice Assistant Class
    Manages the complete pipeline: Listen → Understand → Respond
    """
    
    def __init__(self):
        """Initialize the voice assistant with all modules"""
        print("🚀 Initializing Hindi Voice Assistant...")
        print("=" * 50)
        
        # Configuration
        self.is_running = False
        self.wake_word = "assistant"  # Optional wake word
        self.use_wake_word = False    # Set to True to enable
        
        # Performance tracking
        self.response_times = []
        self.command_count = 0
        
        # Initialize modules (uncomment when modules are ready)
        # self.asr = SpeechRecognizer()
        # self.intent_handler = IntentHandler()
        # self.tts = TextToSpeech()
        
        print("✅ Voice Assistant initialized successfully!")
        print("=" * 50)
    
    def start(self):
        """Start the voice assistant main loop"""
        self.is_running = True
        
        print("\n🎤 Voice Assistant is now listening...")
        print("Speak in Hindi to give commands")
        print("Press Ctrl+C to stop\n")
        
        # Welcome message
        self._speak("नमस्ते! मैं आपकी हिंदी सहायक हूं।")
        
        try:
            while self.is_running:
                # Main processing loop
                self._process_audio()
                
        except KeyboardInterrupt:
            print("\n\n🛑 Stopping voice assistant...")
            self.stop()
    
    def _process_audio(self):
        """
        Main processing pipeline:
        1. Listen for audio
        2. Convert speech to text (ASR)
        3. Parse intent
        4. Execute action
        5. Generate response (TTS)
        """
        
        # Start timer for performance measurement
        start_time = time.time()
        
        # STEP 1: Listen and convert speech to text
        # recognized_text = self.asr.listen()
        recognized_text = self._mock_listen()  # Temporary mock
        
        if not recognized_text:
            return  # No speech detected
        
        print(f"👂 Heard: {recognized_text}")
        
        # STEP 2: Parse the intent from recognized text
        # intent, response = self.intent_handler.process(recognized_text)
        intent, response = self._mock_intent(recognized_text)  # Temporary mock
        
        print(f"🧠 Intent: {intent}")
        print(f"💬 Response: {response}")
        
        # STEP 3: Speak the response
        # self.tts.speak(response)
        self._speak(response)
        
        # Track performance
        end_time = time.time()
        response_time = end_time - start_time
        self.response_times.append(response_time)
        self.command_count += 1
        
        print(f"⏱️  Response time: {response_time:.2f} seconds")
        print("-" * 50)
    
    def _mock_listen(self):
        """
        Temporary mock function for testing
        Replace this with actual ASR when asr_module.py is ready
        """
        # Simulate waiting for speech
        time.sleep(0.5)
        
        # For now, return None (no speech)
        # In real implementation, this will return recognized Hindi text
        return None
    
    def _mock_intent(self, text):
        """
        Temporary mock function for testing
        Replace this with actual intent handler when intent_handler.py is ready
        """
        intent = "unknown"
        response = "मुझे समझ नहीं आया"  # "I don't understand"
        
        return intent, response
    
    def _speak(self, text):
        """
        Temporary mock function for testing
        Replace this with actual TTS when tts_module.py is ready
        """
        print(f"🔊 Speaking: {text}")
        # In real implementation, this will use eSpeak-NG to speak
    
    def stop(self):
        """Stop the voice assistant and print statistics"""
        self.is_running = False
        
        print("\n" + "=" * 50)
        print("📊 Session Statistics:")
        print(f"   Total commands processed: {self.command_count}")
        
        if self.response_times:
            avg_time = sum(self.response_times) / len(self.response_times)
            min_time = min(self.response_times)
            max_time = max(self.response_times)
            
            print(f"   Average response time: {avg_time:.2f} seconds")
            print(f"   Fastest response: {min_time:.2f} seconds")
            print(f"   Slowest response: {max_time:.2f} seconds")
        
        print("=" * 50)
        print("👋 Thank you for using Hindi Voice Assistant!")
        print("   धन्यवाद!\n")


def main():
    """Main entry point"""
    
    # ASCII Art Banner
    print("""
    ╔═══════════════════════════════════════════════╗
    ║                                               ║
    ║     Hindi Voice Assistant - Raspberry Pi      ║
    ║     Offline Privacy Preserving System         ║
    ║                                               ║
    ║     भारतीय आवाज़ सहायक                        ║
    ║                                               ║
    ╚═══════════════════════════════════════════════╝
    """)
    
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Create and start the assistant
    assistant = VoiceAssistant()
    assistant.start()


if __name__ == "__main__":
    main()
