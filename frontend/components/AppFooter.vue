<template>
  <footer class="border-t-2 border-ink bg-ink text-chalk">
    <div class="container-custom py-12 lg:py-16">
      <div class="grid gap-10 md:grid-cols-2 lg:grid-cols-4">
        <div class="lg:col-span-2">
          <div>
            <span class="font-display text-4xl leading-none">RIFLET</span>
            <p class="mt-1 text-[10px] font-bold uppercase tracking-street text-smoke-light">
              Automobile — Malmedy
            </p>
          </div>
          <p class="mt-6 max-w-md text-sm leading-relaxed text-smoke-light">
            {{ $t('footer.description') }}
          </p>
          <a
            v-if="settings?.facebook_url"
            :href="settings.facebook_url"
            target="_blank"
            rel="noopener noreferrer"
            class="mt-6 inline-block text-xs font-bold uppercase tracking-street text-acid hover:underline"
          >
            Facebook
          </a>
        </div>

        <div>
          <h3 class="text-xs font-bold uppercase tracking-street text-acid">
            {{ $t('footer.navigation') }}
          </h3>
          <ul class="mt-4 space-y-2">
            <li v-for="link in navLinks" :key="link.to">
              <NuxtLinkLocale
                :to="link.to"
                class="text-sm uppercase tracking-wide text-smoke-light hover:text-chalk"
              >
                {{ $t(link.label) }}
              </NuxtLinkLocale>
            </li>
          </ul>
        </div>

        <div>
          <h3 class="text-xs font-bold uppercase tracking-street text-acid">
            {{ $t('footer.contact') }}
          </h3>
          <ul class="mt-4 space-y-3 text-sm text-smoke-light">
            <li v-if="settings">
              {{ settings.address }}<br>
              {{ settings.postal_code }} {{ settings.city }}
            </li>
            <li v-if="settings?.phone">
              <a :href="phoneHref(settings.phone)" class="hover:text-chalk">
                {{ settings.phone }}
              </a>
            </li>
            <li v-if="settings?.email">
              <a :href="`mailto:${settings.email}`" class="hover:text-chalk">
                {{ settings.email }}
              </a>
            </li>
          </ul>
        </div>
      </div>

      <div class="mt-10 border-t border-ink-muted pt-6 text-center text-[10px] uppercase tracking-street text-smoke">
        © {{ new Date().getFullYear() }} {{ settings?.company_name }}.
        {{ $t('footer.rights') }}
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
import type { SiteSettings } from '~/types/api'

const settings = inject<Ref<SiteSettings | null>>('siteSettings')

const navLinks = [
  { to: '/', label: 'nav.home' },
  { to: '/services', label: 'nav.services' },
  { to: '/actualites', label: 'nav.news' },
  { to: '/a-propos', label: 'nav.about' },
  { to: '/contact', label: 'nav.contact' },
]
</script>
