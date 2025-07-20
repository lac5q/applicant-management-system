import { useEffect, useState } from 'react'

export default function TestPage() {
  const [data, setData] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const testAPI = async () => {
      try {
        console.log('Testing API...')
        const response = await fetch('/api/applicants/')
        console.log('Response status:', response.status)
        
        if (!response.ok) {
          throw new Error(`API error: ${response.status}`)
        }
        
        const result = await response.json()
        console.log('API result:', result)
        setData(result)
        setLoading(false)
      } catch (err) {
        console.error('Test error:', err)
        setError(err instanceof Error ? err.message : 'Unknown error')
        setLoading(false)
      }
    }

    testAPI()
  }, [])

  if (loading) return <div>Loading...</div>
  if (error) return <div>Error: {error}</div>

  return (
    <div style={{ padding: '20px' }}>
      <h1>API Test Results</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  )
} 