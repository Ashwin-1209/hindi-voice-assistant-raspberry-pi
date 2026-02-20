# Installation Guide

Complete step-by-step installation instructions for Hindi Voice Assistant on Raspberry Pi 4.

---

## Prerequisites

### Hardware
- Raspberry Pi 4 (4GB RAM recommended)
- 32GB microSD card (Class 10 or better)
- USB Microphone
- Speaker (3.5mm jack or USB)
- USB-C Power Supply (5V, 3A minimum)
- Raspberry Pi Cooler (optional but recommended)
- Computer with SD card reader (for initial setup)

### Software
- Raspberry Pi Imager (download from raspberrypi.com/software)
- Internet connection (for initial setup only)

---

## Step 1: Flash Raspberry Pi OS

### 1.1 Download Raspberry Pi Imager

Download from: https://www.raspberrypi.com/software/

### 1.2 Flash SD Card

1. Insert SD card into your computer
2. Open Raspberry Pi Imager
3. Click "Choose OS" → Select "Raspberry Pi OS (64-bit)"
4. Click "Choose Storage" → Select your SD card
5. **Click the Settings icon (⚙️)** - This is important!

### 1.3 Configure Settings

In the settings menu, configure:

```
✅ Set hostname: voiceassistant

✅ Enable SSH
   ● Use password authentication

✅ Set username and password:
   Username: pi
   Password: [choose a password]

✅ Configure wireless LAN:
   SSID: [your WiFi name]
   Password: [your WiFi password]
   Wireless LAN country: IN

✅ Set locale settings:
   Time zone: Asia/Kolkata
   Keyboard layout: us
```

6. Click "SAVE"
7. Click "WRITE"
8. Wait for writing and verification (15-20 minutes)
9. Safely eject SD card

---

## Step 2: First Boot

### 2.1 Insert SD Card

1. Insert the flashed SD card into Raspberry Pi
2. Connect the cooler (if you have one)
3. Connect power supply
4. Wait 3-5 minutes for first boot

### 2.2 Find Pi's IP Address

**Method 1: Using hostname**
```bash
ping voiceassistant.local
```

**Method 2: Check your router**
- Login to router admin page
- Look for device named "voiceassistant"
- Note the IP address

**Method 3: Use IP scanner**
```bash
# On Windows
arp -a
```

### 2.3 Connect via SSH

```bash
# Replace 192.168.1.100 with your Pi's actual IP
ssh pi@192.168.1.100

# Or use hostname
ssh pi@voiceassistant.local
```

Enter the password you set in Step 1.3

---

## Step 3: System Setup

### 3.1 Update System

```bash
# Update package lists
sudo apt update

# Upgrade installed packages (optional, takes time)
sudo apt upgrade -y
```

### 3.2 Install System Dependencies

```bash
# Install audio and Python dependencies
sudo apt install -y python3-pip python3-pyaudio portaudio19-dev

# Install additional tools
sudo apt install -y git vim alsa-utils espeak-ng unzip wget
```

### 3.3 Test Hardware

**Test Microphone:**
```bash
# List audio devices
arecord -l

# Record 5 second test
arecord -D plughw:1,0 -d 5 test.wav

# Play it back
aplay test.wav
```

**Test Speaker:**
```bash
# List playback devices
aplay -l

# Test speaker
speaker-test -t wav -c 2
# Press Ctrl+C to stop

# Adjust volume
alsamixer
```

**Test Text-to-Speech:**
```bash
espeak-ng -v hi "नमस्ते"
```

---

## Step 4: Install Python Dependencies

### 4.1 Install Python Packages

```bash
# Install Vosk and PyAudio
pip3 install vosk pyaudio --break-system-packages
```

### 4.2 Download Hindi Model

```bash
# Go to home directory
cd ~

# Download Vosk Hindi model (~45 MB)
wget https://alphacephei.com/vosk/models/vosk-model-small-hi-0.22.zip

# Unzip
unzip vosk-model-small-hi-0.22.zip

# Rename for easy access
mv vosk-model-small-hi-0.22 vosk-model-hindi

# Verify
ls vosk-model-hindi
# Should show: am  conf  graph  ivector
```

---

## Step 5: Install Voice Assistant

### 5.1 Clone Repository

```bash
# Create project directory
mkdir -p ~/projects
cd ~/projects

# Clone the repository
git clone https://github.com/[your-username]/hindi-voice-assistant.git

# Enter directory
cd hindi-voice-assistant
```

### 5.2 Verify Files

```bash
ls -l
```

You should see:
- main.py
- asr_module.py
- intent_handler.py
- tts_module.py
- requirements.txt
- README.md

### 5.3 Install Dependencies (Alternative)

If you haven't installed dependencies yet:

```bash
pip3 install -r requirements.txt --break-system-packages
```

---

## Step 6: Configuration

### 6.1 Update Model Path (if needed)

If your model is in a different location, edit `asr_module.py`:

```bash
nano asr_module.py
```

Find this line:
```python
def __init__(self, model_path="/home/pi/vosk-model-hindi"):
```

Update the path to where your model is located.

Press `Ctrl+X`, then `Y`, then `Enter` to save.

### 6.2 Configure Audio Devices (if needed)

If your microphone is not on device 1:

```bash
# List devices
arecord -l

# Note your device number (e.g., card 2, device 0)
```

Edit `asr_module.py` to specify device index.

---

## Step 7: Run the Application

### 7.1 First Run

