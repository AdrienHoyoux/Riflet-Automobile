<template>
  <article class="card group overflow-hidden !p-0">
    <NuxtLinkLocale :to="`/vehicules/${vehicle.slug}`" class="block">
      <div class="relative aspect-[16/10] overflow-hidden bg-ink-soft">
        <img
          :src="imageSrc"
          :alt="title"
          class="h-full w-full object-cover transition duration-700 group-hover:scale-105"
        >
        <span v-if="vehicle.is_sold" class="absolute left-3 top-3 bg-ink px-2 py-1 text-[10px] font-bold uppercase tracking-street text-chalk">
          {{ $t('vehicles.sold') }}
        </span>
      </div>
      <div class="border-t-2 border-ink p-6">
        <p class="text-[10px] font-bold uppercase tracking-street text-smoke">
          {{ vehicle.year }} · {{ formattedMileage }} · {{ fuelLabel }}
        </p>
        <h3 class="mt-3 font-display text-2xl leading-none text-ink">
          {{ title }}
        </h3>
        <p class="mt-3 line-clamp-2 text-sm leading-relaxed text-smoke">
          {{ description }}
        </p>
        <p class="mt-5 font-display text-3xl text-ink">{{ formattedPrice }}</p>
      </div>
    </NuxtLinkLocale>
  </article>
</template>

<script setup lang="ts">
import type { UsedVehicle } from '~/types/api'
import { resolveImageUrl } from '~/composables/useAssetUrl'
import { UNSPLASH_IMAGES } from '~/utils/images'

const props = defineProps<{ vehicle: UsedVehicle }>()
const { locale, t } = useI18n()

const title = computed(() => useLocalizedField(props.vehicle, 'title'))
const description = computed(() => useLocalizedField(props.vehicle, 'description'))
const imageSrc = computed(() => resolveImageUrl(props.vehicle.image) || UNSPLASH_IMAGES.usedCars)
const formattedPrice = computed(() =>
  new Intl.NumberFormat(locale.value === 'fr' ? 'fr-BE' : locale.value === 'de' ? 'de-BE' : 'nl-BE', {
    style: 'currency',
    currency: 'EUR',
    maximumFractionDigits: 0,
  }).format(Number(props.vehicle.price)),
)
const formattedMileage = computed(() =>
  new Intl.NumberFormat(locale.value === 'fr' ? 'fr-BE' : 'de-BE').format(props.vehicle.mileage) + ' km',
)
const fuelLabel = computed(() => t(`vehicles.fuel.${props.vehicle.fuel_type}`))
</script>
