<template>
  <div>
    <h1 class="font-display text-4xl">Messages de contact</h1>
    <p class="mt-2 text-sm text-smoke">Demandes reçues via le formulaire du site.</p>

    <p v-if="!messages.length" class="mt-8 text-sm text-smoke">Aucun message pour le moment.</p>

    <ul class="mt-8 space-y-3">
      <li v-for="msg in messages" :key="msg.id" class="card !p-4" :class="{ 'opacity-60': msg.is_read }">
        <div class="flex flex-wrap items-start justify-between gap-4">
          <div class="min-w-0 flex-1">
            <p class="font-bold">{{ msg.name }} — {{ msg.subject }}</p>
            <p class="text-xs text-smoke">{{ msg.email }} · {{ msg.phone || '—' }}</p>
            <p class="mt-2 whitespace-pre-line text-sm">{{ msg.message }}</p>
            <p class="mt-1 text-xs text-smoke">{{ formatDate(msg.created_at, 'fr') }}</p>
          </div>

          <div class="flex flex-wrap gap-2">
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
definePageMeta({ layout: 'admin', middleware: 'admin-auth' })

interface AdminMessage {
  id: number
  name: string
  email: string
  phone: string
  subject: string
  message: string
  is_read: boolean
  created_at: string
}

const messages = ref<AdminMessage[]>([])

onMounted(load)

async function load() {
  const data = await adminFetch<{ results: AdminMessage[] } | AdminMessage[]>('messages/')
  messages.value = Array.isArray(data) ? data : data.results
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
  const body = encodeURIComponent(
    `\n\n---\nMessage de ${msg.name} (${msg.email}), reçu le ${formatDate(msg.created_at, 'fr')} :\n\n${msg.message}`,
  )
  return `mailto:${encodeURIComponent(msg.email)}?subject=${subject}&body=${body}`
}

async function removeMessage(id: number) {
  if (!confirm('Supprimer ce message définitivement ?')) return
  await adminFetch(`messages/${id}/`, { method: 'DELETE' })
  await load()
}
</script>
