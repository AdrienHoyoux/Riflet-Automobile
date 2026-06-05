<template>

  <div>

    <h1 class="font-display text-4xl">Paramètres du site</h1>

    <p class="mt-2 text-sm text-smoke">Modifiez les textes, horaires et images affichés sur le site.</p>



    <form v-if="form" class="mt-8 space-y-8" @submit.prevent="save">

      <section class="card space-y-4">

        <h2 class="font-display text-2xl">Identité</h2>

        <AdminField v-model="form.company_name" label="Nom du garage" />

        <AdminField v-model="form.tagline_fr" label="Slogan (FR)" />

        <AdminField v-model="form.tagline_de" label="Slogan (DE)" />

        <AdminField v-model="form.tagline_nl" label="Slogan (NL)" />

        <AdminField v-model="form.about_fr" label="À propos (FR)" type="textarea" />

        <AdminField v-model="form.about_de" label="À propos (DE)" type="textarea" />

        <AdminField v-model="form.about_nl" label="À propos (NL)" type="textarea" />

        <AdminImageUpload v-model="form.logo_url" label="Logo" folder="settings" url-label="URL du logo" />

        <AdminImageUpload v-model="form.hero_image_url" label="Image d'accueil (hero)" folder="settings" url-label="URL image hero" />

      </section>



      <section class="card space-y-4">

        <h2 class="font-display text-2xl">Coordonnées</h2>

        <AdminField v-model="form.address" label="Adresse" />

        <div class="grid gap-4 sm:grid-cols-3">

          <AdminField v-model="form.postal_code" label="Code postal" />

          <AdminField v-model="form.city" label="Ville" />

          <AdminField v-model="form.country" label="Pays" />

        </div>

        <AdminField v-model="form.phone" label="Téléphone" />

        <AdminField v-model="form.email" label="E-mail" type="email" />

        <AdminField v-model="form.facebook_url" label="Facebook" type="url" />

      </section>



      <section class="card space-y-4">

        <h2 class="font-display text-2xl">Horaires</h2>

        <AdminField v-model="form.monday_hours" label="Lundi" />

        <AdminField v-model="form.tuesday_hours" label="Mardi" />

        <AdminField v-model="form.wednesday_hours" label="Mercredi" />

        <AdminField v-model="form.thursday_hours" label="Jeudi" />

        <AdminField v-model="form.friday_hours" label="Vendredi" />

        <AdminField v-model="form.saturday_hours" label="Samedi" />

        <AdminField v-model="form.sunday_hours" label="Dimanche" />

      </section>



      <p v-if="message" class="text-sm font-bold text-green-700">{{ message }}</p>

      <p v-if="error" class="text-sm font-bold text-red-600">{{ error }}</p>



      <button type="submit" class="btn-primary" :disabled="saving">

        {{ saving ? 'Enregistrement...' : 'Enregistrer' }}

      </button>

    </form>

  </div>

</template>



<script setup lang="ts">

import type { SiteSettings } from '~/types/api'
import { formatAdminError, normalizeImageUrlForStorage } from '~/composables/useAssetUrl'



definePageMeta({ layout: 'admin', middleware: 'admin-auth' })



const form = ref<SiteSettings | null>(null)

const saving = ref(false)

const message = ref('')

const error = ref('')



onMounted(async () => {

  form.value = await adminFetch<SiteSettings>('settings/')

})



async function save() {

  if (!form.value) return

  saving.value = true

  message.value = ''

  error.value = ''

  try {

    form.value = await adminFetch<SiteSettings>('settings/', {

      method: 'PATCH',

      body: {
        ...form.value,
        logo_url: normalizeImageUrlForStorage(form.value.logo_url),
        hero_image_url: normalizeImageUrlForStorage(form.value.hero_image_url),
      },

    })

    message.value = 'Paramètres enregistrés.'

  } catch (err) {

    error.value = formatAdminError(err)

  } finally {

    saving.value = false

  }

}

</script>


