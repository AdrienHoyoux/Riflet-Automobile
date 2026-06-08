<template>
  <header class="border-b-2 border-ink pb-6">
    <p v-if="eyebrow" class="text-xs font-bold uppercase tracking-street text-smoke">{{ eyebrow }}</p>
    <h1 class="font-display text-4xl">{{ title }}</h1>
    <p class="mt-2 max-w-2xl text-sm leading-relaxed text-smoke">{{ description }}</p>
    <a
      v-if="pageUrl"
      :href="pageUrl"
      target="_blank"
      rel="noopener noreferrer"
      class="mt-4 inline-flex items-center gap-2 text-xs font-bold uppercase tracking-street text-ink underline-offset-4 hover:underline"
    >
      Voir la page sur le site →
    </a>
  </header>
</template>

<script setup lang="ts">
defineProps<{
  title: string
  description: string
  pageUrl?: string
  eyebrow?: string
}>()
</script>
