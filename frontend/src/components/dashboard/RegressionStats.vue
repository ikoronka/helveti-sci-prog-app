<template>
  <div class="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
    <h3 class="mb-3 text-sm font-semibold text-slate-700">Regression Stats</h3>
    <dl class="grid grid-cols-3 gap-3 text-center">
      <div>
        <dt class="text-xs text-slate-500">Slope (₹/sqft)</dt>
        <dd class="mt-0.5 font-mono text-lg font-semibold text-slate-800">{{ regression.slope.toFixed(2) }}</dd>
      </div>
      <div>
        <dt class="text-xs text-slate-500">R²</dt>
        <dd class="mt-0.5 font-mono text-lg font-semibold text-slate-800">{{ regression.r_squared.toFixed(3) }}</dd>
      </div>
      <div>
        <dt class="text-xs text-slate-500">p-value</dt>
        <dd class="mt-0.5 font-mono text-lg font-semibold" :class="pValueColor">
          {{ regression.p_value < 0.001 ? '< 0.001' : regression.p_value.toFixed(4) }}
        </dd>
      </div>
    </dl>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Regression } from '@/types/api'

const props = defineProps<{ regression: Regression }>()

const pValueColor = computed(() =>
  props.regression.p_value < 0.05 ? 'text-green-600' : 'text-amber-600',
)
</script>
