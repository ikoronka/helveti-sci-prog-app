<template>
  <div class="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
    <h3 class="mb-4 text-sm font-semibold text-slate-700">Rent vs. Size</h3>
    <Scatter :data="chartData" :options="options" />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Scatter } from 'vue-chartjs'
import {
  Chart as ChartJS,
  LinearScale,
  PointElement,
  LineElement,
  LineController,
  Tooltip,
  Legend,
} from 'chart.js'
import type { ChartData } from 'chart.js'
import type { Regression, ScatterPoint } from '@/types/api'

ChartJS.register(LinearScale, PointElement, LineElement, LineController, Tooltip, Legend)

const props = defineProps<{ scatter: ScatterPoint[]; regression: Regression }>()

const chartData = computed(() => {
  const xValues = props.scatter.map((p) => p.x)
  const xMin = Math.min(...xValues)
  const xMax = Math.max(...xValues)
  const { slope, intercept } = props.regression
  const regressionLine = [
    { x: xMin, y: slope * xMin + intercept },
    { x: xMax, y: slope * xMax + intercept },
  ]

  // Chart.js allows mixing scatter + line datasets at runtime even though TS
  // types don't permit it cleanly; cast the whole object once.
  return {
    datasets: [
      {
        label: 'Listings',
        data: props.scatter,
        backgroundColor: 'rgba(99, 102, 241, 0.4)',
        pointRadius: 3,
      },
      {
        label: 'Regression line',
        data: regressionLine,
        type: 'line',
        borderColor: 'rgb(239, 68, 68)',
        borderWidth: 2,
        pointRadius: 0,
        fill: false,
      },
    ],
  } as ChartData<'scatter'>
})

const options = {
  responsive: true,
  plugins: { legend: { position: 'top' as const } },
  scales: {
    x: { title: { display: true, text: 'Size (sqft)' } },
    y: { title: { display: true, text: 'Rent (₹)' } },
  },
}
</script>
