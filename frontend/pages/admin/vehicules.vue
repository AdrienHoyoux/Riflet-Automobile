<template>

  <div>

    <div class="flex flex-wrap items-center justify-between gap-4">

      <div>

        <h1 class="font-display text-4xl">Véhicules d'occasion</h1>

        <p class="mt-2 text-sm text-smoke">Ajoutez et gérez les voitures en vente.</p>

      </div>

      <button type="button" class="btn-primary" @click="startCreate">Ajouter un véhicule</button>

    </div>



    <form v-if="editing" class="card mt-8 space-y-4" @submit.prevent="saveVehicle">

      <h2 class="font-display text-2xl">{{ editing.id ? 'Modifier' : 'Ajouter' }} un véhicule</h2>

      <div class="grid gap-4 sm:grid-cols-2">

        <AdminField v-model="editing.brand" label="Marque" />

        <AdminField v-model="editing.model_name" label="Modèle" />

        <AdminField v-model="editing.year" label="Année" type="number" />

        <AdminField v-model="editing.mileage" label="Kilométrage" type="number" />

        <AdminField v-model="editing.price" label="Prix (€)" />
        <p class="text-xs text-smoke">Jusqu'à 10 chiffres (ex. 9 999 999 999 €).</p>

        <div>

          <label class="block">

            <span class="text-xs font-bold uppercase tracking-street">Carburant</span>

            <select v-model="editing.fuel_type" class="mt-2 w-full border-2 border-ink bg-chalk px-3 py-2 text-sm">

              <option value="petrol">Essence</option>

              <option value="diesel">Diesel</option>

              <option value="electric">Électrique</option>

              <option value="hybrid">Hybride</option>

              <option value="lpg">LPG</option>

            </select>

          </label>

        </div>

      </div>

      <AdminField v-model="editing.title_fr" label="Titre affiché (FR)" />

      <AdminField v-model="editing.description_fr" label="Description (FR)" type="textarea" />

      <AdminMultiImageUpload
        v-model="editing.gallery_urls"
        label="Photos du véhicule"
        hint="Ajoutez plusieurs photos. La première sera utilisée sur la liste des véhicules."
        folder="vehicles"
      >
        <template #site-preview>
          <VehicleCard :vehicle="previewVehicle" />
        </template>
      </AdminMultiImageUpload>

      <div class="flex flex-wrap gap-4 text-sm">

        <label class="flex items-center gap-2"><input v-model="editing.is_active" type="checkbox"> Visible sur le site</label>

        <label class="flex items-center gap-2"><input v-model="editing.is_sold" type="checkbox"> Vendu</label>

      </div>

      <p v-if="error" class="text-sm font-bold text-red-600">{{ error }}</p>

      <div class="flex gap-3">

        <button type="submit" class="btn-primary" :disabled="saving">{{ saving ? 'Enregistrement...' : (editing.id ? 'Mettre à jour' : 'Ajouter') }}</button>

        <button type="button" class="border-2 border-ink px-4 py-2 text-xs font-bold uppercase" @click="editing = null">Annuler</button>

      </div>

    </form>



    <ul class="mt-8 space-y-3">

      <li v-for="vehicle in vehicles" :key="vehicle.id" class="card flex flex-wrap items-center justify-between gap-4 !p-4">

        <div>

          <p class="font-display text-xl">{{ vehicle.brand }} {{ vehicle.model_name }} ({{ vehicle.year }})</p>

          <p class="text-sm text-smoke">{{ formatPrice(vehicle.price) }} — {{ vehicle.mileage }} km</p>

          <p class="text-xs text-smoke">

            {{ vehicle.is_sold ? 'Vendu' : vehicle.is_active ? 'En ligne' : 'Masqué' }}

          </p>

        </div>

        <div class="flex gap-2">

          <button type="button" class="border-2 border-ink px-3 py-1 text-xs font-bold uppercase" @click="editVehicle(vehicle)">Modifier</button>

          <button type="button" class="border-2 border-red-600 px-3 py-1 text-xs font-bold uppercase text-red-600" @click="removeVehicle(vehicle.id)">Supprimer</button>

        </div>

      </li>

    </ul>

  </div>

</template>



<script setup lang="ts">
import type { UsedVehicle } from '~/types/api'
import { formatAdminError, imageUrlFromPreview, normalizeImageUrlForStorage, resolveImageUrl } from '~/composables/useAssetUrl'
import { parsePriceInput } from '~/utils/price'

definePageMeta({ layout: 'admin', middleware: 'admin-auth' })



interface AdminVehicle {

