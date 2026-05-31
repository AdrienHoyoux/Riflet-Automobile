<template>
  <section ref="heroRef" class="page-hero">
    <div class="container-custom">
      <p v-if="label" class="anim-label section-label text-acid">{{ label }}</p>
      <h1 class="anim-title mt-3 font-display text-5xl leading-none sm:text-6xl lg:text-7xl">
        {{ title }}
      </h1>
      <p v-if="subtitle" class="anim-subtitle mt-6 max-w-2xl text-base leading-relaxed text-smoke-light sm:text-lg">
        {{ subtitle }}
      </p>
    </div>
  </section>
</template>

<script setup lang="ts">
defineProps<{
  title: string
  subtitle?: string
  label?: string
}>()

const heroRef = ref<HTMLElement | null>(null)
const { pageHeroAnimation } = useGsap()

onMounted(() => {
  pageHeroAnimation(heroRef.value)
})
</script>
