<template>
  <article class="card group overflow-hidden !p-0">
    <NuxtLinkLocale :to="`/vehicules/${vehicle.slug}`" class="block">
      <div
        class="relative aspect-[16/10] overflow-hidden bg-ink-soft transition-transform duration-700 group-hover:scale-105"
        @mouseenter="startHoverSlideshow"
        @mouseleave="stopHoverSlideshow"
      >
        <img
          v-for="(src, index) in galleryImages"
          :key="`${src}-${index}`"
          :src="src"
          :alt="title"
          class="absolute inset-0 h-full w-full object-cover transition-opacity duration-500"
          :class="index === currentIndex ? 'opacity-100' : 'opacity-0'"
        >
        <span v-if="vehicle.is_sold" class="absolute left-3 top-3 z-10 bg-ink px-2 py-1 text-[10px] font-bold uppercase tracking-street text-chalk">
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

const currentIndex = ref(0)
const hoverTimer = ref<ReturnType<typeof setInterval> | null>(null)

const title = computed(() => useLocalizedField(props.vehicle, 'title'))
const description = computed(() => useLocalizedField(props.vehicle, 'description'))
const galleryImages = computed(() => {
  const fromApi = props.vehicle.images?.map(url => resolveImageUrl(url)).filter(Boolean) as string[]
  if (fromApi?.length) return fromApi
  const single = resolveImageUrl(props.vehicle.image)
  return single ? [single] : [UNSPLASH_IMAGES.usedCars]
})
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

function startHoverSlideshow() {
  if (galleryImages.value.length <= 1) return
  stopHoverSlideshow()
  hoverTimer.value = setInterval(() => {
    currentIndex.value = (currentIndex.value + 1) % galleryImages.value.length
  }, 2000)
}

function stopHoverSlideshow() {
  if (hoverTimer.value) {
    clearInterval(hoverTimer.value)
    hoverTimer.value = null
  }
  currentIndex.value = 0
}

onBeforeUnmount(stopHoverSlideshow)
</script>
