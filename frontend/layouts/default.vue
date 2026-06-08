<template>
  <div class="flex min-h-screen flex-col">
    <AppHeader />
    <main class="relative z-0 flex-1">
      <slot />
    </main>
    <AppFooter />
  </div>
</template>

<script setup lang="ts">
const { data: settings } = await useAsyncData('site-settings', fetchSettings)

provide('siteSettings', settings)

const i18nHead = useLocaleHead({
  addDirAttribute: true,
  addSeoAttributes: true,
})

useHead(i18nHead)
</script>
