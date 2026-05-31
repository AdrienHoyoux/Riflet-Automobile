<template>
  <div class="card">
    <h3 class="font-display text-2xl leading-none text-ink">
      {{ $t('about.hours_title') }}
    </h3>
    <dl class="mt-6 space-y-0">
      <div
        v-for="day in days"
        :key="day.key"
        class="flex justify-between gap-4 border-b border-ink/10 py-3 text-sm last:border-0"
      >
        <dt class="font-bold uppercase tracking-street text-ink">{{ $t(`about.days.${day.key}`) }}</dt>
        <dd class="text-right text-smoke">{{ day.hours }}</dd>
      </div>
    </dl>
  </div>
</template>

<script setup lang="ts">
import type { SiteSettings } from '~/types/api'

const settings = inject<Ref<SiteSettings | null>>('siteSettings')

const days = computed(() => {
  const s = settings?.value
  if (!s) return []
  return [
    { key: 'monday', hours: s.monday_hours },
    { key: 'tuesday', hours: s.tuesday_hours },
    { key: 'wednesday', hours: s.wednesday_hours },
    { key: 'thursday', hours: s.thursday_hours },
    { key: 'friday', hours: s.friday_hours },
    { key: 'saturday', hours: s.saturday_hours },
    { key: 'sunday', hours: s.sunday_hours },
  ]
})
</script>
