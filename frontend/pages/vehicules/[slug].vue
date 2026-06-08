<template>
  <div v-if="vehicle">
    <section class="border-b-2 border-ink bg-ink py-16 text-chalk lg:py-24">
      <div class="container-custom grid gap-8 lg:grid-cols-2 lg:items-start">
        <div class="order-2 min-w-0 lg:order-1">
          <VehicleGallery :images="galleryImages" :alt="title" />
        </div>
        <div class="order-1 lg:order-2">
          <p class="text-[10px] font-bold uppercase tracking-street text-acid">{{ $t('nav.vehicles') }}</p>
          <h1 class="mt-4 font-display text-5xl leading-none lg:text-6xl">{{ title }}</h1>
          <p class="mt-4 text-sm text-chalk/80">{{ vehicle.year }} · {{ formattedMileage }} · {{ fuelLabel }} · {{ transmissionLabel }}</p>
          <p v-if="vehicle.is_sold" class="mt-4 inline-block bg-chalk px-3 py-1 text-[10px] font-bold uppercase tracking-street text-ink">
            {{ $t('vehicles.sold') }}
          </p>
          <p class="mt-6 font-display text-3xl text-acid sm:text-4xl">{{ formattedPrice }}</p>
        </div>
      </div>
    </section>

    <section class="py-16">
      <div class="container-custom max-w-3xl">
        <h2 class="font-display text-3xl">{{ $t('vehicles.details') }}</h2>
        <p class="mt-6 whitespace-pre-line text-sm leading-relaxed text-smoke">{{ description }}</p>
        <NuxtLinkLocale
          v-if="!vehicle.is_sold"
          :to="{ path: '/contact', query: { vehicule: vehicle.slug } }"
          class="btn-primary mt-10 inline-flex"
        >
          {{ $t('vehicles.contact_cta') }}
        </NuxtLinkLocale>
        <p v-else class="mt-10 text-sm text-smoke">{{ $t('vehicles.contact_sold_text') }}</p>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import type { UsedVehicle } from '~/types/api'
import { resolveImageUrl } from '~/composables/useAssetUrl'
import { UNSPLASH_IMAGES } from '~/utils/images'

const route = useRoute()
const { locale, t } = useI18n()
const slug = route.params.slug as string

const { data: vehicle } = await useAsyncData(`vehicle-${slug}`, () => fetchVehicle(slug))

if (!vehicle.value) {
  throw createError({ statusCode: 404, statusMessage: 'Véhicule introuvable' })
}

const title = computed(() => useLocalizedField(vehicle.value as UsedVehicle, 'title'))
const description = computed(() => useLocalizedField(vehicle.value as UsedVehicle, 'description'))
const galleryImages = computed(() => {
  const fromApi = vehicle.value?.images?.map(url => resolveImageUrl(url)).filter(Boolean) as string[]
  if (fromApi?.length) return fromApi
  const fallback = resolveImageUrl(vehicle.value?.image)
  return fallback ? [fallback] : [UNSPLASH_IMAGES.usedCars]
})
const formattedPrice = computed(() =>
  new Intl.NumberFormat('fr-BE', { style: 'currency', currency: 'EUR', maximumFractionDigits: 0 }).format(Number(vehicle.value!.price)),
)
const formattedMileage = computed(() =>
  new Intl.NumberFormat('fr-BE').format(vehicle.value!.mileage) + ' km',
)
const fuelLabel = computed(() => t(`vehicles.fuel.${vehicle.value!.fuel_type}`))
const transmissionLabel = computed(() => t(`vehicles.transmission.${vehicle.value!.transmission}`))

useSeoMetaTags(title.value, description.value.slice(0, 160), galleryImages.value[0])
</script>