  id?: number

  slug?: string

  brand: string

  model_name: string

  year: string | number

  mileage: string | number

  fuel_type: string

  transmission: string

  price: string | number

  title_fr: string

  description_fr: string

  image_url: string

  gallery_urls: string[]

  gallery?: string[]

  image_preview?: string | null

  is_active: boolean

  is_sold: boolean

  order: number

}



const vehicles = ref<AdminVehicle[]>([])

const editing = ref<AdminVehicle | null>(null)

const saving = ref(false)

const error = ref('')

const previewVehicle = computed((): UsedVehicle => {
  const vehicle = editing.value ?? emptyVehicle()
  const title = vehicle.title_fr.trim() || `${vehicle.brand} ${vehicle.model_name}`.trim()

  return {
    id: 0,
    slug: 'apercu',
    brand: vehicle.brand || 'Marque',
    model_name: vehicle.model_name || 'Modèle',
    year: Number(vehicle.year) || new Date().getFullYear(),
    mileage: Number(vehicle.mileage) || 0,
    fuel_type: vehicle.fuel_type,
    transmission: vehicle.transmission,
    price: vehicle.price || 0,
    title_fr: title || 'Titre du véhicule',
    title_de: '',
    title_nl: '',
    description_fr: vehicle.description_fr || 'Description du véhicule…',
    description_de: '',
    description_nl: '',
    image: resolveImageUrl(vehicle.gallery_urls[0] || vehicle.image_url) || null,
    is_sold: vehicle.is_sold,
    order: 0,
  }
})

function emptyVehicle(): AdminVehicle {

  return {

    brand: '',

    model_name: '',

    year: new Date().getFullYear().toString(),

    mileage: '0',

    fuel_type: 'diesel',

    transmission: 'manual',

    price: '0',

    title_fr: '',

    description_fr: '',

    image_url: '',

    gallery_urls: [],

    is_active: true,

    is_sold: false,

    order: 0,

  }

}



function buildPayload(vehicle: AdminVehicle) {
  const title = vehicle.title_fr.trim() || `${vehicle.brand} ${vehicle.model_name}`.trim()
  const price = parsePriceInput(vehicle.price)

  return {
    brand: vehicle.brand,
    model_name: vehicle.model_name,
    year: Number(vehicle.year),
    mileage: Number(vehicle.mileage),
    fuel_type: vehicle.fuel_type,
    transmission: vehicle.transmission,
    price,
    title_fr: title,
    description_fr: vehicle.description_fr,
    gallery_urls: vehicle.gallery_urls.map(url => normalizeImageUrlForStorage(url)),
    is_active: vehicle.is_active,
    is_sold: vehicle.is_sold,
    order: vehicle.order,
  }
}



onMounted(load)



async function load() {

  const data = await adminFetch<{ results: AdminVehicle[] } | AdminVehicle[]>('vehicles/')

  vehicles.value = Array.isArray(data) ? data : data.results

}



function startCreate() {

  editing.value = emptyVehicle()

  error.value = ''

}



function editVehicle(vehicle: AdminVehicle) {

  editing.value = {

    ...vehicle,

    year: String(vehicle.year),

    mileage: String(vehicle.mileage),

    price: String(vehicle.price),

    image_url: imageUrlFromPreview(vehicle.image_preview, vehicle.image_url),

    gallery_urls: (vehicle.gallery?.length
      ? vehicle.gallery
      : [imageUrlFromPreview(vehicle.image_preview, vehicle.image_url)]
    ).filter(Boolean).map(url => normalizeImageUrlForStorage(url)),

  }

  error.value = ''

}



async function saveVehicle() {

  if (!editing.value) return

  saving.value = true

  error.value = ''

  try {
    const body = buildPayload(editing.value)
    if (editing.value.id) {
      await adminFetch(`vehicles/${editing.value.id}/`, { method: 'PATCH', body })
    } else {
      await adminFetch('vehicles/', { method: 'POST', body })
    }
    editing.value = null
    await load()
  } catch (err) {
    error.value = err instanceof Error && err.message.includes('chiffres')
      ? err.message
      : formatAdminError(err)
  } finally {

    saving.value = false

  }

}



async function removeVehicle(id: number) {

  if (!confirm('Supprimer ce véhicule ?')) return

  await adminFetch(`vehicles/${id}/`, { method: 'DELETE' })

  await load()

}



function formatPrice(value: string | number) {

  return new Intl.NumberFormat('fr-BE', { style: 'currency', currency: 'EUR', maximumFractionDigits: 0 }).format(Number(value))

}

</script>


