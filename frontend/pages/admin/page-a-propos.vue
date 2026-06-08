<template>
  <div>
    <AdminSectionHeader
      eyebrow="Contenu du site"
      title="Page À propos"
      description="Contenu complet de la page /a-propos : en-tête, photo et texte de présentation du garage."
      page-url="/a-propos"
    />

    <form v-if="form" class="mt-8 space-y-8" @submit.prevent="saveSettings">
      <AdminI18nBlock
        :form="form"
        title="En-tête de la page"
        help="Grand titre et sous-titre en haut de la page À propos."
        title-prefix="about_title"
        subtitle-prefix="about_subtitle"
        :defaults="ADMIN_DEFAULTS.aboutPage"
      />

      <section class="card space-y-4">
        <h2 class="font-display text-2xl">Photo principale</h2>
        <p class="text-sm text-smoke">Image affichée à gauche du texte de présentation.</p>
        <AdminImageUpload
          v-model="form.about_image_url"
          label="Photo de la page À propos"
          folder="settings"
          url-label="URL de l'image"
        />
      </section>

      <AdminI18nBlock
        :form="form"
        title="Texte de présentation"
        help="Paragraphe descriptif du garage, sous la photo sur la page À propos."
        body-prefix="about"
        :defaults="{
          body: {
            fr: 'Riflet Automobile est un garage automobile toutes marques…',
            de: 'Riflet Automobile ist eine markenunabhängige Autowerkstatt…',
            nl: 'Riflet Automobile is een autogarage alle merken…',
          },
        }"
      />

      <AdminSaveBar :message="message" :error="error" :saving="saving" />
    </form>
  </div>
</template>

<script setup lang="ts">
import { ADMIN_DEFAULTS } from '~/utils/adminDefaults'

definePageMeta({ layout: 'admin', middleware: 'admin-auth' })

const { form, saving, message, error, loadSettings, saveSettings } = useAdminSettingsForm()

onMounted(loadSettings)
</script>
