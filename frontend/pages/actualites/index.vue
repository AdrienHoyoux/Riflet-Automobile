<template>
  <div>
    <PageHero
      :title="$t('news.title')"
      :subtitle="$t('news.subtitle')"
      :label="$t('nav.news')"
    />

    <section class="py-16 lg:py-24">
      <div class="container-custom">
        <div ref="newsGrid" class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          <NewsCard
            v-for="(article, index) in news"
            :key="article.id"
            :article="article"
            :index="index"
          />
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
const { t } = useI18n()
const { data: news } = await useAsyncData('news-list', fetchNews)

const newsGrid = ref<HTMLElement | null>(null)
const { staggerIn } = useGsap()

useSeoMetaTags(t('seo.news_title'), t('seo.news_description'))

onMounted(() => {
  if (newsGrid.value) {
    staggerIn(newsGrid.value.children, { trigger: newsGrid.value })
  }
})
</script>
