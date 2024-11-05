import React, { useEffect, useRef, useState } from 'react';
import { Chart, CategoryScale, LinearScale, LineElement, Title, Tooltip, Legend, PointElement, LineController } from 'chart.js';

Chart.register(CategoryScale, LinearScale, LineElement, Title, Tooltip, Legend, PointElement, LineController);

const App = () => {
  const chartRef = useRef(null);
  const [frequencies, setFrequencies] = useState([]);
  const [magnitudes, setMagnitudes] = useState([]);

  // Establish WebSocket connection and handle incoming data
  const connectWebSocket = () => {
    const websocket = new WebSocket('ws://localhost:6789');

    websocket.onopen = () => console.log('WebSocket connected');
    websocket.onclose = () => {
      console.log('WebSocket connection closed, retrying...');
      setTimeout(connectWebSocket, 1000); // Retry connection
    };

    websocket.onerror = (error) => console.error('WebSocket error:', error);

    websocket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      console.log("Received data:", data);

      // Update state only if data has both frequencies and magnitudes arrays
      if (data.frequencies && data.magnitudes) {
        setFrequencies(data.frequencies);
        setMagnitudes(data.magnitudes);
      } else {
        console.error("Unexpected data format:", data);
      }
    };

    return websocket;
  };

  useEffect(() => {
    const websocket = connectWebSocket();
    return () => websocket.close(); // Close WebSocket on unmount
  }, []);

  const renderChart = () => {
    const ctx = document.getElementById('myChart').getContext('2d');

    // Destroy the previous chart instance if it exists
    if (chartRef.current) {
      chartRef.current.destroy();
    }

    // Create a new chart instance
    chartRef.current = new Chart(ctx, {
      type: 'line',
      data: {
        labels: frequencies, // X-axis labels (frequency bins)
        datasets: [{
          label: 'Frequency Magnitudes',
          data: magnitudes,   // Y-axis data (magnitudes)
          borderColor: 'rgba(75, 192, 192, 1)',
          backgroundColor: 'rgba(75, 192, 192, 0.2)',
          fill: true,
        }]
      },
      options: {
        responsive: true,
        scales: {
          x: {
            type: 'linear',
            title: {
              display: true,
              text: 'Frequency (Hz)'
            }
          },
          y: {
            beginAtZero: true,
            title: {
              display: true,
              text: 'Magnitude'
            }
          }
        }
      }
    });
  };


  // Re-render chart whenever frequencies or magnitudes change
  useEffect(() => {
    if (frequencies.length > 0 && magnitudes.length > 0) {
      renderChart();
    }
  }, [frequencies, magnitudes]);

  return (
    <div className="App">
      <h1>Audio Frequency Visualizer</h1>
      <canvas id="myChart"></canvas>
    </div>
  );
};

export default App;
