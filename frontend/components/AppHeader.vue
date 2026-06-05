<template>
  <header class="sticky top-0 z-50 border-b-2 border-ink bg-chalk/95 backdrop-blur-sm">
    <div class="container-custom">
      <div class="flex h-[4.5rem] items-center justify-between lg:h-20">
        <NuxtLinkLocale to="/" class="group flex items-center gap-4">
          <img
            :src="logoUrl"
            :alt="settings?.company_name || 'Riflet Automobile'"
            referrerpolicy="no-referrer"
            class="h-14 w-14 shrink-0 object-contain sm:h-16 sm:w-16 lg:h-[4.5rem] lg:w-[4.5rem]"
          >
          <div>
            <span class="font-display text-2xl leading-none text-ink lg:text-3xl">
              RIFLET
            </span>
            <span class="mt-0.5 block text-[10px] font-bold uppercase tracking-street text-smoke">
              Automobile — Malmedy
            </span>
          </div>
        </NuxtLinkLocale>

        <nav class="hidden items-center gap-1 lg:flex">
          <NuxtLinkLocale
            v-for="link in navLinks"
            :key="link.to"
            :to="link.to"
            class="px-4 py-2 text-xs font-bold uppercase tracking-street text-ink transition hover:bg-acid"
            active-class="!bg-ink !text-chalk"
          >
            {{ $t(link.label) }}
          </NuxtLinkLocale>
        </nav>

        <div class="flex items-center gap-3">
          <LanguageSwitcher />
          <a
            v-if="settings?.phone"
            :href="phoneHref(settings.phone)"
            class="hidden btn-primary !px-4 !py-2 lg:inline-flex"
          >
            {{ settings.phone }}
          </a>
          <button
            type="button"
            class="border-2 border-ink px-3 py-2 text-[10px] font-bold uppercase tracking-street lg:hidden"
            @click="mobileOpen = !mobileOpen"
          >
            {{ mobileOpen ? 'Close' : 'Menu' }}
          </button>
        </div>
      </div>

      <nav
        v-show="mobileOpen"
        class="border-t-2 border-ink py-4 lg:hidden"
      >
        <NuxtLinkLocale
          v-for="link in navLinks"
          :key="link.to"
          :to="link.to"
          class="block px-2 py-3 text-xs font-bold uppercase tracking-street hover:bg-acid"
          @click="mobileOpen = false"
        >
          {{ $t(link.label) }}
        </NuxtLinkLocale>
        <a
          v-if="settings?.phone"
          :href="phoneHref(settings.phone)"
          class="mt-2 block px-2 py-3 text-xs font-bold uppercase tracking-street text-ink"
        >
          {{ settings.phone }}
        </a>
      </nav>
    </div>
  </header>
</template>

<script setup lang="ts">
import type { SiteSettings } from '~/types/api'

const settings = inject<Ref<SiteSettings | null>>('siteSettings')
const logoUrl = useLogoUrl(settings)
const mobileOpen = ref(false)

const navLinks = [
  { to: '/', label: 'nav.home' },
  { to: '/services', label: 'nav.services' },
  { to: '/vehicules', label: 'nav.vehicles' },
  { to: '/actualites', label: 'nav.news' },
  { to: '/a-propos', label: 'nav.about' },
  { to: '/contact', label: 'nav.contact' },
]
</script>
