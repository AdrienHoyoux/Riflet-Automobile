<template>
  <div>
    <h1 class="font-display text-4xl">Paramètres du site</h1>
    <p class="mt-2 text-sm text-smoke">
      Chaque section affiche son aperçu à côté des champs d'édition.
    </p>

    <form v-if="form" class="mt-8 space-y-8" @submit.prevent="save">
      <div class="grid items-start gap-6 xl:grid-cols-2">
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
          <AdminImageUpload
            v-model="form.hero_image_url"
            label="Image d'accueil (hero)"
            folder="settings"
            url-label="URL image hero"
          />
        </section>

        <aside class="card xl:sticky xl:top-8">
          <AdminSettingsPreview :settings="form" section="identity" />
        </aside>
      </div>

      <div class="grid items-start gap-6 xl:grid-cols-2">
        <section class="card space-y-4">
          <h2 class="font-display text-2xl">Page À propos</h2>
          <AdminField v-model="form.about_title_fr" label="Titre (FR)" />
          <AdminField v-model="form.about_title_de" label="Titre (DE)" />
          <AdminField v-model="form.about_title_nl" label="Titre (NL)" />
          <AdminField v-model="form.about_subtitle_fr" label="Sous-titre (FR)" type="textarea" />
          <AdminField v-model="form.about_subtitle_de" label="Sous-titre (DE)" type="textarea" />
          <AdminField v-model="form.about_subtitle_nl" label="Sous-titre (NL)" type="textarea" />
          <AdminImageUpload
            v-model="form.about_image_url"
            label="Image de la page À propos"
            folder="settings"
            url-label="URL image À propos"
          />
        </section>

        <aside class="card xl:sticky xl:top-8">
          <p class="text-xs font-bold uppercase tracking-street text-smoke">Aperçu</p>
          <h3 class="mt-3 font-display text-3xl">{{ form.about_title_fr || 'À propos' }}</h3>
          <p class="mt-3 text-sm text-smoke">{{ form.about_subtitle_fr || 'Sous-titre…' }}</p>
        </aside>
      </div>

      <div class="grid items-start gap-6 xl:grid-cols-2">
        <section class="card space-y-4">
          <h2 class="font-display text-2xl">Accueil — section Services</h2>
          <AdminField v-model="form.home_services_title_fr" label="Titre (FR)" />
          <AdminField v-model="form.home_services_title_de" label="Titre (DE)" />
          <AdminField v-model="form.home_services_title_nl" label="Titre (NL)" />
          <AdminField v-model="form.home_services_subtitle_fr" label="Sous-titre (FR)" type="textarea" />
          <AdminField v-model="form.home_services_subtitle_de" label="Sous-titre (DE)" type="textarea" />
          <AdminField v-model="form.home_services_subtitle_nl" label="Sous-titre (NL)" type="textarea" />
        </section>

        <section class="card space-y-4">
          <h2 class="font-display text-2xl">Page Services</h2>
          <AdminField v-model="form.services_title_fr" label="Titre (FR)" />
          <AdminField v-model="form.services_title_de" label="Titre (DE)" />
          <AdminField v-model="form.services_title_nl" label="Titre (NL)" />
          <AdminField v-model="form.services_subtitle_fr" label="Sous-titre (FR)" type="textarea" />
          <AdminField v-model="form.services_subtitle_de" label="Sous-titre (DE)" type="textarea" />
          <AdminField v-model="form.services_subtitle_nl" label="Sous-titre (NL)" type="textarea" />
        </section>
      </div>

      <section class="card space-y-6">
        <div>
          <h2 class="font-display text-2xl">Pourquoi nous choisir ?</h2>
          <p class="mt-2 text-sm text-smoke">Arguments affichés sur la page d'accueil (3 colonnes).</p>
        </div>

        <AdminField v-model="form.home_why_title_fr" label="Titre de la section (FR)" />
        <AdminField v-model="form.home_why_title_de" label="Titre de la section (DE)" />
        <AdminField v-model="form.home_why_title_nl" label="Titre de la section (NL)" />

        <div v-if="editingWhy" class="space-y-4 border-2 border-ink bg-chalk-dark p-4">
          <h3 class="font-display text-xl">{{ editingWhy.id ? 'Modifier' : 'Ajouter' }} un argument</h3>
          <AdminField v-model="editingWhy.text_fr" label="Texte (FR)" type="textarea" />
          <AdminField v-model="editingWhy.text_de" label="Texte (DE)" type="textarea" />
          <AdminField v-model="editingWhy.text_nl" label="Texte (NL)" type="textarea" />
          <AdminField v-model="editingWhy.order" label="Ordre" type="number" />
          <label class="flex items-center gap-2 text-sm">
            <input v-model="editingWhy.is_active" type="checkbox">
            Visible sur le site
          </label>
          <p v-if="whyError" class="text-sm font-bold text-red-600">{{ whyError }}</p>
          <div class="flex gap-3">
            <button type="button" class="btn-primary" :disabled="whySaving" @click="saveWhyItem">
              {{ whySaving ? 'Enregistrement...' : (editingWhy.id ? 'Mettre à jour' : 'Ajouter') }}
            </button>
            <button type="button" class="border-2 border-ink px-4 py-2 text-xs font-bold uppercase" @click="editingWhy = null">
              Annuler
            </button>
          </div>
        </div>

        <button v-else type="button" class="btn-secondary" @click="startWhyCreate">Ajouter un argument</button>

        <ul class="space-y-3">
          <li
            v-for="item in whyItems"
            :key="item.id"
            class="flex flex-wrap items-center justify-between gap-4 border-2 border-ink p-4"
          >
            <div>
              <p class="font-medium">{{ item.text_fr }}</p>
              <p class="text-xs text-smoke">Ordre {{ item.order }} — {{ item.is_active ? 'Visible' : 'Masqué' }}</p>
            </div>
            <div class="flex gap-2">
              <button type="button" class="border-2 border-ink px-3 py-1 text-xs font-bold uppercase" @click="editWhyItem(item)">
                Modifier
              </button>
              <button type="button" class="border-2 border-red-600 px-3 py-1 text-xs font-bold uppercase text-red-600" @click="removeWhyItem(item.id)">
                Supprimer
              </button>
            </div>
          </li>
        </ul>
      </section>

      <div class="grid items-start gap-6 xl:grid-cols-2">
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

        <aside class="card xl:sticky xl:top-8">
          <AdminSettingsPreview :settings="form" section="contact" />
        </aside>
      </div>

      <div class="grid items-start gap-6 xl:grid-cols-2">
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

        <aside class="card xl:sticky xl:top-8">
          <AdminSettingsPreview :settings="form" section="hours" />
        </aside>
      </div>

      <p v-if="message" class="text-sm font-bold text-green-700">{{ message }}</p>
      <p v-if="error" class="text-sm font-bold text-red-600">{{ error }}</p>

      <button type="submit" class="btn-primary" :disabled="saving">
        {{ saving ? 'Enregistrement...' : 'Enregistrer' }}
      </button>
    </form>
  </div>
