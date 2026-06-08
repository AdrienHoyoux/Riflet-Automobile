import type { ComputedRef, Ref } from 'vue'

export function useCarousel(
  itemCount: Ref<number> | ComputedRef<number>,
  autoplayMs = 0,
) {
  const currentIndex = ref(0)
  const autoplayTimer = ref<ReturnType<typeof setInterval> | null>(null)
  const touchStartX = ref<number | null>(null)

  function goTo(index: number) {
    const count = unref(itemCount)
    if (!count) return
    currentIndex.value = ((index % count) + count) % count
  }

  function goNext() {
    goTo(currentIndex.value + 1)
  }

  function goPrev() {
    goTo(currentIndex.value - 1)
  }

  function stopAutoplay() {
    if (autoplayTimer.value) {
      clearInterval(autoplayTimer.value)
      autoplayTimer.value = null
    }
  }

  function startAutoplay() {
    stopAutoplay()
    if (!autoplayMs || unref(itemCount) <= 1) return
    autoplayTimer.value = setInterval(goNext, autoplayMs)
  }

  function pauseAutoplay() {
    stopAutoplay()
  }

  function resumeAutoplay() {
    startAutoplay()
  }

  function onTouchStart(event: TouchEvent) {
    touchStartX.value = event.touches[0]?.clientX ?? null
    pauseAutoplay()
  }

  function onTouchEnd(event: TouchEvent) {
    if (touchStartX.value === null) return
    const endX = event.changedTouches[0]?.clientX ?? touchStartX.value
    const delta = endX - touchStartX.value
    touchStartX.value = null

    if (Math.abs(delta) >= 48) {
      if (delta > 0) goPrev()
      else goNext()
    }

    resumeAutoplay()
  }

  watch(itemCount, () => {
    currentIndex.value = 0
    startAutoplay()
  })

  onBeforeUnmount(stopAutoplay)

  return {
    currentIndex,
    goTo,
    goNext,
    goPrev,
    startAutoplay,
    stopAutoplay,
    pauseAutoplay,
    resumeAutoplay,
    onTouchStart,
    onTouchEnd,
  }
}
