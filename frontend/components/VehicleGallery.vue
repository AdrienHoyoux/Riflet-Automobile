<template>
  <div
    class="relative"
    @mouseenter="pauseAutoplay"
    @mouseleave="resumeAutoplay"
    @focusin="pauseAutoplay"
    @focusout="resumeAutoplay"
  >
    <div class="relative aspect-[16/10] overflow-hidden border-2 border-chalk bg-ink-soft">
      <div
        class="flex h-full transition-transform duration-500 ease-out"
        :style="{ transform: `translateX(-${currentIndex * 100}%)` }"
      >
        <img
          v-for="(src, index) in images"
          :key="`${src}-${index}`"
          :src="src"
          :alt="`${alt} — ${index + 1}`"
          class="h-full w-full shrink-0 object-cover"
        >
      </div>

      <template v-if="images.length > 1">
        <button
          type="button"
          class="absolute left-3 top-1/2 -translate-y-1/2 border-2 border-chalk bg-ink/80 px-3 py-2 text-sm font-bold text-chalk backdrop-blur hover:bg-ink"
          :aria-label="$t('vehicles.gallery_prev')"
          @click="goPrev"
        >
          ←
        </button>
        <button
          type="button"
          class="absolute right-3 top-1/2 -translate-y-1/2 border-2 border-chalk bg-ink/80 px-3 py-2 text-sm font-bold text-chalk backdrop-blur hover:bg-ink"
          :aria-label="$t('vehicles.gallery_next')"
          @click="goNext"
        >
          →
        </button>
        <span class="absolute bottom-3 right-3 bg-ink/80 px-2 py-1 text-[10px] font-bold uppercase tracking-street text-chalk backdrop-blur">
          {{ currentIndex + 1 }} / {{ images.length }}
        </span>
      </template>
    </div>

    <div
      v-if="images.length > 1"
      class="mt-3 flex gap-2 overflow-x-auto pb-1"
    >
      <button
        v-for="(src, index) in images"
        :key="`thumb-${src}-${index}`"
        type="button"
        class="relative h-16 w-24 shrink-0 overflow-hidden border-2 transition"
        :class="index === currentIndex ? 'border-acid' : 'border-chalk/40 opacity-70 hover:opacity-100'"
        :aria-label="$t('vehicles.gallery_go_to', { index: index + 1 })"
        @click="goTo(index)"
      >
        <img :src="src" :alt="`${alt} ${index + 1}`" class="h-full w-full object-cover">
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  images: string[]
  alt: string
}>()

const currentIndex = ref(0)
const autoplayTimer = ref<ReturnType<typeof setInterval> | null>(null)

function goTo(index: number) {
  if (!props.images.length) return
  currentIndex.value = ((index % props.images.length) + props.images.length) % props.images.length
}

function goNext() {
  goTo(currentIndex.value + 1)
}

function goPrev() {
  goTo(currentIndex.value - 1)
}

function startAutoplay() {
  stopAutoplay()
  if (props.images.length <= 1) return
  autoplayTimer.value = setInterval(goNext, 5000)
}

function stopAutoplay() {
  if (autoplayTimer.value) {
    clearInterval(autoplayTimer.value)
    autoplayTimer.value = null
  }
}

function pauseAutoplay() {
  stopAutoplay()
}

function resumeAutoplay() {
  startAutoplay()
}

watch(
  () => props.images,
  () => {
    currentIndex.value = 0
    startAutoplay()
  },
  { deep: true },
)

onMounted(startAutoplay)
onBeforeUnmount(stopAutoplay)
</script>
