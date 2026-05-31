<template>
  <section ref="sectionRef" class="border-y-2 border-ink bg-chalk-dark py-16 lg:py-24">
    <div class="container-custom">
      <div class="flex flex-wrap items-end justify-between gap-6 border-b-2 border-ink pb-6">
        <div>
          <p class="anim-label section-label">{{ $t('reviews.label') }}</p>
          <h2 class="anim-title section-title mt-2">{{ $t('reviews.title') }}</h2>
          <p class="anim-subtitle section-subtitle">{{ $t('reviews.subtitle') }}</p>
        </div>

        <div class="anim-cta text-right">
          <div class="flex items-center gap-3">
            <span class="font-display text-5xl leading-none text-ink">{{ ratingDisplay }}</span>
            <div>
              <div class="flex gap-0.5">
                <span
                  v-for="star in 5"
                  :key="star"
                  class="text-xl leading-none"
                  :class="star <= Math.round(Number(ratingDisplay)) ? 'text-ink' : 'text-smoke/40'"
                >
                  ★
                </span>
              </div>
              <p class="mt-1 text-xs uppercase tracking-street text-smoke">
                {{ $t('reviews.based_on', { count: reviewCount }) }}
              </p>
            </div>
          </div>
          <a
            v-if="googleMapsUrl"
            :href="googleMapsUrl"
            target="_blank"
            rel="noopener noreferrer"
            class="mt-4 inline-block text-xs font-bold uppercase tracking-street text-ink underline-offset-4 hover:underline"
          >
            {{ $t('reviews.view_on_google') }}
          </a>
        </div>
      </div>

      <div ref="reviewsGrid" class="mt-10 grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        <article
          v-for="review in reviews"
          :key="review.id"
          class="card flex h-full flex-col"
        >
          <div class="flex items-center justify-between gap-4">
            <div>
              <p class="font-bold uppercase tracking-street text-ink">{{ review.author_name }}</p>
              <p v-if="review.review_date" class="mt-1 text-[10px] uppercase tracking-street text-smoke">
                {{ formatReviewDate(review.review_date) }}
              </p>
            </div>
            <div class="flex shrink-0 gap-0.5">
              <span
                v-for="star in 5"
                :key="star"
                class="text-base leading-none"
                :class="star <= review.rating ? 'text-ink' : 'text-smoke/40'"
              >
                ★
              </span>
            </div>
          </div>
          <p class="mt-4 flex-1 text-sm leading-relaxed text-smoke">
            {{ review.content }}
          </p>
          <p class="mt-4 text-[10px] font-bold uppercase tracking-street text-smoke">
            {{ $t('reviews.source') }}
          </p>
        </article>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import type { SiteSettings } from '~/types/api'

const props = defineProps<{
  reviews: Array<{
    id: number
    author_name: string
    rating: number
    content: string
    review_date: string | null
  }>
}>()

const settings = inject<Ref<SiteSettings | null>>('siteSettings')
const { locale, t } = useI18n()
const sectionRef = ref<HTMLElement | null>(null)
const reviewsGrid = ref<HTMLElement | null>(null)
const { revealSection, staggerIn } = useGsap()

const ratingDisplay = computed(() => {
  const rating = settings?.value?.google_rating
  return rating ? Number(rating).toFixed(1) : '5.0'
})

const reviewCount = computed(() => settings?.value?.google_review_count || props.reviews.length)

const googleMapsUrl = computed(() => settings?.value?.google_maps_url || '')

function formatReviewDate(dateString: string) {
  return new Date(dateString).toLocaleDateString(
    locale.value === 'fr' ? 'fr-BE' : locale.value === 'de' ? 'de-BE' : 'nl-BE',
    { month: 'long', year: 'numeric' },
  )
}

onMounted(() => {
  revealSection(sectionRef.value)
  if (reviewsGrid.value) {
    staggerIn(reviewsGrid.value.children, { trigger: reviewsGrid.value })
  }
})
</script>
