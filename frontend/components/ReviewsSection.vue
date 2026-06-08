<template>
  <section ref="sectionRef" class="border-y-2 border-ink bg-chalk-dark py-16 lg:py-24">
    <div class="container-custom">
      <div class="flex flex-wrap items-end justify-between gap-6 border-b-2 border-ink pb-6">
        <div>
          <p class="anim-label section-label">{{ $t('reviews.label') }}</p>
          <h2 class="anim-title section-title mt-2">{{ $t('reviews.title') }}</h2>
          <p class="anim-subtitle section-subtitle">{{ $t('reviews.subtitle') }}</p>
        </div>

        <div v-if="reviews.length" class="anim-cta w-full sm:w-auto sm:text-right">
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

      <div class="mt-10 grid min-w-0 gap-10 xl:grid-cols-2 xl:items-start">
        <div v-if="reviews.length" class="min-w-0 space-y-6">
          <div
            class="relative w-full min-w-0 overflow-hidden"
            @mouseenter="pauseAutoplay"
            @mouseleave="resumeAutoplay"
            @focusin="pauseAutoplay"
            @focusout="resumeAutoplay"
            @touchstart.passive="onTouchStart"
            @touchend="onTouchEnd"
          >
            <div class="overflow-hidden">
              <div
                class="flex w-full transition-transform duration-500 ease-out"
                :style="{ transform: `translateX(-${currentIndex * 100}%)` }"
              >
                <article
                  v-for="review in reviews"
                  :key="review.id"
                  class="card flex w-full min-w-full shrink-0 basis-full flex-col"
                >
                  <div class="flex flex-wrap items-start justify-between gap-3">
                    <div class="min-w-0 flex-1">
                      <p class="break-words font-bold uppercase tracking-street text-ink">{{ review.author_name }}</p>
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
                  <p class="mt-4 flex-1 break-words text-sm leading-relaxed text-smoke">
                    {{ review.content }}
                  </p>
                  <p class="mt-4 text-[10px] font-bold uppercase tracking-street text-smoke">
                    {{ sourceLabel(review.source) }}
                  </p>
                </article>
              </div>
            </div>

            <div v-if="reviews.length > 1" class="mt-4 flex items-center justify-between gap-2 sm:mt-6 sm:gap-4">
              <button
                type="button"
                class="flex h-10 w-10 shrink-0 items-center justify-center border-2 border-ink text-sm font-bold hover:bg-ink hover:text-chalk sm:h-auto sm:w-auto sm:px-4 sm:py-2"
                :aria-label="$t('reviews.carousel_prev')"
                @click="goPrev"
              >
                ←
              </button>

              <span class="shrink-0 text-xs font-bold uppercase tracking-street text-smoke sm:hidden">
                {{ currentIndex + 1 }} / {{ reviews.length }}
              </span>

              <div class="hidden max-w-full flex-1 justify-center gap-2 overflow-x-auto pb-1 sm:flex [-ms-overflow-style:none] [scrollbar-width:none] [&::-webkit-scrollbar]:hidden">
                <button
                  v-for="(_, index) in reviews"
                  :key="index"
                  type="button"
                  class="h-2.5 w-2.5 shrink-0 border-2 border-ink transition"
                  :class="index === currentIndex ? 'bg-ink' : 'bg-transparent'"
                  :aria-label="$t('reviews.carousel_go_to', { index: index + 1 })"
                  @click="goTo(index)"
                />
              </div>

              <span class="hidden shrink-0 text-xs font-bold uppercase tracking-street text-smoke sm:inline">
                {{ currentIndex + 1 }} / {{ reviews.length }}
              </span>

              <button
                type="button"
                class="flex h-10 w-10 shrink-0 items-center justify-center border-2 border-ink text-sm font-bold hover:bg-ink hover:text-chalk sm:h-auto sm:w-auto sm:px-4 sm:py-2"
                :aria-label="$t('reviews.carousel_next')"
                @click="goNext"
              >
                →
              </button>
            </div>
          </div>
        </div>

        <div v-else class="card border-dashed">
          <p class="text-sm text-smoke">{{ $t('reviews.empty') }}</p>
        </div>

        <div class="card min-w-0 space-y-5">
          <div>
            <h3 class="font-display text-2xl">{{ $t('reviews.form_title') }}</h3>
            <p class="mt-2 text-sm text-smoke">{{ $t('reviews.form_subtitle') }}</p>
          </div>

          <form class="space-y-4" novalidate @submit.prevent="handleSubmit">
            <div>
              <label for="review-name" class="mb-2 block text-[10px] font-bold uppercase tracking-street text-ink">
                {{ $t('reviews.form_name') }} *
              </label>
              <input
                id="review-name"
                v-model="form.author_name"
                type="text"
                required
                maxlength="120"
                class="input-field"
              >
            </div>

            <div>
              <span class="mb-2 block text-[10px] font-bold uppercase tracking-street text-ink">
                {{ $t('reviews.form_rating') }} *
              </span>
              <div class="flex gap-1">
                <button
                  v-for="star in 5"
                  :key="star"
                  type="button"
                  class="text-2xl leading-none transition"
                  :class="star <= form.rating ? 'text-ink' : 'text-smoke/40'"
                  :aria-label="$t('reviews.form_rating_star', { star })"
                  @click="form.rating = star"
                >
                  ★
                </button>
              </div>
            </div>

            <div>
              <label for="review-content" class="mb-2 block text-[10px] font-bold uppercase tracking-street text-ink">
                {{ $t('reviews.form_content') }} *
              </label>
              <textarea
                id="review-content"
                v-model="form.content"
                required
                rows="4"
                minlength="10"
                maxlength="2000"
                class="input-field resize-y"
              />
            </div>

            <div class="hidden" aria-hidden="true">
              <label for="review-company">Company</label>
              <input id="review-company" v-model="form.company" type="text" tabindex="-1" autocomplete="off">
            </div>

            <div v-if="successMessage" class="border-2 border-ink bg-acid px-4 py-3 text-sm font-medium text-ink">
              {{ successMessage }}
            </div>
            <div v-if="errorMessage" class="border-2 border-ink bg-ink px-4 py-3 text-sm font-medium text-chalk">
              {{ errorMessage }}
            </div>

            <button type="submit" class="btn-primary w-full sm:w-auto" :disabled="loading">
              {{ loading ? $t('reviews.form_sending') : $t('reviews.form_submit') }}
            </button>
          </form>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import type { ReviewSubmitData, SiteSettings } from '~/types/api'
