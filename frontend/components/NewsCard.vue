<template>
  <article ref="cardRef" class="card group overflow-hidden !p-0">
    <NuxtLinkLocale :to="`/actualites/${article.slug}`" class="block">
      <div class="aspect-[16/10] overflow-hidden bg-ink-soft">
        <img
          :src="imageSrc"
          :alt="title"
          class="h-full w-full object-cover grayscale transition duration-700 group-hover:scale-105 group-hover:grayscale-0"
        >
      </div>
      <div class="border-t-2 border-ink p-6">
        <time class="text-[10px] font-bold uppercase tracking-street text-smoke">
          {{ formattedDate }}
        </time>
        <h3 class="mt-3 font-display text-2xl leading-none text-ink group-hover:text-ink/80">
          {{ title }}
        </h3>
        <p class="mt-3 line-clamp-2 text-sm leading-relaxed text-smoke">
          {{ description }}
        </p>
        <span class="mt-5 inline-block text-[10px] font-bold uppercase tracking-street text-ink underline-offset-4 group-hover:underline">
          {{ $t('home.read_more') }}
        </span>
      </div>
    </NuxtLinkLocale>
  </article>
</template>

<script setup lang="ts">
import type { NewsArticle } from '~/types/api'
import { getNewsFallback } from '~/utils/images'

const props = defineProps<{
  article: NewsArticle
  index?: number
}>()

const { locale } = useI18n()
const cardRef = ref<HTMLElement | null>(null)
const { fadeInUp } = useGsap()

const title = computed(() => useLocalizedField(props.article, 'title'))
const description = computed(() => useLocalizedField(props.article, 'description'))
const formattedDate = computed(() => formatDate(props.article.published_at, locale.value))
const imageSrc = computed(() =>
  props.article.image || getNewsFallback(props.index ?? props.article.id),
)

onMounted(() => {
  fadeInUp(cardRef.value)
})
</script>
