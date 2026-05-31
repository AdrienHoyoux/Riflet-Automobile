<template>
  <div>
    <PageHero
      :title="$t('contact.title')"
      :subtitle="$t('contact.subtitle')"
      :label="$t('nav.contact')"
    />

    <section class="py-16 lg:py-24">
      <div class="container-custom">
        <div class="grid gap-10 lg:grid-cols-5">
          <div class="lg:col-span-3">
            <ContactForm />
          </div>

          <div class="space-y-6 lg:col-span-2">
            <div class="card">
              <h3 class="font-display text-2xl leading-none text-ink">
                {{ $t('contact.info_title') }}
              </h3>
              <ul class="mt-6 space-y-4 text-sm text-smoke">
                <li v-if="settings">
                  <span class="font-bold uppercase tracking-street text-ink">{{ settings.company_name }}</span><br>
                  {{ settings.address }}<br>
                  {{ settings.postal_code }} {{ settings.city }}
                </li>
                <li v-if="settings?.phone">
                  <span class="block text-[10px] font-bold uppercase tracking-street text-ink">{{ $t('contact.call_us') }}</span>
                  <a :href="phoneHref(settings.phone)" class="font-bold text-ink hover:underline">
                    {{ settings.phone }}
                  </a>
                </li>
                <li v-if="settings?.email">
                  <a :href="`mailto:${settings.email}`" class="hover:text-ink hover:underline">
                    {{ settings.email }}
                  </a>
                </li>
              </ul>
            </div>

            <OpeningHours />
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import type { SiteSettings } from '~/types/api'

const { t } = useI18n()
const settings = inject<Ref<SiteSettings | null>>('siteSettings')

useSeoMetaTags(t('seo.contact_title'), t('seo.contact_description'))
</script>
