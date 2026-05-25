<template>
  <header class="border-b border-slate-200 bg-white px-6 py-4 shadow-sm">
    <div class="flex items-center gap-6">
      <h1 class="text-lg font-bold text-slate-800">Helveti House Rent</h1>
      <nav class="flex gap-4 text-sm">
        <RouterLink
          to="/dashboard"
          class="font-medium text-slate-600 hover:text-indigo-600"
          active-class="text-indigo-600"
        >Dashboard</RouterLink>
        <RouterLink
          to="/about"
          class="font-medium text-slate-600 hover:text-indigo-600"
          active-class="text-indigo-600"
        >About</RouterLink>
      </nav>
    </div>
  </header>
</template>
