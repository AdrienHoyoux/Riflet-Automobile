<template>
  <section ref="heroRef" class="relative overflow-hidden border-b-2 border-ink bg-ink">
    <div class="absolute inset-0">
      <img
        :src="heroImage"
        alt=""
        class="hero-image h-full w-full object-cover opacity-50"
      >
      <div class="absolute inset-0 bg-gradient-to-t from-ink via-ink/85 to-ink/50" />
    </div>

    <div class="container-custom relative py-24 sm:py-32 lg:py-40">
      <div class="max-w-4xl">
        <p class="hero-badge text-xs font-bold uppercase tracking-street text-acid">
          {{ $t('hero.badge') }}
        </p>
        <p class="hero-brands mt-4 inline-block border-2 border-acid bg-acid px-4 py-2 text-xs font-bold uppercase tracking-street text-ink">
          {{ $t('hero.all_brands') }}
        </p>
        <h1 class="hero-title mt-8 font-display text-6xl leading-none text-chalk sm:text-7xl lg:text-8xl">
          {{ settings?.company_name }}
        </h1>
        <p class="hero-subtitle mt-8 max-w-xl text-base leading-relaxed text-smoke-light sm:text-lg">
          {{ tagline }}
        </p>
        <div class="hero-cta mt-10 flex flex-wrap gap-4">
          <NuxtLinkLocale to="/services" class="btn-primary">
            {{ $t('hero.cta_services') }}
          </NuxtLinkLocale>
          <NuxtLinkLocale to="/contact" class="btn-secondary !border-chalk !text-chalk hover:!bg-chalk hover:!text-ink">
            {{ $t('hero.cta_contact') }}
          </NuxtLinkLocale>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import type { SiteSettings } from '~/types/api'
import { VOLVO_IMAGES } from '~/utils/images'

const settings = inject<Ref<SiteSettings | null>>('siteSettings')
const heroRef = ref<HTMLElement | null>(null)
const { heroAnimation } = useGsap()

const tagline = computed(() => {
  if (!settings?.value) return ''
  return useLocalizedField(settings.value, 'tagline')
})

const heroImage = computed(() =>
  settings?.value?.hero_image_url || VOLVO_IMAGES.hero,
)

onMounted(() => {
  heroAnimation(heroRef.value)
})
</script>
