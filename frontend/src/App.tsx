import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [backendStatus, setBackendStatus] = useState("checking...")
  useEffect(() => {
    const fetchBackendData = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/health')

        if (!response.ok) {
          throw new Error('Network response was not ok')
        }

        const result = await response.json()
        setBackendStatus(result.status)

      } catch (error) {
        console.error('Error fetching backend data:', error)
        setBackendStatus("error")
      }
    };

    fetchBackendData();
  }, []);

  return (
    <main>
       <h1>AI Chess Coach</h1>
      <p>Backend status: {backendStatus}</p>
    </main> 
  );
}

export default App
