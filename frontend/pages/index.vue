<template>
  <div>
    <HeroSection />

    <section ref="servicesSection" class="py-16 lg:py-24">
      <div class="container-custom">
        <div class="flex flex-wrap items-end justify-between gap-6 border-b-2 border-ink pb-6">
          <div>
            <p class="anim-label section-label">{{ $t('nav.services') }}</p>
            <h2 class="anim-title section-title mt-2">{{ $t('home.services_title') }}</h2>
            <p class="anim-subtitle section-subtitle">{{ $t('home.services_subtitle') }}</p>
          </div>
          <NuxtLinkLocale to="/services" class="anim-cta btn-secondary">
            {{ $t('home.view_all') }}
          </NuxtLinkLocale>
        </div>

        <div ref="servicesGrid" class="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          <ServiceCard
            v-for="service in services?.slice(0, 6)"
            :key="service.id"
            :service="service"
          />
        </div>
      </div>
    </section>

    <section ref="newsSection" class="border-y-2 border-ink bg-ink py-16 text-chalk lg:py-24">
      <div class="container-custom">
        <div class="flex flex-wrap items-end justify-between gap-6">
          <div>
            <p class="anim-label section-label text-acid">{{ $t('nav.news') }}</p>
            <h2 class="anim-title section-title mt-2 text-chalk">{{ $t('home.news_title') }}</h2>
            <p class="anim-subtitle section-subtitle text-smoke-light">{{ $t('home.news_subtitle') }}</p>
          </div>
          <NuxtLinkLocale to="/actualites" class="anim-cta btn-primary">
            {{ $t('home.view_all') }}
          </NuxtLinkLocale>
        </div>

        <div ref="newsGrid" class="mt-10 grid gap-6 md:grid-cols-2">
          <NewsCard
            v-for="(article, index) in news?.slice(0, 2)"
            :key="article.id"
            :article="article"
            :index="index"
          />
        </div>
      </div>
    </section>

    <ReviewsSection v-if="reviews?.length" :reviews="reviews" />

    <section ref="whySection" class="py-16 lg:py-24">
      <div class="container-custom">
        <p class="anim-label section-label text-center">{{ $t('nav.about') }}</p>
        <h2 class="anim-title section-title mt-2 text-center">{{ $t('home.why_title') }}</h2>
        <div class="mx-auto mt-12 grid max-w-5xl gap-px bg-ink sm:grid-cols-3">
          <div
            v-for="(item, index) in whyItems"
            :key="index"
            class="bg-chalk p-8"
          >
            <span class="why-number-badge anim-number">
              {{ String(index + 1).padStart(2, '0') }}
            </span>
            <p class="anim-why-text mt-4 text-sm font-medium leading-relaxed text-ink">{{ item }}</p>
          </div>
        </div>
      </div>
    </section>

    <section ref="ctaSection" class="border-t-2 border-ink bg-acid py-16 lg:py-20">
      <div class="container-custom text-center">
        <h2 class="anim-title font-display text-4xl leading-none text-ink sm:text-5xl">
          {{ $t('home.cta_title') }}
        </h2>
        <p class="anim-subtitle mx-auto mt-4 max-w-xl text-sm font-medium text-ink/80">
          {{ $t('home.cta_text') }}
        </p>
        <div class="anim-cta mt-8 flex flex-wrap justify-center gap-4">
          <a
            v-if="settings?.phone"
            :href="phoneHref(settings.phone)"
            class="btn-secondary !bg-ink !text-chalk hover:!bg-ink-soft"
          >
            {{ settings.phone }}
          </a>
          <NuxtLinkLocale to="/contact" class="btn-secondary">
            {{ $t('hero.cta_contact') }}
          </NuxtLinkLocale>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import type { SiteSettings } from '~/types/api'
import { LOGO_URL, VOLVO_IMAGES } from '~/utils/images'

const { t } = useI18n()
const settings = inject<Ref<SiteSettings | null>>('siteSettings')
const config = useRuntimeConfig()
const logoUrl = useLogoUrl(settings)

const servicesSection = ref<HTMLElement | null>(null)
const newsSection = ref<HTMLElement | null>(null)
const whySection = ref<HTMLElement | null>(null)
const ctaSection = ref<HTMLElement | null>(null)
const servicesGrid = ref<HTMLElement | null>(null)
const newsGrid = ref<HTMLElement | null>(null)

const { revealSection, revealWhySection, staggerIn } = useGsap()

const [{ data: services }, { data: news }, { data: reviews }] = await Promise.all([
  useAsyncData('home-services', fetchServices),
  useAsyncData('home-news', fetchNews),
  useAsyncData('home-reviews', fetchReviews),
])

useSeoMetaTags(
  t('seo.home_title'),
  t('seo.home_description'),
  settings?.value?.hero_image_url || VOLVO_IMAGES.hero,
)

useHead({
  script: [
    {
      type: 'application/ld+json',
      innerHTML: JSON.stringify({
        '@context': 'https://schema.org',
        '@type': 'AutoRepair',
        name: settings?.value?.company_name || 'Riflet Automobile',
        image: logoUrl.value || `${config.public.siteUrl}${LOGO_URL}`,
        address: {
          '@type': 'PostalAddress',
          streetAddress: settings?.value?.address,
          addressLocality: settings?.value?.city,
          postalCode: settings?.value?.postal_code,
          addressCountry: 'BE',
        },
        telephone: settings?.value?.phone,
        email: settings?.value?.email,
        url: useRuntimeConfig().public.siteUrl,
      }),
    },
  ],
})

const whyItems = computed(() => [
  t('home.why_items.all_brands'),
  t('home.why_items.quality'),
  t('home.why_items.location'),
])

onMounted(() => {
  revealSection(servicesSection.value)
  revealSection(newsSection.value)
  revealWhySection(whySection.value)
  revealSection(ctaSection.value)

  if (servicesGrid.value) {
    staggerIn(servicesGrid.value.children, { trigger: servicesGrid.value })
  }
  if (newsGrid.value) {
    staggerIn(newsGrid.value.children, { trigger: newsGrid.value })
  }
})
</script>
