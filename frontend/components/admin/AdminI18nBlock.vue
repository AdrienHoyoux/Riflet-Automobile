<template>
  <section :class="plain ? 'space-y-4' : 'card space-y-4'">
    <div>
      <h2 class="font-display text-2xl">{{ title }}</h2>
      <p v-if="help" class="mt-2 text-sm leading-relaxed text-smoke">{{ help }}</p>
    </div>

    <div class="flex flex-wrap gap-2">
      <button
        v-for="loc in locales"
        :key="loc"
        type="button"
        class="border-2 border-ink px-3 py-1.5 text-[10px] font-bold uppercase tracking-street"
        :class="activeLocale === loc ? 'bg-ink text-chalk' : 'bg-chalk text-ink'"
        @click="activeLocale = loc"
      >
        {{ loc }}
      </button>
    </div>

    <AdminField
      v-if="titlePrefix"
      :model-value="readField(titlePrefix)"
      :label="`Titre (${activeLocale.toUpperCase()})`"
      :placeholder="titlePlaceholder"
      @update:model-value="writeField(titlePrefix, $event)"
    />

    <AdminField
      v-if="subtitlePrefix"
      :model-value="readField(subtitlePrefix)"
      :label="`Sous-titre (${activeLocale.toUpperCase()})`"
      type="textarea"
      :placeholder="subtitlePlaceholder"
      @update:model-value="writeField(subtitlePrefix, $event)"
    />

    <AdminField
      v-if="bodyPrefix"
      :model-value="readField(bodyPrefix)"
      :label="`Texte (${activeLocale.toUpperCase()})`"
      type="textarea"
      :placeholder="bodyPlaceholder"
      @update:model-value="writeField(bodyPrefix, $event)"
    />

    <p class="rounded border border-ink/20 bg-chalk-dark px-3 py-2 text-xs leading-relaxed text-smoke">
      <span class="font-bold uppercase tracking-street text-ink">Affiché sur le site :</span>
      {{ livePreview }}
    </p>
  </section>
</template>

<script setup lang="ts">
import type { SiteSettings } from '~/types/api'
import { adminFieldValue, pickLocaleText, type AdminLocale } from '~/utils/adminDefaults'

const props = defineProps<{
  form: SiteSettings
  title: string
  help?: string
  plain?: boolean
  titlePrefix?: string
  subtitlePrefix?: string
  bodyPrefix?: string
  defaults: {
    title?: Record<AdminLocale, string>
    subtitle?: Record<AdminLocale, string>
    body?: Record<AdminLocale, string>
  }
}>()

const locales: AdminLocale[] = ['fr', 'de', 'nl']
const activeLocale = ref<AdminLocale>('fr')

function fieldKey(prefix: string) {
  return `${prefix}_${activeLocale.value}` as keyof SiteSettings
}

function readField(prefix: string) {
  return String(props.form[fieldKey(prefix)] || '')
}

function writeField(prefix: string, value: string) {
  ;(props.form as Record<string, string>)[fieldKey(prefix)] = value
}

const titlePlaceholder = computed(() =>
  props.defaults.title ? pickLocaleText(props.defaults.title, activeLocale.value) : '',
)

const subtitlePlaceholder = computed(() =>
  props.defaults.subtitle ? pickLocaleText(props.defaults.subtitle, activeLocale.value) : '',
)

const bodyPlaceholder = computed(() =>
  props.defaults.body ? pickLocaleText(props.defaults.body, activeLocale.value) : '',
)

const livePreview = computed(() => {
  const parts: string[] = []
  if (props.titlePrefix && props.defaults.title) {
    parts.push(adminFieldValue(readField(props.titlePrefix), pickLocaleText(props.defaults.title, activeLocale.value)))
  }
  if (props.subtitlePrefix && props.defaults.subtitle) {
    parts.push(adminFieldValue(readField(props.subtitlePrefix), pickLocaleText(props.defaults.subtitle, activeLocale.value)))
  }
  if (props.bodyPrefix && props.defaults.body) {
    const body = adminFieldValue(readField(props.bodyPrefix), pickLocaleText(props.defaults.body, activeLocale.value))
    parts.push(body.length > 120 ? `${body.slice(0, 120)}…` : body)
  }
  return parts.join(' — ') || '—'
})
</script>
