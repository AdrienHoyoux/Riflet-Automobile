<template>

  <div>

    <div class="flex flex-wrap items-center justify-between gap-4">

      <div>

        <h1 class="font-display text-4xl">Actualités</h1>

        <p class="mt-2 text-sm text-smoke">Publiez des nouvelles sur le garage.</p>

      </div>

      <button type="button" class="btn-primary" @click="startCreate">Nouvelle actualité</button>

    </div>



    <form v-if="editing" class="card mt-8 space-y-4" @submit.prevent="saveArticle">

      <h2 class="font-display text-2xl">{{ editing.id ? 'Modifier' : 'Créer' }} une actualité</h2>

      <AdminField v-model="editing.title_fr" label="Titre (FR)" />

      <AdminField v-model="editing.description_fr" label="Résumé (FR)" type="textarea" />

      <AdminField v-model="editing.content_fr" label="Contenu (FR)" type="textarea" />

      <AdminImageUpload v-model="editing.image_url" label="Image" folder="news" url-label="URL image">
        <template #site-preview>
          <NewsCard :article="previewArticle" :index="0" />
        </template>
      </AdminImageUpload>

      <label class="flex items-center gap-2 text-sm">

        <input v-model="editing.is_published" type="checkbox">

        Publié sur le site

      </label>

      <p v-if="error" class="text-sm font-bold text-red-600">{{ error }}</p>

      <div class="flex gap-3">

        <button type="submit" class="btn-primary" :disabled="saving">{{ saving ? 'Enregistrement...' : (editing.id ? 'Mettre à jour' : 'Publier') }}</button>

        <button type="button" class="border-2 border-ink px-4 py-2 text-xs font-bold uppercase" @click="editing = null">Annuler</button>

      </div>

    </form>



    <ul class="mt-8 space-y-3">

      <li v-for="article in articles" :key="article.id" class="card flex flex-wrap items-center justify-between gap-4 !p-4">

        <div>

          <p class="font-display text-xl">{{ article.title_fr }}</p>

          <p class="text-xs text-smoke">{{ article.is_published ? 'Publié' : 'Brouillon' }} — {{ article.slug }}</p>

        </div>

        <div class="flex gap-2">

          <button type="button" class="border-2 border-ink px-3 py-1 text-xs font-bold uppercase" @click="editArticle(article)">Modifier</button>

          <button type="button" class="border-2 border-red-600 px-3 py-1 text-xs font-bold uppercase text-red-600" @click="removeArticle(article.id)">Supprimer</button>

        </div>

      </li>

    </ul>

  </div>

</template>



<script setup lang="ts">
import type { NewsArticle } from '~/types/api'
import { formatAdminError, normalizeImageUrlForStorage, resolveImageUrl } from '~/composables/useAssetUrl'

definePageMeta({ layout: 'admin', middleware: 'admin-auth' })



interface AdminNews {

  id?: number

  slug?: string

  title_fr: string

  description_fr: string

  content_fr: string

  image_url: string

  is_published: boolean

}



const articles = ref<AdminNews[]>([])

const editing = ref<AdminNews | null>(null)

const saving = ref(false)

const error = ref('')

const previewArticle = computed((): NewsArticle => {
  const article = editing.value ?? emptyArticle()

  return {
    id: 0,
    slug: 'apercu',
    title_fr: article.title_fr || 'Titre de l\'actualité',
    title_de: '',
    title_nl: '',
    description_fr: article.description_fr || 'Résumé de l\'actualité…',
    description_de: '',
    description_nl: '',
    image: resolveImageUrl(article.image_url) || null,
    published_at: new Date().toISOString(),
  }
})

function emptyArticle(): AdminNews {

  return {

    title_fr: '',

    description_fr: '',

    content_fr: '',

    image_url: '',

    is_published: true,

  }

}



function buildPayload(article: AdminNews) {

  return {

    title_fr: article.title_fr,

    description_fr: article.description_fr,

    content_fr: article.content_fr,

    image_url: normalizeImageUrlForStorage(article.image_url),

    is_published: article.is_published,

  }

}



onMounted(load)



async function load() {

  const data = await adminFetch<{ results: AdminNews[] } | AdminNews[]>('news/')

  articles.value = Array.isArray(data) ? data : data.results

}



function startCreate() {

  editing.value = emptyArticle()

  error.value = ''

}



function editArticle(article: AdminNews) {

  editing.value = {

    id: article.id,

    slug: article.slug,

    title_fr: article.title_fr,

    description_fr: article.description_fr || '',

    content_fr: article.content_fr || '',

    image_url: article.image_url || '',

    is_published: article.is_published,

  }

  error.value = ''

}



async function saveArticle() {

  if (!editing.value) return

  saving.value = true

  error.value = ''

  try {

    const body = buildPayload(editing.value)

    if (editing.value.id) {

      await adminFetch(`news/${editing.value.id}/`, { method: 'PATCH', body })

    } else {

      await adminFetch('news/', { method: 'POST', body })

    }

    editing.value = null

    await load()

  } catch (err) {

    error.value = formatAdminError(err)

  } finally {

    saving.value = false

  }

}



async function removeArticle(id: number) {

  if (!confirm('Supprimer cette actualité ?')) return

  await adminFetch(`news/${id}/`, { method: 'DELETE' })

  await load()

}

</script>