import { formatApiErrors } from '~/utils/formErrors'

const props = defineProps<{
  reviews: Array<{
    id: number
    author_name: string
    rating: number
    content: string
    source: string
    review_date: string | null
  }>
}>()

const settings = inject<Ref<SiteSettings | null>>('siteSettings')
const { locale, t } = useI18n()
const sectionRef = ref<HTMLElement | null>(null)
const { revealSection } = useGsap()

const reviewCountForCarousel = computed(() => props.reviews.length)

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
} = useCarousel(reviewCountForCarousel, 6000)

const loading = ref(false)
const successMessage = ref('')
const errorMessage = ref('')

const form = reactive<ReviewSubmitData>({
  author_name: '',
  rating: 5,
  content: '',
  company: '',
})

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

function sourceLabel(source: string) {
  if (source === 'website') return t('reviews.source_website')
  if (source === 'manual') return t('reviews.source_manual')
  if (source === 'facebook') return t('reviews.source_facebook')
  return t('reviews.source')
}

function validateForm(): string | null {
  if (!form.author_name.trim() || form.author_name.trim().length < 2) {
    return t('reviews.form_name_required')
  }
  if (form.content.trim().length < 10) {
    return t('reviews.form_content_too_short')
  }
  return null
}

function getSubmitErrorMessage(err: unknown): string {
  const fetchErr = err as { message?: string; statusCode?: number; data?: unknown }
  const fromBody = formatApiErrors(fetchErr.data)
  if (fromBody) return fromBody
  if (typeof fetchErr.message === 'string' && fetchErr.message.trim()) {
    return fetchErr.message
  }
  return t('reviews.form_error')
}

async function handleSubmit() {
  loading.value = true
  successMessage.value = ''
  errorMessage.value = ''

  const validationError = validateForm()
  if (validationError) {
    errorMessage.value = validationError
    loading.value = false
    return
  }

  try {
    const result = await submitReview({
      author_name: form.author_name.trim(),
      rating: form.rating,
      content: form.content.trim(),
      company: form.company,
    })
    successMessage.value = result.detail || t('reviews.form_success')
    form.author_name = ''
    form.rating = 5
    form.content = ''
    form.company = ''
  } catch (err: unknown) {
    errorMessage.value = getSubmitErrorMessage(err)
  } finally {
    loading.value = false
  }
}

watch(
  () => props.reviews.length,
  () => {
    startAutoplay()
  },
)

onMounted(() => {
  revealSection(sectionRef.value)
  startAutoplay()
})
</script>
