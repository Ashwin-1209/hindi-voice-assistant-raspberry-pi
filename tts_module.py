#!/usr/bin/env python3
"""
TTS Module - Text-to-Speech for Hindi
Uses eSpeak-NG for offline Hindi speech synthesis

This module:
- Converts Hindi text to speech
- Plays audio through speakers
- Manages voice settings
"""

import subprocess
import os
import tempfile

class TextToSpeech:
    """
    Handles text-to-speech conversion using eSpeak-NG
    """
    
    def __init__(self, voice='hi', speed=150, pitch=50):
        """
        Initialize Text-to-Speech engine
        
        Args:
            voice (str): Voice language code ('hi' for Hindi)
            speed (int): Speaking speed (80-500, default 150)
            pitch (int): Voice pitch (0-99, default 50)
        """
        print("🔊 Initializing Text-to-Speech...")
        
        self.voice = voice
        self.speed = speed
        self.pitch = pitch
        
        # Check if eSpeak-NG is installed
        if not self._check_espeak():
            raise RuntimeError("eSpeak-NG not found. Install with: sudo apt install espeak-ng")
        
        print(f"   Voice: {voice}")
        print(f"   Speed: {speed} WPM")
        print(f"   Pitch: {pitch}")
        print("   ✅ TTS initialized successfully!")
    
    def _check_espeak(self):
        """
        Check if eSpeak-NG is installed
        
        Returns:
            bool: True if eSpeak-NG is available
        """
        try:
            result = subprocess.run(
                ['espeak-ng', '--version'],
                capture_output=True,
                timeout=2
            )
            return result.returncode == 0
        except:
            return False
    
    def speak(self, text):
        """
        Convert text to speech and play it
        
        Args:
            text (str): Hindi text to speak
        """
        
        if not text or text.strip() == '':
            print("⚠️  No text to speak")
            return
        
        print(f"🔊 Speaking: {text}")
        
        try:
            # Build eSpeak-NG command
            command = [
                'espeak-ng',
                '-v', self.voice,      # Voice (Hindi)
                '-s', str(self.speed),  # Speed
                '-p', str(self.pitch),  # Pitch
                text                    # Text to speak
            ]
            
            # Execute and wait for completion
            result = subprocess.run(
                command,
                capture_output=True,
                timeout=10
            )
            
            if result.returncode != 0:
                print(f"⚠️  eSpeak-NG error: {result.stderr.decode()}")
        
        except subprocess.TimeoutExpired:
            print("⚠️  Speech timeout - text too long?")
        except Exception as e:
            print(f"❌ Error speaking: {e}")
    
    def speak_to_file(self, text, filename):
        """
        Convert text to speech and save to WAV file
        
        Args:
            text (str): Hindi text to convert
            filename (str): Output WAV filename
        """
        
        print(f"💾 Saving speech to: {filename}")
        
        try:
            command = [
                'espeak-ng',
                '-v', self.voice,
                '-s', str(self.speed),
                '-p', str(self.pitch),
                '-w', filename,  # Write to file
                text
            ]
            
            result = subprocess.run(
                command,
                capture_output=True,
                timeout=10
            )
            
            if result.returncode == 0:
                print(f"   ✅ Saved successfully!")
            else:
                print(f"   ❌ Error: {result.stderr.decode()}")
        
        except Exception as e:
            print(f"❌ Error saving: {e}")
    
    def set_speed(self, speed):
        """
        Change speaking speed
        
        Args:
            speed (int): Words per minute (80-500)
        """
        if 80 <= speed <= 500:
            self.speed = speed
            print(f"✅ Speed set to {speed} WPM")
        else:
            print("⚠️  Speed must be between 80-500")
    
    def set_pitch(self, pitch):
        """
        Change voice pitch
        
        Args:
            pitch (int): Pitch value (0-99)
        """
        if 0 <= pitch <= 99:
            self.pitch = pitch
            print(f"✅ Pitch set to {pitch}")
        else:
            print("⚠️  Pitch must be between 0-99")
    
    def list_voices(self):
        """List all available voices"""
        try:
            result = subprocess.run(
                ['espeak-ng', '--voices'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            print("\n📋 Available voices:")
            print(result.stdout)
        
        except Exception as e:
            print(f"❌ Error listing voices: {e}")
    
    def test_voice(self):
        """Test the current voice configuration"""
        test_phrases = [
            'नमस्ते',
            'मैं एक हिंदी आवाज़ सहायक हूं',
            'यह एक परीक्षण है'
        ]
        
        print("\n🎵 Testing voice with sample phrases:\n")
        
        for i, phrase in enumerate(test_phrases, 1):
            print(f"{i}. {phrase}")
            self.speak(phrase)
            
            # Small pause between phrases
            import time
            time.sleep(0.5)
        
        print("\n✅ Voice test complete!")


def test_tts():
    """
    Test function for TTS module
    Run: python3 tts_module.py
    """
    
    print("\n" + "="*50)
    print("TTS Module Test")
    print("="*50 + "\n")
    
    # Initialize TTS
    tts = TextToSpeech()
    
    # Test 1: List available voices
    print("\nTest 1: Available Voices")
    print("-" * 30)
    tts.list_voices()
    
    # Test 2: Speak some Hindi text
    print("\nTest 2: Speaking Hindi Text")
    print("-" * 30)
    
    test_sentences = [
        'नमस्ते! मैं आपकी हिंदी सहायक हूं।',
        'आज मौसम बहुत सुहावना है।',
        'धन्यवाद!',
        'आपका स्वागत है!'
    ]
    
    for i, sentence in enumerate(test_sentences, 1):
        print(f"\n{i}. Testing: {sentence}")
        tts.speak(sentence)
        
        import time
        time.sleep(1)  # Pause between sentences
    
    # Test 3: Different speeds
    print("\n\nTest 3: Different Speaking Speeds")
    print("-" * 30)
    
    speeds = [100, 150, 200]
    test_text = "यह एक परीक्षण है"
    
    for speed in speeds:
        print(f"\nSpeed {speed} WPM:")
        tts.set_speed(speed)
        tts.speak(test_text)
        
        import time
        time.sleep(1)
    
    # Test 4: Save to file
    print("\n\nTest 4: Save to File")
    print("-" * 30)
    
    output_file = "/tmp/test_speech.wav"
    tts.speak_to_file("यह फाइल में सेव किया गया", output_file)
    
    if os.path.exists(output_file):
        print(f"✅ File created: {output_file}")
        print("   Playing saved file...")
        subprocess.run(['aplay', output_file])
    
    print("\n" + "="*50)
    print("Test Complete!")
    print("="*50 + "\n")


if __name__ == "__main__":
    # Run test when this file is executed directly
    test_tts()
