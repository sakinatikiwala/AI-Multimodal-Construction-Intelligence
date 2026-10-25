import React, { useCallback, useEffect, useState } from 'react'
import axios from 'axios'
import { RefreshCw } from 'lucide-react'

const AnalysisHistory = () => {
    const [items, setItems] = useState([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState('')

    const loadHistory = useCallback(async () => {
        setLoading(true)
        setError('')
        try {
            const response = await axios.get('http://localhost:8000/api/history')
            setItems(response.data)
        } catch (requestError) {
            setError(
                requestError.response?.status === 404
                    ? 'History API not found. Restart the FastAPI backend to load the new endpoint.'
                    : requestError.response?.data?.detail || 'Could not load analysis history.'
            )
        } finally {
            setLoading(false)
        }
    }, [])

    useEffect(() => {
        loadHistory()
    }, [loadHistory])

    return (
        <section>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                    <h1>Analysis History</h1>
                    <p>Saved AI analyses from this application.</p>
                </div>
                <button className="btn btn-primary" onClick={loadHistory} disabled={loading}>
                    <RefreshCw size={16} style={{ marginRight: 8 }} />
                    {loading ? 'Loading...' : 'Refresh'}
                </button>
            </div>

            {error && <div className="card" role="alert">{error}</div>}
            {!loading && !error && items.length === 0 && (
                <div className="card">No analyses have been saved yet.</div>
            )}

            {items.map((item) => (
                <article className="card" key={item.id}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', gap: '1rem', flexWrap: 'wrap' }}>
                        <h3>{item.feature}</h3>
                        <time dateTime={item.created_at}>
                            {new Date(item.created_at).toLocaleString()}
                        </time>
                    </div>
                    <details>
                        <summary style={{ cursor: 'pointer', fontWeight: 700 }}>View request and response</summary>
                        <div className="grid-2 mt-4">
                            <div>
                                <h4>Request</h4>
                                <pre style={{ whiteSpace: 'pre-wrap', overflowWrap: 'anywhere' }}>
                                    {JSON.stringify(item.request_data, null, 2)}
                                </pre>
                            </div>
                            <div>
                                <h4>Response</h4>
                                <pre style={{ whiteSpace: 'pre-wrap', overflowWrap: 'anywhere' }}>
                                    {JSON.stringify(item.response_data, null, 2)}
                                </pre>
                            </div>
                        </div>
                    </details>
                </article>
            ))}
        </section>
    )
}

export default AnalysisHistory
