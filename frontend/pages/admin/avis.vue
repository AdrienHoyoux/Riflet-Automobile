<template>
  <div>
    <div class="flex flex-wrap items-center justify-between gap-4">
      <div>
        <h1 class="font-display text-4xl">Avis clients</h1>
        <p class="mt-2 text-sm text-smoke">
          Ajoutez vos avis à la main (copiés depuis Google Maps, Facebook, etc.), puis choisissez
          <strong class="text-ink">{{ selectedIds.length }} / {{ maxFeatured }}</strong> pour l'accueil.
          Aucune API Google payante requise.
        </p>
      </div>
      <div class="flex flex-wrap gap-2">
        <button type="button" class="btn-primary" @click="startCreate">
          Ajouter un avis
        </button>
        <button
          type="button"
          class="btn-primary"
          :disabled="saving || selectedIds.length === 0"
          @click="saveSelection"
        >
          {{ saving ? 'Enregistrement...' : 'Enregistrer la sélection' }}
        </button>
      </div>
    </div>

    <p v-if="message" class="mt-4 text-sm font-bold text-green-700">{{ message }}</p>
    <p v-if="error" class="mt-4 text-sm font-bold text-red-600">{{ error }}</p>

    <form v-if="editing" class="card mt-8 space-y-4" @submit.prevent="saveReview">
      <h2 class="font-display text-2xl">{{ editing.id ? 'Modifier' : 'Ajouter' }} un avis</h2>
      <AdminField v-model="editing.author_name" label="Nom du client" required />
      <div>
        <label class="text-xs font-bold uppercase tracking-street text-smoke">Note (1 à 5)</label>
        <select
          v-model.number="editing.rating"
          class="mt-1 w-full border-2 border-ink bg-chalk px-3 py-2 text-sm"
        >
          <option v-for="n in 5" :key="n" :value="n">{{ n }} / 5</option>
        </select>
      </div>
      <AdminField v-model="editing.content" label="Commentaire" type="textarea" required />
      <AdminField v-model="editing.review_date" label="Date (optionnel)" type="date" />
      <div class="flex gap-3">
        <button type="submit" class="btn-primary" :disabled="formSaving">
          {{ formSaving ? 'Enregistrement...' : (editing.id ? 'Mettre à jour' : 'Ajouter') }}
        </button>
        <button
          type="button"
          class="border-2 border-ink px-4 py-2 text-xs font-bold uppercase"
          @click="editing = null"
        >
          Annuler
        </button>
      </div>
    </form>

    <section class="card mt-8 space-y-4">
      <h2 class="font-display text-2xl">Bloc « Google » sur l'accueil</h2>
      <p class="text-sm text-smoke">
        Note et nombre d'avis affichés à côté du lien Google (à renseigner vous-même depuis votre fiche Google).
      </p>
      <div class="grid gap-4 sm:grid-cols-3">
        <AdminField v-model="googleForm.google_rating" label="Note moyenne (ex. 4.9)" />
        <AdminField v-model="googleForm.google_review_count" label="Nombre total d'avis" type="number" />
        <AdminField v-model="googleForm.google_maps_url" label="Lien Google Maps" type="url" />
      </div>
      <button
        type="button"
        class="border-2 border-ink px-4 py-2 text-xs font-bold uppercase"
        :disabled="googleSaving"
        @click="saveGoogleBlock"
      >
        {{ googleSaving ? 'Enregistrement...' : 'Enregistrer le bloc Google' }}
      </button>
    </section>

    <details class="card mt-8">
      <summary class="cursor-pointer font-display text-lg">
        Synchronisation Google (API payante, optionnel)
      </summary>
      <p class="mt-3 text-sm text-smoke">
        Nécessite une clé Google Places API facturée après le crédit gratuit mensuel.
        Sans clé, utilisez l'ajout manuel ci-dessus.
      </p>
      <button
        type="button"
        class="mt-4 border-2 border-ink px-4 py-2 text-xs font-bold uppercase"
        :disabled="refreshing"
        @click="refreshFromGoogle"
      >
        {{ refreshing ? 'Actualisation...' : 'Rafraîchir depuis Google' }}
      </button>
    </details>

    <p v-if="!reviews.length" class="mt-8 text-sm text-smoke">
      Aucun avis. Cliquez sur « Ajouter un avis » ou lancez <code class="text-xs">seed_data</code> en dev.
    </p>

    <ul class="mt-8 space-y-3">
      <li
        v-for="review in reviews"
        :key="review.id"
        class="card !p-4 transition"
        :class="isSelected(review.id) ? '!border-acid !bg-acid/10' : ''"
      >
        <div class="flex flex-wrap items-start gap-4">
          <label class="flex shrink-0 cursor-pointer items-start gap-3">
            <input
              type="checkbox"
              class="mt-1 h-4 w-4 border-2 border-ink"
              :checked="isSelected(review.id)"
              :disabled="!isSelected(review.id) && selectedIds.length >= maxFeatured"
              @change="toggleSelection(review.id)"
            >
            <span class="sr-only">Sélectionner pour l'accueil</span>
          </label>

          <div class="min-w-0 flex-1">
            <div class="flex flex-wrap items-center gap-2">
              <p class="font-bold">{{ review.author_name }} — {{ review.rating }}/5</p>
              <span
                v-if="isSelected(review.id)"
                class="bg-ink px-2 py-0.5 text-[10px] font-bold uppercase tracking-street text-chalk"
              >
                Sur l'accueil
              </span>
            </div>
            <p class="mt-2 text-sm leading-relaxed text-smoke">{{ review.content }}</p>
            <p class="mt-1 text-xs text-smoke">
              {{ sourceLabel(review.source) }}
              <span v-if="review.review_date"> · {{ formatDate(review.review_date) }}</span>
            </p>
          </div>

          <div class="flex gap-2">
            <button
              type="button"
              class="border-2 border-ink px-3 py-1 text-xs font-bold uppercase"
              @click="editReview(review)"
            >
              Modifier
            </button>
            <button
              type="button"
              class="border-2 border-red-600 px-3 py-1 text-xs font-bold uppercase text-red-600"
              @click="removeReview(review.id)"
            >
              Supprimer
            </button>
          </div>
        </div>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import type { SiteSettings } from '~/types/api'
