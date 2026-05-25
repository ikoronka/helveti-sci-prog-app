import { defineStore } from 'pinia'
import { ref } from 'vue'
import { fetchFilters } from '@/api/client'

export const useFiltersStore = defineStore('filters', () => {
  const city = ref('')
  const bhk = ref(1)
  const cities = ref<string[]>([])
  const bhkMin = ref(1)
  const bhkMax = ref(6)

  async function loadFilters() {
    const data = await fetchFilters()
    cities.value = data.cities
    bhkMin.value = data.bhk_min
    bhkMax.value = data.bhk_max
    city.value = data.cities[0] ?? ''
    bhk.value = data.bhk_min
  }

  return { city, bhk, cities, bhkMin, bhkMax, loadFilters }
})
