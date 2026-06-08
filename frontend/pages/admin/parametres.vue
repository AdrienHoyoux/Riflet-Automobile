<template>
  <div>
    <AdminSectionHeader
      eyebrow="Contenu du site"
      title="Paramètres du garage"
      description="Informations générales affichées dans l'en-tête, le pied de page, la page contact et les horaires. Pour modifier les pages Accueil, À propos ou Services, utilisez les menus dédiés."
    />

    <form v-if="form" class="mt-8 space-y-8" @submit.prevent="saveSettings">
      <div class="grid items-start gap-6 xl:grid-cols-2">
        <section class="card space-y-4">
          <h2 class="font-display text-2xl">Identité & bannière d'accueil</h2>
          <p class="text-sm text-smoke">
            Nom et slogan visibles dans le bandeau principal de la page d'accueil.
          </p>

          <AdminField v-model="form.company_name" label="Nom du garage" />

          <AdminField v-model="form.tagline_fr" label="Slogan (FR)" placeholder="Garage toutes marques de confiance à Malmedy" />
          <AdminField v-model="form.tagline_de" label="Slogan (DE)" />
          <AdminField v-model="form.tagline_nl" label="Slogan (NL)" />

          <AdminImageUpload v-model="form.logo_url" label="Logo" folder="settings" url-label="URL du logo" />
          <AdminImageUpload
            v-model="form.hero_image_url"
            label="Photo de la bannière d'accueil"
            folder="settings"
            url-label="URL de l'image"
          />
        </section>

        <aside class="card xl:sticky xl:top-8">
          <AdminSettingsPreview :settings="form" section="identity" />
        </aside>
      </div>

      <div class="grid items-start gap-6 xl:grid-cols-2">
        <section class="card space-y-4">
          <h2 class="font-display text-2xl">Coordonnées</h2>
          <p class="text-sm text-smoke">Utilisées sur la page contact, le pied de page et les e-mails.</p>

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

        <aside class="card xl:sticky xl:top-8">
          <AdminSettingsPreview :settings="form" section="contact" />
        </aside>
      </div>

      <div class="grid items-start gap-6 xl:grid-cols-2">
        <section class="card space-y-4">
          <h2 class="font-display text-2xl">Horaires d'ouverture</h2>
          <p class="text-sm text-smoke">Affichés sur la page À propos et la page contact.</p>

          <AdminField v-model="form.monday_hours" label="Lundi" />
          <AdminField v-model="form.tuesday_hours" label="Mardi" />
          <AdminField v-model="form.wednesday_hours" label="Mercredi" />
          <AdminField v-model="form.thursday_hours" label="Jeudi" />
          <AdminField v-model="form.friday_hours" label="Vendredi" />
          <AdminField v-model="form.saturday_hours" label="Samedi" />
          <AdminField v-model="form.sunday_hours" label="Dimanche" />
        </section>

        <aside class="card xl:sticky xl:top-8">
          <AdminSettingsPreview :settings="form" section="hours" />
        </aside>
      </div>

      <AdminSaveBar :message="message" :error="error" :saving="saving" />
    </form>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: 'admin', middleware: 'admin-auth' })

const { form, saving, message, error, loadSettings, saveSettings } = useAdminSettingsForm()

onMounted(loadSettings)
</script>
