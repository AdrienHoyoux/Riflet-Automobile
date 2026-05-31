<template>
  <article ref="cardRef" class="card group flex h-full flex-col overflow-hidden !p-0">
    <div class="aspect-[4/3] overflow-hidden bg-ink-soft">
      <img
        :src="imageSrc"
        :alt="title"
        class="h-full w-full object-cover grayscale transition duration-700 group-hover:scale-105 group-hover:grayscale-0"
      >
    </div>
    <div class="flex flex-1 flex-col border-t-2 border-ink p-6">
      <span class="text-[10px] font-bold uppercase tracking-street text-smoke">
        {{ String(service.order).padStart(2, '0') }}
      </span>
      <h3 class="mt-2 font-display text-2xl leading-none text-ink">
        {{ title }}
      </h3>
      <p class="mt-4 flex-1 text-sm leading-relaxed text-smoke">
        {{ description }}
      </p>
    </div>
  </article>
</template>

<script setup lang="ts">
import type { Service } from '~/types/api'
import { getServiceImage } from '~/utils/images'

const props = defineProps<{
  service: Service
}>()

const cardRef = ref<HTMLElement | null>(null)
const { fadeInUp } = useGsap()

const title = computed(() => useLocalizedField(props.service, 'title'))
const description = computed(() => useLocalizedField(props.service, 'description'))
const imageSrc = computed(() => getServiceImage(props.service.order, props.service.image))

onMounted(() => {
  fadeInUp(cardRef.value)
})
</script>
