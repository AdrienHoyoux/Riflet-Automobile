<template>
  <div v-if="article">
    <section class="page-hero">
      <div class="container-custom">
        <NuxtLinkLocale
          to="/actualites"
          class="text-[10px] font-bold uppercase tracking-street text-acid hover:underline"
        >
          {{ $t('news.back') }}
        </NuxtLinkLocale>
        <time class="mt-6 block text-[10px] font-bold uppercase tracking-street text-smoke-light">
          {{ $t('news.published') }} {{ formattedDate }}
        </time>
        <h1 class="mt-4 font-display text-5xl leading-none sm:text-6xl">
          {{ title }}
        </h1>
      </div>
    </section>

    <article class="py-16 lg:py-24">
      <div class="container-custom">
        <div class="mx-auto max-w-3xl">
          <img
            :src="imageSrc"
            :alt="title"
            class="mb-10 aspect-[16/10] w-full object-cover"
          >
          <div class="whitespace-pre-line text-base leading-relaxed text-smoke sm:text-lg">
            {{ content }}
          </div>
        </div>
      </div>
    </article>
  </div>
</template>

<script setup lang="ts">
import { resolveImageUrl } from '~/composables/useAssetUrl'
import { getNewsFallback } from '~/utils/images'

const route = useRoute()
const { locale } = useI18n()
const slug = route.params.slug as string

const { data: article } = await useAsyncData(
  `news-${slug}`,
  () => fetchNewsArticle(slug),
)

if (!article.value) {
  throw createError({ statusCode: 404, statusMessage: 'Article not found' })
}

const title = computed(() => useLocalizedField(article.value!, 'title'))
const content = computed(() => useLocalizedField(article.value!, 'content'))
const formattedDate = computed(() =>
  formatDate(article.value!.published_at, locale.value),
)
const imageSrc = computed(() =>
  resolveImageUrl(article.value?.image) || getNewsFallback(article.value!.id),
)

useSeoMetaTags(
  title.value,
  useLocalizedField(article.value!, 'description'),
  imageSrc.value,
)
</script>
