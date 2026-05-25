<template>
  <div class="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
    <p class="text-xs font-medium uppercase tracking-wide text-slate-500">{{ label }}</p>
    <p class="mt-1 text-2xl font-semibold text-slate-800">{{ formatted }}</p>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{ label: string; value: number; prefix?: string; suffix?: string }>()

const formatted = new Intl.NumberFormat('en-IN', { maximumFractionDigits: 0 }).format(props.value)
</script>
