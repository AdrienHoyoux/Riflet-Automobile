<template>
  <div>
    <AdminSectionHeader
      eyebrow="Contenu du site"
      title="Page d'accueil"
      description="Modifiez les textes des sections visibles sur la page d'accueil. Les cartes de services (entretien, pneus, etc.) se gèrent dans « Page Services »."
      page-url="/"
    />

    <form v-if="form" class="mt-8 space-y-8" @submit.prevent="saveSettings">
      <AdminI18nBlock
        :form="form"
        title="Bloc « Nos services »"
        help="Titre et introduction au-dessus des 6 cartes de services sur l'accueil. La liste des prestations se modifie dans Page Services."
        title-prefix="home_services_title"
        subtitle-prefix="home_services_subtitle"
        :defaults="ADMIN_DEFAULTS.homeServices"
      />

      <section class="card space-y-6">
        <div>
          <h2 class="font-display text-2xl">Bloc « Pourquoi nous choisir ? »</h2>
          <p class="mt-2 text-sm text-smoke">Titre de la section et liste des arguments (3 colonnes sur l'accueil).</p>
        </div>

        <AdminI18nBlock
          :form="form"
          plain
          title="Titre de la section"
          title-prefix="home_why_title"
          :defaults="ADMIN_DEFAULTS.homeWhy"
        />

        <div class="border-t-2 border-ink pt-6">
          <h3 class="font-display text-xl">Arguments (colonnes)</h3>
          <p class="mt-2 text-sm text-smoke">Chaque ligne correspond à une colonne sur l'accueil.</p>

          <div v-if="editingWhy" class="mt-4 space-y-4 border-2 border-ink bg-chalk-dark p-4">
            <h4 class="font-display text-lg">{{ editingWhy.id ? 'Modifier' : 'Ajouter' }} un argument</h4>
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

          <button v-else type="button" class="btn-secondary mt-4" @click="startWhyCreate">
            Ajouter un argument
          </button>
          <ul v-if="whyItems.length" class="mt-4 space-y-3">
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
          <p v-else class="mt-4 text-sm text-smoke">Aucun argument — les textes par défaut du site seront utilisés.</p>
        </div>
      </section>

      <AdminSaveBar :message="message" :error="error" :saving="saving" />
    </form>
  </div>
</template>

<script setup lang="ts">
import type { WhyChooseItem } from '~/types/api'
import { formatAdminError } from '~/composables/useAssetUrl'
import { ADMIN_DEFAULTS } from '~/utils/adminDefaults'

definePageMeta({ layout: 'admin', middleware: 'admin-auth' })

const { form, saving, message, error, loadSettings, saveSettings } = useAdminSettingsForm()
const whyItems = ref<WhyChooseItem[]>([])
const editingWhy = ref<(WhyChooseItem & { is_active: boolean }) | null>(null)
const whySaving = ref(false)
const whyError = ref('')

onMounted(async () => {
  await loadSettings()
  await loadWhyItems()
})

async function loadWhyItems() {
  whyItems.value = await adminFetch<WhyChooseItem[]>('why-items/')
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
  editingWhy.value = { ...item, is_active: item.is_active ?? true }
  whyError.value = ''
}

async function saveWhyItem() {
  if (!editingWhy.value?.text_fr.trim()) {
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
