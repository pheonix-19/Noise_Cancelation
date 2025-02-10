import numpy as np
import uvicorn
import asyncio
from fastapi import FastAPI, WebSocket
from scipy.signal import butter, lfilter

app = FastAPI()

class VoiceFilter:
    def __init__(self, chunk=1024, rate=44100):
        self.chunk = chunk
        self.rate = rate
        self.low_cutoff, self.high_cutoff = 120, 4000  # Keep human voice range(80/3000)
        self.smoothing_factor = 0.8  # Reduce sudden jumps
        self.previous_spectrum = None

    def butter_bandpass(self, lowcut, highcut, fs, order=4):
        """Create a bandpass filter to remove unwanted frequencies."""
        nyquist = 0.5 * fs
        low = lowcut / nyquist
        high = highcut / nyquist
        b, a = butter(order, [low, high], btype='band')
        return b, a

    def apply_bandpass_filter(self, audio_chunk):
        """Applies a bandpass filter to keep only voice frequencies."""
        b, a = self.butter_bandpass(self.low_cutoff, self.high_cutoff, self.rate, order=6)
        return lfilter(b, a, audio_chunk)

    def spectral_subtraction(self, spectrum):
        """Reduces background noise by subtracting the noise profile."""
        if self.previous_spectrum is None:
            self.previous_spectrum = spectrum  # First frame, no noise profile yet
            return spectrum

        noise_estimate = self.previous_spectrum * (1 - self.smoothing_factor)
        enhanced_spectrum = spectrum - noise_estimate
        enhanced_spectrum = np.maximum(enhanced_spectrum, 0)  # Avoid negative values

        self.previous_spectrum = self.smoothing_factor * self.previous_spectrum + (1 - self.smoothing_factor) * spectrum
        return enhanced_spectrum

    def enhance_voice(self, audio_chunk):
        """Applies filtering, noise suppression, and spectral enhancement."""
        # Step 1: Apply bandpass filter to remove low/high-frequency noise
        filtered_audio = self.apply_bandpass_filter(audio_chunk)

        # Step 2: Convert to frequency domain
        audio_spec = np.fft.rfft(filtered_audio)
        audio_mag = np.abs(audio_spec)
        audio_phase = np.angle(audio_spec)

        # Step 3: Apply spectral subtraction for noise suppression
        enhanced_mag = self.spectral_subtraction(audio_mag)

        # Step 4: Reconstruct the audio signal
        enhanced_spec = enhanced_mag * np.exp(1j * audio_phase)
        return np.fft.irfft(enhanced_spec).astype(np.float32)

voice_filter = VoiceFilter()

@app.websocket("/process_audio")
async def process_audio(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_bytes()
            audio_chunk = np.frombuffer(data, dtype=np.float32)
            enhanced_audio = voice_filter.enhance_voice(audio_chunk)
            await websocket.send_bytes(enhanced_audio.tobytes())
    except Exception as e:
        print(f"WebSocket closed: {e}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
