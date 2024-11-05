
# Audio Spectrum Visualizer

This project provides a real-time audio spectrum visualizer that captures audio data from a microphone, processes it to obtain frequency and amplitude information, and displays it using a line chart in a web interface. The application is built with a Python WebSocket server for audio analysis and a React frontend with Chart.js for visualization.

## Features

- **Real-time Audio Analysis**: Captures audio input, processes it using FFT (Fast Fourier Transform) to obtain frequencies and magnitudes.
- **WebSocket Communication**: Streams audio frequency data continuously to the frontend.
- **Visual Display**: Shows frequency magnitudes on a dynamic, responsive chart.

## Technology Stack

- **Backend**: Python, WebSocket Server, FFT for frequency analysis.
- **Frontend**: React, Chart.js, WebSocket API for real-time data rendering.

---

## Getting Started

### Prerequisites

- **Python 3.x**
- **Node.js** and **npm**
- **Dependencies**: Install the required Python and Node.js packages.

### Installation

1. **Backend Setup**:
   - Navigate to the backend directory.
   - Install dependencies (like `websockets` and any required audio processing libraries):
     ```bash
     pip install websockets numpy
     ```
   - Run the WebSocket server:
     ```bash
     python audio_stream_server.py
     ```
   - This script will start a WebSocket server on `ws://localhost:6789` to stream frequency and amplitude data.

2. **Frontend Setup**:
   - Navigate to the React frontend directory.
   - Install dependencies:
     ```bash
     npm install
     ```
   - Start the React app:
     ```bash
     npm start
     ```
   - The React app will open on `http://localhost:3000`.

---

## How It Works

### Backend (Python WebSocket Server)

The backend captures audio data, processes it using FFT to obtain frequency bins and their magnitudes, and sends this data via WebSocket to the React frontend. 

1. **Connect Microphone**: Captures audio in real time from the microphone.
2. **FFT Processing**: Converts the time-domain audio signal into a frequency-domain representation.
3. **Data Streaming**: Streams the processed frequency and amplitude data via WebSocket in JSON format.

### Frontend (React App)

The React app establishes a WebSocket connection to receive frequency data from the server and visualizes it using Chart.js.

- **WebSocket Client**: Connects to the WebSocket server at `ws://localhost:6789` and listens for incoming data.
- **Dynamic Chart Rendering**: Updates the chart whenever new data is received, showing frequency (Hz) on the X-axis and magnitude on the Y-axis.

---

## File Structure

- **audio_stream_server.py**: The Python WebSocket server script for capturing and processing audio data.
- **App.js**: Main React component that handles WebSocket connections and renders the Chart.js line chart.

---

## Troubleshooting

- **WebSocket Connection Issues**: Ensure the WebSocket server is running on `ws://localhost:6789` and no other service is blocking this port.
- **Chart Rendering Issues**: Verify that Chart.js is installed and registered correctly in the React app.


