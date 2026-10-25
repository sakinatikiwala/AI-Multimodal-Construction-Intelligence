const configuredApiUrl = import.meta.env.VITE_API_BASE_URL

export const API_BASE_URL = configuredApiUrl
    ? configuredApiUrl.startsWith('http')
        ? configuredApiUrl
        : `https://${configuredApiUrl}`
    : import.meta.env.DEV
        ? 'http://localhost:8000'
        : ''