import { formatAdminError } from '~/composables/useAssetUrl'

definePageMeta({ layout: 'admin', middleware: 'admin-auth' })

const maxFeatured = 6

interface AdminReview {
  id: number
  author_name: string
  rating: number
  content: string
  source: string
  review_date: string | null
  is_published: boolean
  order: number
}

interface ReviewForm {
  id?: number
  author_name: string
  rating: number
  content: string
  review_date: string
}

const reviews = ref<AdminReview[]>([])
const selectedIds = ref<number[]>([])
const editing = ref<ReviewForm | null>(null)
const saving = ref(false)
const formSaving = ref(false)
const refreshing = ref(false)
const googleSaving = ref(false)
const message = ref('')
const error = ref('')

const googleForm = ref({
  google_rating: '5',
  google_review_count: '0',
  google_maps_url: '',
})

onMounted(async () => {
  await Promise.all([load(), loadGoogleBlock()])
})

function emptyForm(): ReviewForm {
  return { author_name: '', rating: 5, content: '', review_date: '' }
}

function startCreate() {
  editing.value = emptyForm()
  error.value = ''
}

function editReview(review: AdminReview) {
  editing.value = {
    id: review.id,
    author_name: review.author_name,
    rating: review.rating,
    content: review.content,
    review_date: review.review_date || '',
  }
  error.value = ''
}

async function load() {
  const data = await adminFetch<AdminReview[]>('reviews/')
  reviews.value = Array.isArray(data) ? data : []
  selectedIds.value = reviews.value
    .filter(review => review.is_published)
    .sort((a, b) => a.order - b.order)
    .map(review => review.id)
}

async function loadGoogleBlock() {
  const settings = await adminFetch<SiteSettings>('settings/')
  googleForm.value = {
    google_rating: String(settings.google_rating ?? '5'),
    google_review_count: String(settings.google_review_count ?? 0),
    google_maps_url: settings.google_maps_url || '',
  }
}

async function saveReview() {
  if (!editing.value) return
  formSaving.value = true
  error.value = ''
  const body = {
    author_name: editing.value.author_name.trim(),
    rating: editing.value.rating,
    content: editing.value.content.trim(),
    review_date: editing.value.review_date || null,
  }
  try {
    if (editing.value.id) {
      await adminFetch(`reviews/${editing.value.id}/`, { method: 'PATCH', body })
      message.value = 'Avis mis à jour.'
    } else {
      await adminFetch('reviews/', { method: 'POST', body })
      message.value = 'Avis ajouté. Cochez-le puis enregistrez la sélection pour l\'accueil.'
    }
    editing.value = null
    await load()
  } catch (err) {
    error.value = formatAdminError(err)
  } finally {
    formSaving.value = false
  }
}

async function saveGoogleBlock() {
  googleSaving.value = true
  error.value = ''
  try {
    await adminFetch('settings/', {
      method: 'PATCH',
      body: {
        google_rating: googleForm.value.google_rating,
        google_review_count: Number(googleForm.value.google_review_count) || 0,
        google_maps_url: googleForm.value.google_maps_url,
      },
    })
    message.value = 'Bloc Google enregistré.'
  } catch (err) {
    error.value = formatAdminError(err)
  } finally {
    googleSaving.value = false
  }
}

function isSelected(id: number) {
  return selectedIds.value.includes(id)
}

function toggleSelection(id: number) {
  if (isSelected(id)) {
    selectedIds.value = selectedIds.value.filter(item => item !== id)
    return
  }
  if (selectedIds.value.length >= maxFeatured) {
    error.value = `Vous ne pouvez sélectionner que ${maxFeatured} avis maximum.`
    return
  }
  error.value = ''
  selectedIds.value = [...selectedIds.value, id]
}

async function saveSelection() {
  saving.value = true
  message.value = ''
  error.value = ''
  try {
    const result = await adminFetch<{ detail: string }>('reviews/selection/', {
      method: 'POST',
      body: { review_ids: selectedIds.value },
    })
    message.value = result.detail
    await load()
  } catch (err) {
    error.value = formatAdminError(err)
  } finally {
    saving.value = false
  }
}

async function refreshFromGoogle() {
  refreshing.value = true
  message.value = ''
  error.value = ''
  try {
    const result = await adminFetch<{ ok: boolean, detail: string }>('reviews/sync/', {
      method: 'POST',
    })
    message.value = result.detail
    await load()
    await loadGoogleBlock()
  } catch (err) {
    error.value = formatAdminError(err)
  } finally {
    refreshing.value = false
  }
}

async function removeReview(id: number) {
  if (!confirm('Supprimer cet avis ?')) return
  try {
    await adminFetch(`reviews/${id}/`, { method: 'DELETE' })
    selectedIds.value = selectedIds.value.filter(item => item !== id)
    await load()
  } catch (err) {
    error.value = formatAdminError(err)
  }
}

function sourceLabel(source: string) {
  if (source === 'manual') return 'Saisie manuelle'
  if (source === 'facebook') return 'Facebook'
  return 'Google'
}

function formatDate(value: string) {
  return new Intl.DateTimeFormat('fr-BE', { dateStyle: 'medium' }).format(new Date(value))
}
</script>
