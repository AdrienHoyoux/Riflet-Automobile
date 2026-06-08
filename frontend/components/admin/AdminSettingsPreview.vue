<template>
  <div class="h-full">
    <p class="text-xs font-bold uppercase tracking-street text-smoke">Aperçu sur le site</p>

    <!-- Identité -->
    <template v-if="section === 'identity'">
      <div class="mt-3 flex gap-1">
        <button
          v-for="loc in locales"
          :key="loc"
          type="button"
          class="border-2 border-ink px-2 py-1 text-[10px] font-bold uppercase"
          :class="previewLocale === loc ? 'bg-ink text-chalk' : 'bg-chalk text-ink'"
          @click="previewLocale = loc"
        >
          {{ loc }}
        </button>
      </div>

      <div class="mt-4 space-y-4 pointer-events-none">
        <div class="overflow-hidden border-2 border-ink">
          <p class="bg-ink px-3 py-1 text-[10px] font-bold uppercase tracking-street text-chalk">
            En-tête
          </p>
          <div class="flex items-center gap-3 bg-chalk/95 px-3 py-3">
            <img :src="logoUrl" :alt="settings.company_name" class="h-12 w-12 shrink-0 object-contain">
            <div class="min-w-0">
              <span class="font-display text-lg leading-none text-ink">RIFLET</span>
              <span class="mt-0.5 block text-[9px] font-bold uppercase tracking-street text-smoke">
                Automobile — Malmedy
              </span>
            </div>
          </div>
        </div>

        <div class="overflow-hidden border-2 border-ink">
          <p class="bg-ink px-3 py-1 text-[10px] font-bold uppercase tracking-street text-chalk">
            Bannière d'accueil
          </p>
          <div class="relative min-h-[160px] bg-ink">
            <img :src="heroImage" alt="" class="absolute inset-0 h-full w-full object-cover object-[center_40%] brightness-110">
            <div class="absolute inset-0 bg-gradient-to-r from-ink/95 via-ink/60 to-ink/20" />
            <div class="relative px-4 py-6">
              <h3 class="font-display text-2xl leading-none text-chalk">
                {{ settings.company_name || 'Nom du garage' }}
              </h3>
              <p class="mt-2 text-xs leading-relaxed text-smoke-light">
                {{ tagline || 'Slogan du garage…' }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </template>

    <!-- Coordonnées -->
    <template v-else-if="section === 'contact'">
      <div class="mt-4 space-y-4 pointer-events-none">
        <div class="overflow-hidden border-2 border-ink">
          <p class="bg-ink px-3 py-1 text-[10px] font-bold uppercase tracking-street text-chalk">
            En-tête — bouton téléphone
          </p>
          <div class="flex justify-end bg-chalk px-3 py-3">
            <span
              v-if="settings.phone"
              class="bg-ink px-3 py-1.5 text-[10px] font-bold uppercase text-chalk"
            >
              {{ settings.phone }}
            </span>
            <span v-else class="text-xs text-smoke">Aucun téléphone</span>
          </div>
        </div>

        <div class="overflow-hidden border-2 border-ink">
          <p class="bg-ink px-3 py-1 text-[10px] font-bold uppercase tracking-street text-chalk">
            Page Contact
          </p>
          <div class="card !m-3 !p-3">
            <p class="text-[10px] font-bold uppercase tracking-street text-ink">Coordonnées</p>
            <ul class="mt-2 space-y-2 text-xs text-smoke">
              <li>
                <span class="font-bold text-ink">{{ settings.company_name }}</span><br>
                {{ settings.address || '—' }}<br>
                {{ settings.postal_code }} {{ settings.city }}
              </li>
              <li v-if="settings.phone" class="font-bold text-ink">{{ settings.phone }}</li>
              <li v-if="settings.email">{{ settings.email }}</li>
            </ul>
          </div>
        </div>

        <div class="overflow-hidden border-2 border-ink">
          <p class="bg-ink px-3 py-1 text-[10px] font-bold uppercase tracking-street text-chalk">
            Pied de page
          </p>
          <div class="space-y-3 bg-ink p-3 text-chalk">
            <ul class="space-y-2 text-xs text-smoke-light">
              <li>
                {{ settings.address }}<br>
                {{ settings.postal_code }} {{ settings.city }}
              </li>
              <li v-if="settings.phone">{{ settings.phone }}</li>
              <li v-if="settings.email">{{ settings.email }}</li>
            </ul>
            <a v-if="settings.facebook_url" :href="settings.facebook_url" class="text-[10px] font-bold uppercase text-acid">
              Facebook
            </a>
            <p class="text-[10px] uppercase tracking-street text-smoke">
              © {{ new Date().getFullYear() }} {{ settings.company_name }}
            </p>
          </div>
        </div>

        <div class="overflow-hidden border-2 border-ink">
          <p class="bg-ink px-3 py-1 text-[10px] font-bold uppercase tracking-street text-chalk">
            À propos — localisation
          </p>
          <div class="card !m-3 !p-3">
            <address class="not-italic text-xs leading-relaxed text-smoke">
              <strong class="text-ink">{{ settings.company_name }}</strong><br>
              {{ settings.address || '—' }}<br>
              {{ settings.postal_code }} {{ settings.city }}<br>
              {{ settings.country }}
            </address>
          </div>
        </div>
      </div>
    </template>

    <!-- Horaires -->
    <template v-else-if="section === 'hours'">
      <div class="mt-4 pointer-events-none">
        <div class="overflow-hidden border-2 border-ink">
          <p class="bg-ink px-3 py-1 text-[10px] font-bold uppercase tracking-street text-chalk">
            Pages Contact & À propos
          </p>
          <div class="bg-chalk p-2">
            <OpeningHours />
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import type { SiteSettings } from '~/types/api'
import { resolveImageUrl } from '~/composables/useAssetUrl'
import { LOGO_URL, VOLVO_IMAGES } from '~/utils/images'

const props = defineProps<{
  settings: SiteSettings
  section: 'identity' | 'contact' | 'hours'
}>()

const locales = ['fr', 'de', 'nl'] as const
const previewLocale = ref<(typeof locales)[number]>('fr')

const settingsRef = computed(() => props.settings)
provide('siteSettings', settingsRef)

const logoUrl = computed(() =>
  resolveImageUrl(props.settings.logo_url) || LOGO_URL,
)

const heroImage = computed(() =>
  resolveImageUrl(props.settings.hero_image_url) || VOLVO_IMAGES.hero,
)

const tagline = computed(() => localizedField('tagline'))
const aboutText = computed(() => localizedField('about'))

function localizedField(field: 'tagline' | 'about') {
  const key = `${field}_${previewLocale.value}` as keyof SiteSettings
  const fallback = `${field}_fr` as keyof SiteSettings
  const value = props.settings[key] || props.settings[fallback]
  return typeof value === 'string' ? value : ''
}
</script>
