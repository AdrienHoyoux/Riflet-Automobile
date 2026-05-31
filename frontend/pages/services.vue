<template>
  <div>
    <PageHero
      :title="$t('services.title')"
      :subtitle="$t('services.subtitle')"
      :label="$t('nav.services')"
    />

    <section class="py-16 lg:py-24">
      <div class="container-custom">
        <div ref="servicesGrid" class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          <ServiceCard
            v-for="service in services"
            :key="service.id"
            :service="service"
          />
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
const { t } = useI18n()
const { data: services } = await useAsyncData('services', fetchServices)

const servicesGrid = ref<HTMLElement | null>(null)
const { staggerIn } = useGsap()

useSeoMetaTags(t('seo.services_title'), t('seo.services_description'))

onMounted(() => {
  if (servicesGrid.value) {
    staggerIn(servicesGrid.value.children, { trigger: servicesGrid.value })
  }
})
</script>
