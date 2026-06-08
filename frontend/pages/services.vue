<template>
  <div>
    <PageHero
      :title="servicesPageTitle"
      :subtitle="servicesPageSubtitle"
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
import type { SiteSettings } from '~/types/api'

const { t } = useI18n()
const settings = inject<Ref<SiteSettings | null>>('siteSettings')
const { data: services } = await useAsyncData('services', fetchServices)

const servicesPageTitle = useSettingsField(settings, 'services_title', 'services.title')
const servicesPageSubtitle = useSettingsField(settings, 'services_subtitle', 'services.subtitle')

const servicesGrid = ref<HTMLElement | null>(null)
const { staggerIn } = useGsap()

useSeoMetaTags(t('seo.services_title'), t('seo.services_description'))

onMounted(() => {
  if (servicesGrid.value) {
    staggerIn(servicesGrid.value.children, { trigger: servicesGrid.value })
  }
})
</script>
