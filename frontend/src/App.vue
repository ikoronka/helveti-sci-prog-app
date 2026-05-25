<template>
  <div class="min-h-screen bg-slate-50">
    <AppHeader />
    <div class="mx-auto max-w-7xl px-6 py-8">
      <LoadingSpinner v-if="initializing" />
      <ErrorAlert v-else-if="initError" :message="initError" />
      <RouterView v-else />
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useFiltersStore } from '@/stores/filtersStore'
import AppHeader from '@/components/layout/AppHeader.vue'
import LoadingSpinner from '@/components/shared/LoadingSpinner.vue'
import ErrorAlert from '@/components/shared/ErrorAlert.vue'

const filtersStore = useFiltersStore()
const initializing = ref(true)
const initError = ref('')

onMounted(async () => {
  try {
    await filtersStore.loadFilters()
  } catch {
    initError.value = 'Could not connect to the backend. Make sure the API server is running.'
  } finally {
    initializing.value = false
  }
})
</script>
