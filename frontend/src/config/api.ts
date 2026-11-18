import axios from 'axios'

/**
 * Configured Axios instance — the single HTTP client for all API calls.
 *
 * Base URL resolution:
 *   - Local dev: empty (Vite proxy forwards /api → http://localhost:8000)
 *   - Docker / production: set VITE_API_BASE_URL in environment
 *
 * Response interceptor unwraps the standard API envelope so callers
 * receive `data` directly instead of { success, message, data }.
 */
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api/v1',
  headers: {
    'Content-Type': 'application/json',
    Accept: 'application/json',
  },
  timeout: 15_000,
})

// ── Response interceptor ───────────────────────────────────────────────────
apiClient.interceptors.response.use(
  (response) => {
    // Unwrap { success, message, data } envelope → return data directly
    const envelope = response.data as { success?: boolean; data?: unknown }
    if (envelope && typeof envelope === 'object' && 'data' in envelope) {
      return { ...response, data: envelope.data }
    }
    return response
  },
  (error: unknown) => {
    if (axios.isAxiosError(error)) {
      const message: string =
        (error.response?.data as { message?: string })?.message ??
        error.message ??
        'An unexpected error occurred.'
      return Promise.reject(new Error(message))
    }
    return Promise.reject(error)
  }
)

export default apiClient
