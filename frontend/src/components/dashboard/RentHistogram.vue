<template>
  <div class="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
    <h3 class="mb-4 text-sm font-semibold text-slate-700">Rent Distribution</h3>
    <Bar :data="chartData" :options="options" />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend,
} from 'chart.js'
import type { Histogram } from '@/types/api'

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend)

const props = defineProps<{ histogram: Histogram }>()

const chartData = computed(() => ({
  labels: props.histogram.labels,
  datasets: [
    {
      label: 'Listings',
      data: props.histogram.values,
      backgroundColor: 'rgba(99, 102, 241, 0.7)',
      borderColor: 'rgb(99, 102, 241)',
      borderWidth: 1,
    },
  ],
}))

const options = {
  responsive: true,
  plugins: { legend: { display: false } },
  scales: {
    x: { ticks: { maxRotation: 45, font: { size: 10 } } },
    y: { beginAtZero: true },
  },
}
</script>