```bash
cd ~/projects/hindi-voice-assistant
python3 main.py
```

You should see:
```
╔═══════════════════════════════════════════════╗
║                                               ║
║     Hindi Voice Assistant - Raspberry Pi      ║
║     Offline Privacy Preserving System         ║
║                                               ║
╚═══════════════════════════════════════════════╝

🚀 Initializing Hindi Voice Assistant...
==================================================
🎤 Initializing Speech Recognizer...
   Loading model from: /home/pi/vosk-model-hindi
   ✅ Model loaded successfully!
   ✅ Microphone initialized!
🧠 Initializing Intent Handler...
   ✅ Loaded 14 command categories
🔊 Initializing Text-to-Speech...
   ✅ TTS initialized successfully!
✅ Voice Assistant initialized successfully!
==================================================

🎤 Voice Assistant is now listening...
Speak in Hindi to give commands
Press Ctrl+C to stop
```

### 7.2 Test Commands

Speak these Hindi commands:
- नमस्ते (Hello)
- समय बताओ (Tell time)
- तारीख बताओ (Tell date)
- धन्यवाद (Thank you)

### 7.3 Stop the Application

Press `Ctrl+C` to stop.

---

## Step 8: Auto-Start on Boot (Optional)

To make the voice assistant start automatically on boot:

### 8.1 Create Service File

```bash
sudo nano /etc/systemd/system/voice-assistant.service
```

Add this content:
```ini
[Unit]
Description=Hindi Voice Assistant
After=network.target sound.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/projects/hindi-voice-assistant
ExecStart=/usr/bin/python3 /home/pi/projects/hindi-voice-assistant/main.py
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Save with `Ctrl+X`, `Y`, `Enter`.

### 8.2 Enable Service

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service
sudo systemctl enable voice-assistant.service

# Start service
sudo systemctl start voice-assistant.service

# Check status
sudo systemctl status voice-assistant.service
```

### 8.3 Manage Service

```bash
# Stop
sudo systemctl stop voice-assistant.service

# Restart
sudo systemctl restart voice-assistant.service

# Disable auto-start
sudo systemctl disable voice-assistant.service
```

---

## Troubleshooting

### Issue: "Module 'vosk' not found"

**Solution:**
```bash
pip3 install vosk --break-system-packages
```

### Issue: "No module named 'pyaudio'"

**Solution:**
```bash
sudo apt install python3-pyaudio portaudio19-dev
pip3 install pyaudio --break-system-packages
```

### Issue: Microphone not detected

**Solution:**
```bash
# Check if microphone is detected
lsusb

# List audio devices
arecord -l

# Check permissions
sudo usermod -a -G audio pi

# Reboot
sudo reboot
```

### Issue: No audio output

**Solution:**
```bash
# Check volume
alsamixer

# Force audio to 3.5mm jack
sudo raspi-config
# System Options → Audio → Force 3.5mm jack

# Test speaker
speaker-test -t wav -c 2
```

### Issue: Hindi not recognized

**Solution:**
- Verify model path: `ls ~/vosk-model-hindi`
- Speak clearly and directly into microphone
- Reduce background noise
- Try simpler commands first (नमस्ते)

### Issue: High CPU temperature

**Solution:**
```bash
# Check temperature
vcgencmd measure_temp

# If > 70°C:
# - Ensure cooler is properly attached
# - Improve ventilation
# - Consider active cooling fan
```

### Issue: "Connection refused" when SSH

**Solution:**
- Ensure SSH was enabled in Raspberry Pi Imager
- Pi might still be booting (wait 5 minutes)
- Verify IP address is correct
- Check WiFi configuration

---

## Verification Checklist

After installation, verify:

- [ ] Pi boots successfully
- [ ] Can SSH to Pi
- [ ] Microphone records audio
- [ ] Speaker plays audio
- [ ] eSpeak-NG speaks Hindi
- [ ] Vosk model loaded
- [ ] main.py runs without errors
- [ ] Voice commands recognized
- [ ] Response time < 2 seconds
- [ ] All 10+ commands working

---

## Performance Optimization

### Disable GUI (saves RAM)

```bash
sudo raspi-config
# System Options → Boot / Auto Login → Console
sudo reboot
```

### Set CPU Governor

```bash
# Set to performance mode
echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor
```

### Reduce Swap Usage

```bash
sudo nano /etc/sysctl.conf
```

Add:
```
vm.swappiness=10
```

---

## Uninstallation

To remove the voice assistant:

```bash
# Stop service (if enabled)
sudo systemctl stop voice-assistant.service
sudo systemctl disable voice-assistant.service
sudo rm /etc/systemd/system/voice-assistant.service

# Remove project
rm -rf ~/projects/hindi-voice-assistant

# Remove Vosk model
rm -rf ~/vosk-model-hindi

# Uninstall Python packages
pip3 uninstall vosk pyaudio

# Remove system packages (optional)
sudo apt remove espeak-ng python3-pyaudio
```

---

## Next Steps

- Read [COMMANDS.md](COMMANDS.md) to learn all available commands
- Check [README.md](README.md) for project overview
- See [OPTIMIZATION.md](OPTIMIZATION.md) for performance tuning

---

## Support

For issues or questions:
- GitHub Issues: https://github.com/[your-username]/hindi-voice-assistant/issues
- Email: [your-email]
- Challenge Support: support@armbharatchallenge.com

---

**Installation complete! Enjoy your offline Hindi voice assistant! 🎉**
