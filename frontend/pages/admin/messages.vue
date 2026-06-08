<template>
  <div>
    <h1 class="font-display text-4xl">Messages de contact</h1>
    <p class="mt-2 text-sm text-smoke">Demandes reçues via le formulaire du site.</p>

    <p v-if="!messages.length" class="mt-8 text-sm text-smoke">Aucun message pour le moment.</p>

    <ul class="mt-8 space-y-3">
      <li v-for="msg in messages" :key="msg.id" class="card overflow-hidden !p-4" :class="{ 'opacity-60': msg.is_read }">
        <div class="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
          <div class="min-w-0 flex-1">
            <p class="break-words font-bold">{{ msg.name }}</p>
            <p class="mt-1 break-words text-sm text-ink">{{ msg.subject }}</p>
            <p class="mt-1 break-all text-xs text-smoke">{{ msg.email }} · {{ msg.phone || '—' }}</p>

            <div
              v-if="msg.vehicle"
              class="mt-3 border-2 border-ink bg-acid/10 px-3 py-2 text-sm"
            >
              <p class="text-[10px] font-bold uppercase tracking-street text-smoke">
                Annonce véhicule
              </p>
              <p class="mt-1 break-words font-bold text-ink">
                {{ vehicleLabel(msg.vehicle) }}
              </p>
              <p class="break-words text-xs text-smoke">
                {{ msg.vehicle.brand }} {{ msg.vehicle.model_name }} ({{ msg.vehicle.year }})
                <span v-if="msg.vehicle.is_sold" class="font-bold text-red-600"> · Vendu</span>
              </p>
              <a
                :href="vehiclePublicUrl(msg.vehicle.slug)"
                target="_blank"
                rel="noopener noreferrer"
                class="mt-2 inline-block break-all text-xs font-bold uppercase tracking-street underline-offset-4 hover:underline"
              >
                Voir l'annonce →
              </a>
            </div>

            <p class="mt-3 break-words whitespace-pre-wrap text-sm leading-relaxed">{{ msg.message }}</p>
            <p class="mt-2 text-xs text-smoke">{{ formatDate(msg.created_at, 'fr') }}</p>
          </div>

          <div class="flex shrink-0 flex-wrap gap-2">
            <a
              :href="replyHref(msg)"
              class="btn-primary !px-3 !py-1.5 text-xs"
              @click="markReadOnReply(msg)"
            >
              Répondre
            </a>
            <button
              v-if="!msg.is_read"
              type="button"
              class="border-2 border-ink px-3 py-1.5 text-xs font-bold uppercase"
              @click="markRead(msg.id)"
            >
              Marquer lu
            </button>
            <button
              type="button"
              class="border-2 border-red-600 px-3 py-1.5 text-xs font-bold uppercase text-red-600"
              @click="removeMessage(msg.id)"
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
import type { ContactMessageVehicle } from '~/types/api'

definePageMeta({ layout: 'admin', middleware: 'admin-auth' })

interface AdminMessage {
  id: number
  name: string
  email: string
  phone: string
  subject: string
  message: string
  vehicle: ContactMessageVehicle | null
  is_read: boolean
  created_at: string
}

const config = useRuntimeConfig()
const messages = ref<AdminMessage[]>([])

onMounted(load)

async function load() {
  const data = await adminFetch<{ results: AdminMessage[] } | AdminMessage[]>('messages/')
  messages.value = Array.isArray(data) ? data : data.results
}

function vehicleLabel(vehicle: ContactMessageVehicle) {
  return vehicle.title_fr || `${vehicle.brand} ${vehicle.model_name}`
}

function vehiclePublicUrl(slug: string) {
  const siteUrl = (config.public.siteUrl as string || '').replace(/\/$/, '')
  return `${siteUrl}/vehicules/${slug}`
}

async function markRead(id: number) {
  await adminFetch(`messages/${id}/`, { method: 'PATCH', body: { is_read: true } })
  await load()
}

async function markReadOnReply(msg: AdminMessage) {
  if (!msg.is_read) {
    await adminFetch(`messages/${msg.id}/`, { method: 'PATCH', body: { is_read: true } })
    msg.is_read = true
  }
}

function replyHref(msg: AdminMessage): string {
  const subject = encodeURIComponent(`Re: ${msg.subject}`)
  let body = `\n\n---\nMessage de ${msg.name} (${msg.email}), reçu le ${formatDate(msg.created_at, 'fr')} :\n\n${msg.message}`
  if (msg.vehicle) {
    body = `\n\n---\nAnnonce : ${vehicleLabel(msg.vehicle)} (${msg.vehicle.slug})\n${body}`
  }
  return `mailto:${encodeURIComponent(msg.email)}?subject=${subject}&body=${encodeURIComponent(body)}`
}

async function removeMessage(id: number) {
  if (!confirm('Supprimer ce message définitivement ?')) return
  await adminFetch(`messages/${id}/`, { method: 'DELETE' })
  await load()
}
</script>
