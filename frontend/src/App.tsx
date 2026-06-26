import { useState, useEffect } from 'react'

function App() {
  const [status, setStatus] = useState<string>("Checking backend...")

  useEffect(() => {
    fetch('http://localhost:8000/api/health')
      .then(res => res.json())
      .then(data => setStatus(data.message))
      .catch(err => setStatus("Error connecting to backend: " + err.message))
  }, [])

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center justify-center">
      <div className="bg-white p-8 rounded-lg shadow-md max-w-md w-full text-center">
        <h1 className="text-3xl font-bold text-blue-600 mb-4">DevFlow Phase 1</h1>
        <p className="text-gray-700 mb-2 font-medium">Frontend: React + Tailwind + Vite (OK)</p>
        <p className={`font-medium ${status.includes('Error') ? 'text-red-500' : 'text-green-500'}`}>
          Backend: {status}
        </p>
      </div>
    </div>
  )
}

export default App
