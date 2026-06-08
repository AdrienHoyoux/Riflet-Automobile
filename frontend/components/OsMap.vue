<template>
  <ClientOnly>
    <div class="os-map-root relative isolate z-0 overflow-hidden border-2 border-ink bg-chalk">
      <div ref="mapContainer" class="os-map-canvas h-[380px] w-full sm:h-[460px]" />
      <div class="relative z-[1] flex flex-wrap items-center justify-between gap-3 border-t-2 border-ink bg-acid/20 px-4 py-3">
        <p class="text-xs uppercase tracking-street text-ink">
          {{ attribution }}
        </p>
        <a
          :href="externalUrl"
          target="_blank"
          rel="noopener noreferrer"
          class="text-xs font-bold uppercase tracking-street text-ink underline-offset-4 hover:underline"
        >
          {{ linkLabel }}
        </a>
      </div>
    </div>
    <template #fallback>
      <div class="flex h-[380px] items-center justify-center border-2 border-ink bg-chalk sm:h-[460px]">
        <p class="text-xs font-bold uppercase tracking-street text-smoke">Chargement de la carte…</p>
      </div>
    </template>
  </ClientOnly>
</template>

<script setup lang="ts">
import type { Map as LeafletMap } from 'leaflet'

const props = withDefaults(defineProps<{
  latitude: number
  longitude: number
  linkLabel?: string
}>(), {
  linkLabel: 'OpenStreetMap',
})

const mapContainer = ref<HTMLElement | null>(null)
let mapInstance: LeafletMap | null = null
let initStarted = false

const externalUrl = computed(() =>
  `https://www.openstreetmap.org/?mlat=${props.latitude}&mlon=${props.longitude}#map=17/${props.latitude}/${props.longitude}`,
)

const attribution = '© OpenStreetMap contributors'

function refreshMapSize() {
  mapInstance?.invalidateSize()
}

/** Leaflet injecte des z-index élevés (400+) — les ramener dans le conteneur. */
function clampLeafletZIndex() {
  if (!mapContainer.value) return
  const selectors = [
    '.leaflet-pane',
    '.leaflet-top',
    '.leaflet-bottom',
    '.leaflet-control',
    '.leaflet-control-container',
  ]
  for (const selector of selectors) {
    for (const el of mapContainer.value.querySelectorAll<HTMLElement>(selector)) {
      el.style.zIndex = '1'
    }
  }
}

async function initMap() {
  if (initStarted || !mapContainer.value || !import.meta.client) return
  initStarted = true

  const L = await import('leaflet')
  await import('leaflet/dist/leaflet.css')

  mapInstance = L.map(mapContainer.value, {
    scrollWheelZoom: false,
    zoomControl: true,
  }).setView([props.latitude, props.longitude], 17)

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '',
    maxZoom: 19,
  }).addTo(mapInstance)

  const markerIcon = L.divIcon({
    className: 'riflet-map-marker',
    html: '<div class="riflet-map-marker__dot"></div>',
    iconSize: [28, 28],
    iconAnchor: [14, 14],
  })

  L.marker([props.latitude, props.longitude], { icon: markerIcon }).addTo(mapInstance)

  clampLeafletZIndex()

  await nextTick()
  refreshMapSize()
  requestAnimationFrame(refreshMapSize)
  setTimeout(refreshMapSize, 200)
  setTimeout(refreshMapSize, 600)
  setTimeout(clampLeafletZIndex, 100)

  if (mapContainer.value) {
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries.some(entry => entry.isIntersecting)) {
          refreshMapSize()
          clampLeafletZIndex()
          observer.disconnect()
        }
      },
      { threshold: 0.15 },
    )
    observer.observe(mapContainer.value)
  }
}

watch(mapContainer, (element) => {
  if (element) {
    initMap()
  }
}, { flush: 'post' })

onMounted(async () => {
  await nextTick()
  await initMap()
})

onBeforeUnmount(() => {
  mapInstance?.remove()
  mapInstance = null
  initStarted = false
})
</script>

<style>
.os-map-root {
  isolation: isolate;
}

.os-map-canvas {
  position: relative;
  isolation: isolate;
  z-index: 0;
  overflow: hidden;
}

.os-map-canvas .leaflet-container {
  height: 100%;
  width: 100%;
  z-index: 0 !important;
  background: #e8e4da;
}

.os-map-canvas .leaflet-pane,
.os-map-canvas .leaflet-top,
.os-map-canvas .leaflet-bottom,
.os-map-canvas .leaflet-control,
.os-map-canvas .leaflet-control-container {
  z-index: 1 !important;
}

.riflet-map-marker {
  background: transparent;
  border: none;
}

.riflet-map-marker__dot {
  width: 28px;
  height: 28px;
  background: #d4ff00;
  border: 3px solid #0a0a0a;
  border-radius: 50%;
  box-shadow: 0 0 0 6px rgba(212, 255, 0, 0.45);
}

.os-map-canvas .leaflet-control-zoom a {
  border: 2px solid #0a0a0a !important;
  color: #0a0a0a !important;
  font-weight: 700 !important;
}

.os-map-canvas .leaflet-control-zoom {
  border: none !important;
  box-shadow: 4px 4px 0 #0a0a0a !important;
}
</style>
