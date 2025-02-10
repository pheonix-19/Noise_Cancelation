# Live Audio Filter Visualization
# Author : Ayush 

## Overview
This project is a real-time audio filtering application that demonstrates advanced signal processing techniques for voice enhancement. It uses a web-based frontend with JavaScript and a Python backend to apply sophisticated audio filtering in the browser.

## Key Features
- Real-time microphone audio processing
- Bandpass filtering to isolate human voice frequencies
- Spectral subtraction for noise reduction
- Visual waveform and frequency spectrum visualization
- WebSocket-based communication between frontend and backend

## Technologies Used
- Frontend: HTML5, JavaScript, Web Audio API
- Backend: Python, FastAPI, WebSockets
- Signal Processing: NumPy, SciPy

## How It Works

### Audio Processing Pipeline
1. **Bandpass Filtering**: 
   - Removes frequencies outside the human voice range (120-4000 Hz)
   - Eliminates low and high-frequency noise
   - Uses a 4th order Butterworth bandpass filter

2. **Spectral Subtraction**:
   - Dynamically estimates and subtracts background noise
   - Smooths noise profile to prevent artifacts
   - Preserves voice clarity while reducing unwanted sounds

### Visualization
The application provides four real-time canvases:
- Input Waveform (Blue)
- Input Frequency Spectrum (Red)
- Processed Waveform (Green)
- Processed Frequency Spectrum (Purple)

## Prerequisites
- Python 3.8+
- Modern web browser with WebSocket support
- Microphone

## Installation

### Backend Setup
1. Clone the repository
```bash
git clone https://github.com/pheonix-19/Noise_Cancelation.git
cd live-audio-filter
```

2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install dependencies
```bash
pip install fastapi uvicorn numpy scipy websockets
```

### Frontend Setup
No additional setup required. Open the HTML file in a modern browser.

## Running the Application

1. Start the Python backend
```bash
python audio_filter_server.py
```

2. Open `index.html` in a web browser
3. Click "Start Processing" and grant microphone permissions
4. Observe real-time audio filtering and visualization

## Technical Details

### Frontend (`index.html`)
- Uses Web Audio API for real-time audio capture
- WebSocket communication with backend
- Canvas-based visualization of audio signals

### Backend (`audio_filter_server.py`)
- FastAPI WebSocket server
- NumPy and SciPy for signal processing
- Implements bandpass filtering and spectral subtraction

## Customization
You can modify these parameters in the `VoiceFilter` class:
- `low_cutoff`: Lower frequency boundary
- `high_cutoff`: Upper frequency boundary
- `smoothing_factor`: Noise estimation smoothness


## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments
- Web Audio API Documentation
- NumPy and SciPy Signal Processing Libraries
