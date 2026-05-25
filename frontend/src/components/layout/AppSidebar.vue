<template>
  <aside class="w-56 shrink-0 space-y-6 rounded-xl border border-slate-200 bg-white p-5 shadow-sm self-start">
    <div>
      <label class="mb-1 block text-xs font-medium text-slate-600">City</label>
      <select
        v-model="filtersStore.city"
        class="w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400"
      >
        <option v-for="c in filtersStore.cities" :key="c" :value="c">{{ c }}</option>
      </select>
    </div>

    <div>
      <label class="mb-1 block text-xs font-medium text-slate-600">
        BHK: <span class="font-semibold text-indigo-600">{{ filtersStore.bhk }}</span>
      </label>
      <input
        v-model.number="filtersStore.bhk"
        type="range"
        :min="filtersStore.bhkMin"
        :max="filtersStore.bhkMax"
        step="1"
        class="w-full accent-indigo-600"
      />
      <div class="mt-0.5 flex justify-between text-xs text-slate-400">
        <span>{{ filtersStore.bhkMin }}</span>
        <span>{{ filtersStore.bhkMax }}</span>
      </div>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { useFiltersStore } from '@/stores/filtersStore'

const filtersStore = useFiltersStore()
</script>
