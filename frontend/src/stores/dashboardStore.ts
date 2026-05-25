import { defineStore } from 'pinia'
import { ref } from 'vue'
import { fetchDashboardData } from '@/api/client'
import type { DashboardData } from '@/types/api'

export const useDashboardStore = defineStore('dashboard', () => {
  const data = ref<DashboardData | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchData(city: string, bhk: number) {
    loading.value = true
    error.value = null
    try {
      data.value = await fetchDashboardData(city, bhk)
    } catch (e: unknown) {
      error.value = e instanceof Error ? e.message : 'Failed to load data.'
      data.value = null
    } finally {
      loading.value = false
    }
  }

  return { data, loading, error, fetchData }
})
