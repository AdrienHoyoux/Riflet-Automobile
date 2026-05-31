<template>
  <div class="inline-flex border-2 border-ink">
    <NuxtLink
      v-for="loc in locales"
      :key="loc.code"
      :to="switchLocalePath(loc.code)"
      class="px-3 py-2 text-[10px] font-bold uppercase tracking-street transition"
      :class="locale === loc.code
        ? 'bg-ink text-chalk'
        : 'bg-chalk text-ink hover:bg-acid'"
    >
      {{ loc.code }}
    </NuxtLink>
  </div>
</template>

<script setup lang="ts">
const { locale, locales } = useI18n()
const switchLocalePath = useSwitchLocalePath()
</script>
