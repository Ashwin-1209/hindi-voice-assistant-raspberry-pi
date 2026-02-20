#!/usr/bin/env python3
"""
ASR Module - Automatic Speech Recognition for Hindi
Uses Vosk for offline speech-to-text conversion

This module handles:
- Audio input from microphone
- Real-time speech recognition
- Converting Hindi speech to text
"""

import json
import pyaudio
from vosk import Model, KaldiRecognizer

class SpeechRecognizer:
    """
    Handles speech-to-text conversion using Vosk
    """
    
    def __init__(self, model_path="/home/pi/vosk-model-hindi"):
        """
        Initialize the speech recognizer
        
        Args:
            model_path (str): Path to Vosk Hindi model
        """
        print("🎤 Initializing Speech Recognizer...")
        
        # Configuration
        self.model_path = model_path
        self.sample_rate = 16000  # 16kHz is standard for speech
        self.chunk_size = 8192    # Audio buffer size
        
        # Load Vosk model
        try:
            print(f"   Loading model from: {model_path}")
            self.model = Model(model_path)
            self.recognizer = KaldiRecognizer(self.model, self.sample_rate)
            print("   ✅ Model loaded successfully!")
        except Exception as e:
            print(f"   ❌ Error loading model: {e}")
            raise
        
        # Initialize PyAudio
        self.audio = pyaudio.PyAudio()
        
        # Find microphone
        self.mic_index = self._find_microphone()
        
        # Open audio stream
        self.stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.sample_rate,
            input=True,
            input_device_index=self.mic_index,
            frames_per_buffer=self.chunk_size
        )
        
        print("   ✅ Microphone initialized!")
        print(f"   Using device: {self.mic_index}")
    
    def _find_microphone(self):
        """
        Find the USB microphone device
        
        Returns:
            int: Device index of the microphone
        """
        info = self.audio.get_host_api_info_by_index(0)
        num_devices = info.get('deviceCount')
        
        print(f"   Found {num_devices} audio devices")
        
        # List all input devices
        for i in range(num_devices):
            device_info = self.audio.get_device_info_by_host_api_device_index(0, i)
            if device_info.get('maxInputChannels') > 0:
                print(f"   Device {i}: {device_info.get('name')}")
        
        # For now, use default input device
        # You can modify this to select specific device
        default_device = self.audio.get_default_input_device_info()
        return default_device['index']
    
    def listen(self, timeout=5):
        """
        Listen for speech and convert to text
        
        Args:
            timeout (int): Maximum seconds to listen
            
        Returns:
            str: Recognized text in Hindi, or None if no speech
        """
        
        print("🎧 Listening...", end=" ", flush=True)
        
        # Clear any previous recognition
        self.recognizer = KaldiRecognizer(self.model, self.sample_rate)
        
        recognized_text = None
        start_time = 0
        speech_started = False
        
        try:
            while True:
                # Read audio data
                data = self.stream.read(4096, exception_on_overflow=False)
                
                # Process audio
                if self.recognizer.AcceptWaveform(data):
                    # Speech segment completed
                    result = json.loads(self.recognizer.Result())
                    text = result.get('text', '').strip()
                    
                    if text:
                        recognized_text = text
                        break
                else:
                    # Partial result (ongoing speech)
                    partial = json.loads(self.recognizer.PartialResult())
                    partial_text = partial.get('partial', '')
                    
                    if partial_text and not speech_started:
                        speech_started = True
                        print("👂 Detecting speech...", end=" ", flush=True)
        
        except KeyboardInterrupt:
            print("\n⚠️  Listening interrupted")
            return None
        
        if recognized_text:
            print(f"✅ Recognized!")
        else:
            print("❌ No speech detected")
        
        return recognized_text
    
    def listen_continuous(self, callback):
        """
        Continuous listening mode
        Calls callback function whenever speech is recognized
        
        Args:
            callback (function): Function to call with recognized text
        """
        
        print("🎧 Continuous listening mode activated")
        print("   Speak anytime... Press Ctrl+C to stop\n")
        
        try:
            while True:
                data = self.stream.read(4096, exception_on_overflow=False)
                
                if self.recognizer.AcceptWaveform(data):
                    result = json.loads(self.recognizer.Result())
                    text = result.get('text', '').strip()
                    
                    if text:
                        # Call the callback function with recognized text
                        callback(text)
                        
                        # Reset recognizer for next utterance
                        self.recognizer = KaldiRecognizer(self.model, self.sample_rate)
        
        except KeyboardInterrupt:
            print("\n⚠️  Continuous listening stopped")
    
    def test_microphone(self, duration=5):
        """
        Test microphone by recording and displaying audio levels
        
        Args:
            duration (int): Seconds to test
        """
        
        print(f"\n🎤 Testing microphone for {duration} seconds...")
        print("   Speak into the microphone!\n")
        
        import struct
        import math
        
        for i in range(int(duration * self.sample_rate / self.chunk_size)):
            data = self.stream.read(self.chunk_size, exception_on_overflow=False)
            
            # Calculate audio level
            count = len(data) / 2
            format_str = "%dh" % count
            shorts = struct.unpack(format_str, data)
            
            # RMS (Root Mean Square) of audio
            sum_squares = sum(s**2 for s in shorts)
            rms = math.sqrt(sum_squares / count)
            
            # Visualize level
            level = int(rms / 1000)
            bar = "█" * min(level, 50)
            print(f"   Level: {bar} {rms:.0f}", end="\r")
        
        print("\n✅ Microphone test complete!\n")
    
    def close(self):
        """Clean up resources"""
        print("🛑 Closing speech recognizer...")
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        print("   ✅ Closed successfully!")


def test_asr():
    """
    Test function to verify ASR is working
    Run this file directly to test: python3 asr_module.py
    """
    
    print("\n" + "="*50)
    print("ASR Module Test")
    print("="*50 + "\n")
    
    # Initialize recognizer
    asr = SpeechRecognizer()
    
    # Test 1: Microphone test
    asr.test_microphone(duration=3)
    
    # Test 2: Single recognition
    print("📝 Test: Single recognition")
    print("   Speak a Hindi command...\n")
    
    for i in range(3):
        text = asr.listen()
        if text:
            print(f"   Result {i+1}: '{text}'")
        else:
            print(f"   Result {i+1}: (no speech)")
        print()
    
    # Clean up
    asr.close()
    
    print("\n" + "="*50)
    print("Test Complete!")
    print("="*50 + "\n")


if __name__ == "__main__":
    # Run test when this file is executed directly
    test_asr()
