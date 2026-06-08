<template>
  <div>
    <div class="flex flex-wrap items-center justify-between gap-4">
      <div>
        <h1 class="font-display text-4xl">Services</h1>
        <p class="mt-2 text-sm text-smoke">Gérez les prestations affichées sur l'accueil et la page Services.</p>
      </div>
      <button type="button" class="btn-primary" @click="startCreate">Ajouter un service</button>
    </div>

    <form v-if="editing" class="card mt-8 space-y-4" @submit.prevent="saveService">
      <h2 class="font-display text-2xl">{{ editing.id ? 'Modifier' : 'Ajouter' }} un service</h2>

      <div class="grid gap-4 sm:grid-cols-2">
        <AdminField v-model="editing.order" label="Ordre d'affichage" type="number" />
        <AdminField v-model="editing.icon" label="Icône (emoji, optionnel)" />
      </div>

      <AdminField v-model="editing.title_fr" label="Titre (FR)" />
      <AdminField v-model="editing.title_de" label="Titre (DE)" />
      <AdminField v-model="editing.title_nl" label="Titre (NL)" />

      <AdminField v-model="editing.description_fr" label="Description (FR)" type="textarea" />
      <AdminField v-model="editing.description_de" label="Description (DE)" type="textarea" />
      <AdminField v-model="editing.description_nl" label="Description (NL)" type="textarea" />

      <AdminImageUpload v-model="editing.image_url" label="Image" folder="services" url-label="URL image">
        <template #site-preview>
          <ServiceCard :service="previewService" />
        </template>
      </AdminImageUpload>

      <label class="flex items-center gap-2 text-sm">
        <input v-model="editing.is_active" type="checkbox">
        Visible sur le site
      </label>

      <p v-if="error" class="text-sm font-bold text-red-600">{{ error }}</p>

      <div class="flex gap-3">
        <button type="submit" class="btn-primary" :disabled="saving">
          {{ saving ? 'Enregistrement...' : (editing.id ? 'Mettre à jour' : 'Ajouter') }}
        </button>
        <button type="button" class="border-2 border-ink px-4 py-2 text-xs font-bold uppercase" @click="editing = null">
          Annuler
        </button>
      </div>
    </form>

    <ul class="mt-8 space-y-3">
      <li
        v-for="service in services"
        :key="service.id"
        class="card flex flex-wrap items-center justify-between gap-4 !p-4"
      >
        <div>
          <p class="font-display text-xl">{{ service.title_fr }}</p>
          <p class="text-xs text-smoke">
            Ordre {{ service.order }} — {{ service.is_active ? 'En ligne' : 'Masqué' }}
          </p>
        </div>
        <div class="flex gap-2">
          <button type="button" class="border-2 border-ink px-3 py-1 text-xs font-bold uppercase" @click="editService(service)">
            Modifier
          </button>
          <button type="button" class="border-2 border-red-600 px-3 py-1 text-xs font-bold uppercase text-red-600" @click="removeService(service.id!)">
            Supprimer
          </button>
        </div>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import type { Service } from '~/types/api'
import { formatAdminError, normalizeImageUrlForStorage, resolveImageUrl } from '~/composables/useAssetUrl'

definePageMeta({ layout: 'admin', middleware: 'admin-auth' })

interface AdminService extends Service {
  id?: number
  image_url: string
  image_preview?: string | null
  is_active: boolean
}

const services = ref<AdminService[]>([])
const editing = ref<AdminService | null>(null)
const saving = ref(false)
const error = ref('')

const previewService = computed((): Service => {
  const service = editing.value ?? emptyService()
  return {
    id: 0,
    title_fr: service.title_fr || 'Titre du service',
    title_de: service.title_de,
    title_nl: service.title_nl,
    description_fr: service.description_fr || 'Description du service…',
    description_de: service.description_de,
    description_nl: service.description_nl,
    icon: service.icon,
    image: resolveImageUrl(service.image_url) || null,
    order: Number(service.order) || 1,
  }
})

function emptyService(): AdminService {
  return {
    title_fr: '',
    title_de: '',
    title_nl: '',
    description_fr: '',
    description_de: '',
    description_nl: '',
    icon: '',
    image_url: '',
    order: services.value.length + 1,
    is_active: true,
  }
}

function buildPayload(service: AdminService) {
  return {
    title_fr: service.title_fr.trim(),
    title_de: service.title_de.trim(),
    title_nl: service.title_nl.trim(),
    description_fr: service.description_fr.trim(),
    description_de: service.description_de.trim(),
    description_nl: service.description_nl.trim(),
    icon: service.icon.trim(),
    image_url: normalizeImageUrlForStorage(service.image_url),
    order: Number(service.order) || 0,
    is_active: service.is_active,
  }
}

onMounted(load)

async function load() {
  services.value = await adminFetch<AdminService[]>('services/')
}

function startCreate() {
  editing.value = emptyService()
  error.value = ''
}

function editService(service: AdminService) {
  editing.value = {
    ...service,
    image_url: service.image_url || '',
  }
  error.value = ''
}

async function saveService() {
  if (!editing.value) return
  if (!editing.value.title_fr.trim()) {
    error.value = 'Le titre en français est obligatoire.'
    return
  }

  saving.value = true
  error.value = ''

  try {
    const payload = buildPayload(editing.value)
    if (editing.value.id) {
      await adminFetch(`services/${editing.value.id}/`, { method: 'PATCH', body: payload })
    } else {
      await adminFetch('services/', { method: 'POST', body: payload })
    }
    editing.value = null
    await load()
  } catch (err) {
    error.value = formatAdminError(err)
  } finally {
    saving.value = false
  }
}

async function removeService(id: number) {
  if (!confirm('Supprimer ce service ?')) return
  await adminFetch(`services/${id}/`, { method: 'DELETE' })
  await load()
}
</script>
