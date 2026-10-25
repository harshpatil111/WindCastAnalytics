
import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api',
  timeout: 120000,
})

export async function fetchSummary(startDate, endDate) {
  const response = await api.get('/summary/', {
    params: { start_date: startDate, end_date: endDate },
  })
  return response.data
}

export async function fetchComparison(startDate, endDate) {
  const response = await api.get('/comparison/', {
    params: { start_date: startDate, end_date: endDate },
  })
  return response.data
}

