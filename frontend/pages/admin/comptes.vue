<template>
  <div>
    <div class="flex flex-wrap items-center justify-between gap-4">
      <div>
        <h1 class="font-display text-4xl">Comptes administrateurs</h1>
        <p class="mt-2 text-sm text-smoke">Ajoutez ou supprimez les accès à l'interface d'administration.</p>
      </div>
      <button type="button" class="btn-primary" @click="showForm = !showForm">
        {{ showForm ? 'Annuler' : 'Ajouter un compte' }}
      </button>
    </div>

    <form v-if="showForm" class="card mt-8 space-y-4" @submit.prevent="createUser">
      <h2 class="font-display text-2xl">Nouveau compte</h2>
      <AdminField v-model="newUser.username" label="Identifiant" />
      <AdminField v-model="newUser.email" label="E-mail" type="email" />
      <AdminField v-model="newUser.password" label="Mot de passe (min. 8 caractères)" type="password" />
      <p class="text-xs text-smoke">
        Le compte pourra se connecter sur `/admin/login` et configurer la MFA dans Sécurité.
      </p>
      <p v-if="error" class="text-sm font-bold text-red-600">{{ error }}</p>
      <button type="submit" class="btn-primary" :disabled="saving">
        {{ saving ? 'Création...' : 'Créer le compte' }}
      </button>
    </form>

    <ul class="mt-8 space-y-3">
      <li v-for="account in users" :key="account.id" class="card flex flex-wrap items-center justify-between gap-4 !p-4">
        <div>
          <p class="font-display text-xl">{{ account.username }}</p>
          <p class="text-sm text-smoke">{{ account.email || '—' }}</p>
          <p class="mt-1 text-xs text-smoke">
            <span v-if="account.is_superuser">Administrateur principal · </span>
            <span v-if="account.mfa_enabled">MFA activée · </span>
            <span v-else>MFA non configurée · </span>
            <span v-if="account.is_current_user">(vous)</span>
          </p>
        </div>
        <button
          v-if="canDelete(account)"
          type="button"
          class="border-2 border-red-600 px-3 py-1 text-xs font-bold uppercase text-red-600"
          @click="removeUser(account)"
        >
          Supprimer
        </button>
        <span v-else class="text-xs font-bold uppercase tracking-street text-smoke">Protégé</span>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { formatAdminError } from '~/composables/useAssetUrl'

definePageMeta({ layout: 'admin', middleware: 'admin-auth' })

interface AdminAccount {
  id: number
  username: string
  email: string
  is_superuser: boolean
  mfa_enabled: boolean
  is_current_user: boolean
  date_joined: string
  last_login: string | null
}

const users = ref<AdminAccount[]>([])
const currentUserId = ref<number | null>(null)
const showForm = ref(false)
const saving = ref(false)
const error = ref('')

const newUser = ref({
  username: '',
  email: '',
  password: '',
})

onMounted(load)

async function load() {
  const [list, me] = await Promise.all([
    adminFetch<AdminAccount[]>('users/'),
    adminFetch<{ id: number }>('me/'),
  ])
  users.value = list
  currentUserId.value = me.id
}

function canDelete(account: AdminAccount) {
  if (account.is_current_user) return false
  if (account.is_superuser) return false
  return true
}

async function createUser() {
  saving.value = true
  error.value = ''
  try {
    await adminFetch('users/', {
      method: 'POST',
      body: {
        username: newUser.value.username.trim(),
        email: newUser.value.email.trim(),
        password: newUser.value.password,
      },
    })
    newUser.value = { username: '', email: '', password: '' }
    showForm.value = false
    await load()
  } catch (err) {
    error.value = formatAdminError(err)
  } finally {
    saving.value = false
  }
}

async function removeUser(account: AdminAccount) {
  if (!confirm(`Supprimer le compte « ${account.username} » ? Cette action est irréversible.`)) return
  try {
    await adminFetch(`users/${account.id}/`, { method: 'DELETE' })
    await load()
  } catch (err) {
    alert(formatAdminError(err))
  }
}
</script>
