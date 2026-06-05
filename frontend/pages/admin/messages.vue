<template>
  <div>
    <h1 class="font-display text-4xl">Messages de contact</h1>
    <p class="mt-2 text-sm text-smoke">Demandes reçues via le formulaire du site.</p>

    <ul class="mt-8 space-y-3">
      <li v-for="msg in messages" :key="msg.id" class="card !p-4" :class="{ 'opacity-60': msg.is_read }">
        <div class="flex flex-wrap items-start justify-between gap-4">
          <div>
            <p class="font-bold">{{ msg.name }} — {{ msg.subject }}</p>
            <p class="text-xs text-smoke">{{ msg.email }} · {{ msg.phone || '—' }}</p>
            <p class="mt-2 text-sm">{{ msg.message }}</p>
            <p class="mt-1 text-xs text-smoke">{{ formatDate(msg.created_at, 'fr') }}</p>
          </div>
          <button
            v-if="!msg.is_read"
            type="button"
            class="border-2 border-ink px-3 py-1 text-xs font-bold uppercase"
            @click="markRead(msg.id)"
          >
            Marquer lu
          </button>
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
</script>
