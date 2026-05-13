import { useEffect, useState } from 'react'
import client from '../api/client'

/**
 * Fetch JSON from the FastAPI backend, returning `{ data, loading, error }`.
 *
 * Each panel calls this hook independently so a failure in one endpoint never
 * blanks the entire dashboard — only that panel renders an error state.
 */
export default function useFetch(url) {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    let cancelled = false
    setLoading(true)
    setError(null)

    client
      .get(url)
      .then((res) => {
        if (!cancelled) setData(res.data)
      })
      .catch((err) => {
        if (!cancelled) {
          setError(err?.message || 'Request failed')
        }
      })
      .finally(() => {
        if (!cancelled) setLoading(false)
      })

    return () => {
      cancelled = true
    }
  }, [url])

  return { data, loading, error }
}
