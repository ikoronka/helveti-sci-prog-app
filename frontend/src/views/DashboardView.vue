<template>
  <div class="flex gap-6">
    <AppSidebar />

    <main class="flex-1 space-y-6 min-w-0">
      <LoadingSpinner v-if="dashboardStore.loading" />
      <ErrorAlert v-else-if="dashboardStore.error" :message="dashboardStore.error" />

      <template v-else-if="dashboardStore.data">
        <!-- KPI row -->
        <div class="grid grid-cols-3 gap-4">
          <KpiCard label="Avg Rent (₹)" :value="dashboardStore.data.kpis.avg_rent" />
          <KpiCard label="Median Size (sqft)" :value="dashboardStore.data.kpis.median_size" />
          <KpiCard label="Listings" :value="dashboardStore.data.kpis.count" />
        </div>

        <!-- Charts -->
        <div class="grid grid-cols-2 gap-6">
          <RentHistogram :histogram="dashboardStore.data.histogram" />
          <RentVsSizeScatter
            :scatter="dashboardStore.data.scatter"
            :regression="dashboardStore.data.regression"
          />
        </div>

        <!-- Regression stats + AI insight -->
        <div class="grid grid-cols-2 gap-6">
          <RegressionStats :regression="dashboardStore.data.regression" />
          <LlmInsightPanel
            :city="filtersStore.city"
            :bhk="filtersStore.bhk"
            :n-samples="dashboardStore.data.kpis.count"
            :regression="dashboardStore.data.regression"
          />
        </div>
      </template>
    </main>
  </div>
</template>

<script setup lang="ts">
import { watch } from 'vue'
import { useFiltersStore } from '@/stores/filtersStore'
import { useDashboardStore } from '@/stores/dashboardStore'
import AppSidebar from '@/components/layout/AppSidebar.vue'
import LoadingSpinner from '@/components/shared/LoadingSpinner.vue'
import ErrorAlert from '@/components/shared/ErrorAlert.vue'
import KpiCard from '@/components/dashboard/KpiCard.vue'
import RentHistogram from '@/components/dashboard/RentHistogram.vue'
import RentVsSizeScatter from '@/components/dashboard/RentVsSizeScatter.vue'
import RegressionStats from '@/components/dashboard/RegressionStats.vue'
import LlmInsightPanel from '@/components/dashboard/LlmInsightPanel.vue'

const filtersStore = useFiltersStore()
const dashboardStore = useDashboardStore()

watch(
  [() => filtersStore.city, () => filtersStore.bhk],
  ([city, bhk]) => {
    if (city) dashboardStore.fetchData(city, bhk)
  },
  { immediate: true },
)
</script>
