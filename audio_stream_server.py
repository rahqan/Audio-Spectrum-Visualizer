import sounddevice as sd
import numpy as np
import asyncio
import websockets
import json
from scipy.fft import fft

# Parameters
fs = 44100            # Sampling frequency (how many times per second we sample the sound wave)
chunk_duration = 0.1  # Duration of each chunk in seconds
chunk_size = int(fs * chunk_duration)  # Number of samples per chunk (total samples in 0.1 seconds)

# Asynchronous function to handle the WebSocket connection and audio streaming
async def audio_stream(websocket, path):
    print("Client connected.")
    try:
        # This function is a callback that processes each small "chunk" of audio data
        # and sends the processed frequency information through the WebSocket

        def audio_callback(indata, frames, time, status):
            if status:
                print("Status:", status)

            # Flattening the 2D audio data into a 1D array for FFT processing
            # `indata` holds raw audio pressure values in the range of -32768 to 32767 (16-bit PCM).
            # We normalize it by dividing by 32768.0 to bring values into the -1.0 to 1.0 range.
            # This prepares the data for FFT analysis.
            audio_data = indata.flatten() / 32768.0

            # Applying FFT to convert the time-domain signal (air pressure changes over time)
            # into frequency components. Each result is a complex number representing
            # both the amplitude (strength) and phase of a frequency in the audio.
            # np.abs() gives us the magnitude, which corresponds to the "strength" (loudness)
            # of each frequency, ignoring the phase. We take only the first half of the
            # results (up to `chunk_size // 2`) since FFT output is symmetric.
            spectrum = np.abs(fft(audio_data))[:chunk_size // 2]

            # Generating frequency bins to know which frequency each index in `spectrum` represents.
            # `np.fft.fftfreq` creates a list where each index matches a specific frequency
            # that `spectrum`'s amplitudes correspond to. We again take only the first half.
            freq_bins = np.fft.fftfreq(chunk_size, 1 / fs)[:chunk_size // 2]

            # Preparing data to send as JSON format, so that the frontend can understand it.
            # We're sending two lists: one for `frequencies` (freq_bins) and one for their
            # corresponding `magnitudes` (spectrum). These will be used to visualize sound.
            data = {
                "frequencies": freq_bins.tolist(),
                "magnitudes": spectrum.tolist()
            }

            # Using `asyncio.run_coroutine_threadsafe` to send the JSON data through WebSocket
            # from this non-async callback. This sends frequency-amplitude data to the client.
            asyncio.run_coroutine_threadsafe(websocket.send(json.dumps(data)), loop)

        # Start the audio stream with `sounddevice` and pass in the callback function.
        # Each time the microphone captures a chunk of audio, `audio_callback` will be called.
        # `channels=1` means mono (single-channel) audio, `samplerate=fs` sets the rate,
        # and `blocksize=chunk_size` sets the number of samples in each audio chunk.
        with sd.InputStream(callback=audio_callback, channels=1, samplerate=fs, blocksize=chunk_size, dtype='int16'):
            await asyncio.Future()  # Keeps the stream open until the WebSocket disconnects

    # Handle WebSocket disconnection cleanly
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected.")

# WebSocket server setup
async def main():
    # `websockets.serve` starts a WebSocket server on localhost at port 6789
    async with websockets.serve(audio_stream, "localhost", 6789):
        print("WebSocket server started on ws://localhost:6789")
        await asyncio.Future()  # Keeps the server running indefinitely

if __name__ == "__main__":
    # Creating an event loop to handle WebSocket connections and audio processing asynchronously
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())  # Start the server
