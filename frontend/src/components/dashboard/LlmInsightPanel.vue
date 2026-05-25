<template>
  <div class="rounded-xl border border-indigo-100 bg-indigo-50 p-5 shadow-sm">
    <div class="flex items-center justify-between">
      <h3 class="text-sm font-semibold text-indigo-800">AI Research Insight</h3>
      <button
        :disabled="loading"
        class="rounded-lg bg-indigo-600 px-3 py-1.5 text-xs font-medium text-white transition hover:bg-indigo-700 disabled:opacity-50"
        @click="generate"
      >
        {{ loading ? 'Generating…' : 'Generate' }}
      </button>
    </div>

    <p v-if="error" class="mt-3 text-sm text-red-600">{{ error }}</p>
    <p v-else-if="conclusion" class="mt-3 text-sm leading-relaxed text-indigo-900">{{ conclusion }}</p>
    <p v-else class="mt-3 text-sm text-indigo-400">Click "Generate" to get an AI-generated conclusion for the current selection.</p>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { fetchInsight } from '@/api/client'
import type { Regression } from '@/types/api'

const props = defineProps<{
  city: string
  bhk: number
  nSamples: number
  regression: Regression
}>()

const conclusion = ref('')
const loading = ref(false)
const error = ref('')

async function generate() {
  loading.value = true
  error.value = ''
  try {
    const res = await fetchInsight({
      city: props.city,
      bhk: props.bhk,
      n_samples: props.nSamples,
      slope: props.regression.slope,
      r_squared: props.regression.r_squared,
      p_value: props.regression.p_value,
    })
    conclusion.value = res.conclusion
  } catch {
    error.value = 'Could not reach the AI service. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>
