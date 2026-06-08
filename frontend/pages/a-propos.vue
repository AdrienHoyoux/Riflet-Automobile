<template>
  <div>
    <PageHero
      :title="aboutPageTitle"
      :subtitle="aboutPageSubtitle"
      :label="$t('nav.about')"
    />

    <section class="py-16 lg:py-24">
      <div class="container-custom">
        <div class="grid gap-12 lg:grid-cols-2 lg:gap-16">
          <div ref="aboutImageRef">
            <img
              :src="aboutImage"
              :alt="settings?.company_name"
              class="aspect-[4/3] w-full object-cover"
            >
            <p class="mt-6 inline-block border-2 border-ink bg-acid px-4 py-2 text-xs font-bold uppercase tracking-street text-ink">
              {{ $t('hero.all_brands') }}
            </p>
            <div ref="aboutTextRef" class="mt-8 whitespace-pre-line text-base leading-relaxed text-smoke">
              {{ aboutText }}
            </div>
          </div>

          <div ref="aboutSideRef" class="space-y-6">
            <OpeningHours />

            <div class="card">
              <h3 class="font-display text-2xl leading-none text-ink">
                {{ $t('about.location_title') }}
              </h3>
              <address class="mt-6 not-italic text-sm leading-relaxed text-smoke">
                <strong class="font-bold uppercase tracking-street text-ink">{{ settings?.company_name }}</strong><br>
                {{ settings?.address }}<br>
                {{ settings?.postal_code }} {{ settings?.city }}<br>
                {{ settings?.country }}
              </address>
              <div class="mt-6 space-y-2 text-sm">
                <a
                  v-if="settings?.phone"
                  :href="phoneHref(settings.phone)"
                  class="block font-bold uppercase tracking-street text-ink hover:underline"
                >
                  {{ settings.phone }}
                </a>
                <a
                  v-if="settings?.email"
                  :href="`mailto:${settings.email}`"
                  class="block text-smoke hover:text-ink hover:underline"
                >
                  {{ settings.email }}
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section v-if="mapCoords" ref="mapSection" class="relative z-0 border-t-2 border-ink bg-chalk-dark pb-16 lg:pb-24">
      <div class="container-custom">
        <p class="anim-label section-label">{{ $t('about.map_label') }}</p>
        <h2 class="anim-title section-title mt-2">{{ $t('about.map_title') }}</h2>
        <div class="mt-8">
          <OsMap
            :latitude="mapCoords.lat"
            :longitude="mapCoords.lng"
            :link-label="$t('about.open_in_osm')"
          />
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import type { SiteSettings } from '~/types/api'
import { resolveImageUrl } from '~/composables/useAssetUrl'
import { VOLVO_IMAGES } from '~/utils/images'

const { t } = useI18n()
const settings = inject<Ref<SiteSettings | null>>('siteSettings')

const aboutImageRef = ref<HTMLElement | null>(null)
const aboutTextRef = ref<HTMLElement | null>(null)
const aboutSideRef = ref<HTMLElement | null>(null)
const mapSection = ref<HTMLElement | null>(null)

const { slideIn, revealSection } = useGsap()

const aboutPageTitle = useSettingsField(settings, 'about_title', 'about.title')
const aboutPageSubtitle = useSettingsField(settings, 'about_subtitle', 'about.subtitle')

const aboutText = computed(() => {
  if (!settings?.value) return ''
  return useLocalizedField(settings.value, 'about')
})

const aboutImage = computed(() =>
  resolveImageUrl(settings?.value?.about_image_url)
    || resolveImageUrl(settings?.value?.hero_image_url)
    || VOLVO_IMAGES.about,
)

const mapCoords = computed(() => {
  const s = settings?.value
  if (!s?.latitude || !s?.longitude) return null
  return {
    lat: Number(s.latitude),
    lng: Number(s.longitude),
  }
})

useSeoMetaTags(t('seo.about_title'), t('seo.about_description'))

onMounted(() => {
  slideIn(aboutImageRef.value, 'left')
  slideIn(aboutTextRef.value, 'left')
  slideIn(aboutSideRef.value, 'right')
  revealSection(mapSection.value)
})
</script>