</template>

<script setup lang="ts">
import type { SiteSettings, WhyChooseItem } from '~/types/api'
import { formatAdminError, normalizeImageUrlForStorage } from '~/composables/useAssetUrl'

definePageMeta({ layout: 'admin', middleware: 'admin-auth' })

const form = ref<SiteSettings | null>(null)
const whyItems = ref<WhyChooseItem[]>([])
const editingWhy = ref<(WhyChooseItem & { is_active: boolean }) | null>(null)
const saving = ref(false)
const whySaving = ref(false)
const message = ref('')
const error = ref('')
const whyError = ref('')

onMounted(async () => {
  form.value = await adminFetch<SiteSettings>('settings/')
  await loadWhyItems()
})

async function loadWhyItems() {
  whyItems.value = await adminFetch<WhyChooseItem[]>('why-items/')
}

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
        about_image_url: normalizeImageUrlForStorage(form.value.about_image_url),
      },
    })
    message.value = 'Paramètres enregistrés.'
  } catch (err) {
    error.value = formatAdminError(err)
  } finally {
    saving.value = false
  }
}

function startWhyCreate() {
  editingWhy.value = {
    text_fr: '',
    text_de: '',
    text_nl: '',
    order: whyItems.value.length + 1,
    is_active: true,
  }
  whyError.value = ''
}

function editWhyItem(item: WhyChooseItem) {
  editingWhy.value = {
    ...item,
    is_active: item.is_active ?? true,
  }
  whyError.value = ''
}

async function saveWhyItem() {
  if (!editingWhy.value) return
  if (!editingWhy.value.text_fr.trim()) {
    whyError.value = 'Le texte en français est obligatoire.'
    return
  }

  whySaving.value = true
  whyError.value = ''

  const payload = {
    text_fr: editingWhy.value.text_fr.trim(),
    text_de: editingWhy.value.text_de.trim(),
    text_nl: editingWhy.value.text_nl.trim(),
    order: Number(editingWhy.value.order) || 0,
    is_active: editingWhy.value.is_active,
  }

  try {
    if (editingWhy.value.id) {
      await adminFetch(`why-items/${editingWhy.value.id}/`, { method: 'PATCH', body: payload })
    } else {
      await adminFetch('why-items/', { method: 'POST', body: payload })
    }
    editingWhy.value = null
    await loadWhyItems()
  } catch (err) {
    whyError.value = formatAdminError(err)
  } finally {
    whySaving.value = false
  }
}

async function removeWhyItem(id: number) {
  if (!confirm('Supprimer cet argument ?')) return
  await adminFetch(`why-items/${id}/`, { method: 'DELETE' })
  await loadWhyItems()
}
</script>
