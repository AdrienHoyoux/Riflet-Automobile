<template>
  <div>
    <PageHero
      :title="$t('vehicles.title')"
      :subtitle="$t('vehicles.subtitle')"
      :label="$t('nav.vehicles')"
    />

    <section class="py-16 lg:py-24">
      <div class="container-custom">
        <div v-if="vehicles?.length" class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          <VehicleCard v-for="vehicle in vehicles" :key="vehicle.id" :vehicle="vehicle" />
        </div>
        <p v-else class="text-center text-smoke">{{ $t('vehicles.empty') }}</p>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
const { t } = useI18n()
const { data: vehicles } = await useAsyncData('vehicles-list', fetchVehicles)

useSeoMetaTags(t('seo.vehicles_title'), t('seo.vehicles_description'))
</script>
