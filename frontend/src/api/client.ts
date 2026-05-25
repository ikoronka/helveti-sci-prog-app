import axios from 'axios'
import type { DashboardData, FilterOptions, InsightResponse } from '@/types/api'

const http = axios.create({ baseURL: '/api' })

export async function fetchFilters(): Promise<FilterOptions> {
  const { data } = await http.get<FilterOptions>('/filters')
  return data
}

export async function fetchDashboardData(city: string, bhk: number): Promise<DashboardData> {
  const { data } = await http.get<DashboardData>('/data', { params: { city, bhk } })
  return data
}

export async function fetchInsight(payload: {
  city: string
  bhk: number
  n_samples: number
  slope: number
  r_squared: number
  p_value: number
}): Promise<InsightResponse> {
  const { data } = await http.post<InsightResponse>('/insight', payload)
  return data
}
