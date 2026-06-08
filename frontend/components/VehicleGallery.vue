<template>
  <div
    class="relative w-full min-w-0"
    @mouseenter="pauseAutoplay"
    @mouseleave="resumeAutoplay"
    @focusin="pauseAutoplay"
    @focusout="resumeAutoplay"
  >
    <div
      class="relative aspect-[4/3] w-full overflow-hidden border-2 border-chalk bg-ink-soft sm:aspect-[16/10]"
      @touchstart.passive="onTouchStart"
      @touchend="onTouchEnd"
    >
      <div
        class="flex h-full w-full transition-transform duration-500 ease-out"
        :style="{ transform: `translateX(-${currentIndex * 100}%)` }"
      >
        <div
          v-for="(src, index) in images"
          :key="`${src}-${index}`"
          class="h-full w-full min-w-full shrink-0 basis-full"
        >
          <img
            :src="src"
            :alt="`${alt} — ${index + 1}`"
            class="h-full w-full object-cover"
            draggable="false"
          >
        </div>
      </div>

      <template v-if="images.length > 1">
        <button
          type="button"
          class="absolute left-2 top-1/2 z-10 flex h-9 w-9 -translate-y-1/2 items-center justify-center border-2 border-chalk bg-ink/85 text-sm font-bold text-chalk backdrop-blur sm:left-3 sm:h-auto sm:w-auto sm:px-3 sm:py-2"
          :aria-label="$t('vehicles.gallery_prev')"
          @click="goPrev"
        >
          ←
        </button>
        <button
          type="button"
          class="absolute right-2 top-1/2 z-10 flex h-9 w-9 -translate-y-1/2 items-center justify-center border-2 border-chalk bg-ink/85 text-sm font-bold text-chalk backdrop-blur sm:right-3 sm:h-auto sm:w-auto sm:px-3 sm:py-2"
          :aria-label="$t('vehicles.gallery_next')"
          @click="goNext"
        >
          →
        </button>
        <span class="absolute bottom-2 right-2 bg-ink/85 px-2 py-1 text-[10px] font-bold uppercase tracking-street text-chalk backdrop-blur sm:bottom-3 sm:right-3">
          {{ currentIndex + 1 }} / {{ images.length }}
        </span>
      </template>
    </div>

    <div
      v-if="images.length > 1"
      class="mt-3 flex gap-2 overflow-x-auto pb-1 [-ms-overflow-style:none] [scrollbar-width:none] [&::-webkit-scrollbar]:hidden"
    >
      <button
        v-for="(src, index) in images"
        :key="`thumb-${src}-${index}`"
        type="button"
        class="relative h-14 w-20 shrink-0 overflow-hidden border-2 transition sm:h-16 sm:w-24"
        :class="index === currentIndex ? 'border-acid' : 'border-chalk/40 opacity-70 hover:opacity-100'"
        :aria-label="$t('vehicles.gallery_go_to', { index: index + 1 })"
        @click="goTo(index)"
      >
        <img :src="src" :alt="`${alt} ${index + 1}`" class="h-full w-full object-cover" draggable="false">
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  images: string[]
  alt: string
}>()

const itemCount = computed(() => props.images.length)

const {
  currentIndex,
  goTo,
  goNext,
  goPrev,
  startAutoplay,
  pauseAutoplay,
  resumeAutoplay,
  onTouchStart,
  onTouchEnd,
} = useCarousel(itemCount, 5000)

watch(
  () => props.images,
  () => {
    currentIndex.value = 0
    startAutoplay()
  },
  { deep: true },
)

onMounted(startAutoplay)
</script>
