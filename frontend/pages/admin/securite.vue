<template>
  <div>
    <h1 class="font-display text-4xl">Sécurité</h1>
    <p class="mt-2 text-sm text-smoke">
      Protégez l'accès à l'administration avec un code à usage unique (Google Authenticator, Microsoft Authenticator, etc.).
    </p>

    <div v-if="loading" class="mt-8 text-sm text-smoke">Chargement...</div>

    <section v-else-if="status?.enabled" class="card mt-8 space-y-4">
      <h2 class="font-display text-2xl text-green-700">MFA activée</h2>
      <p class="text-sm text-smoke">
        À chaque connexion, un code à 6 chiffres généré par votre application sera demandé en plus du mot de passe.
      </p>

      <form class="space-y-4 border-t-2 border-ink pt-6" @submit.prevent="onDisable">
        <h3 class="font-display text-xl">Désactiver la MFA</h3>
        <AdminField v-model="disablePassword" label="Mot de passe" type="password" />
        <label class="block">
          <span class="text-xs font-bold uppercase tracking-street">Code MFA actuel</span>
          <input
            v-model="disableCode"
            type="text"
            inputmode="numeric"
            maxlength="6"
            required
            class="mt-2 w-full border-2 border-ink px-3 py-2 text-center tracking-[0.3em]"
            placeholder="000000"
          >
        </label>
        <p v-if="message" class="text-sm font-bold text-green-700">{{ message }}</p>
        <p v-if="error" class="text-sm font-bold text-red-600">{{ error }}</p>
        <button type="submit" class="border-2 border-red-600 px-4 py-2 text-xs font-bold uppercase text-red-600" :disabled="saving">
          Désactiver la MFA
        </button>
      </form>
    </section>

    <section v-else class="card mt-8 space-y-6">
      <div>
        <h2 class="font-display text-2xl">Authentification à deux facteurs</h2>
        <p class="mt-2 text-sm text-smoke">
          Scannez un QR code avec votre téléphone pour enregistrer le compte dans une application TOTP.
        </p>
      </div>

      <button v-if="!setup" type="button" class="btn-primary" :disabled="saving" @click="startSetup">
        {{ saving ? 'Préparation...' : 'Configurer la MFA' }}
      </button>

      <div v-if="setup" class="space-y-6 border-t-2 border-ink pt-6">
        <div class="grid gap-8 lg:grid-cols-2">
          <div>
            <p class="text-xs font-bold uppercase tracking-street">1. Scanner le QR code</p>
            <img :src="setup.qr_code" alt="QR code MFA" class="mt-4 max-w-[220px] border-2 border-ink bg-white p-2">
          </div>
          <div>
            <p class="text-xs font-bold uppercase tracking-street">Ou saisir la clé manuellement</p>
            <p class="mt-4 break-all border-2 border-ink bg-chalk px-3 py-2 font-mono text-sm">{{ setup.secret }}</p>
            <p class="mt-4 text-xs text-smoke">
              Application : Google Authenticator, Microsoft Authenticator, Authy, etc.
            </p>
          </div>
        </div>

        <form class="space-y-4" @submit.prevent="onEnable">
          <p class="text-xs font-bold uppercase tracking-street">2. Confirmer avec un code à 6 chiffres</p>
          <input
            v-model="enableCode"
            type="text"
            inputmode="numeric"
            maxlength="6"
            required
            class="w-full max-w-xs border-2 border-ink px-3 py-2 text-center text-2xl tracking-[0.4em]"
            placeholder="000000"
          >
          <p v-if="message" class="text-sm font-bold text-green-700">{{ message }}</p>
          <p v-if="error" class="text-sm font-bold text-red-600">{{ error }}</p>
          <div class="flex flex-wrap gap-3">
            <button type="submit" class="btn-primary" :disabled="saving">
              {{ saving ? 'Activation...' : 'Activer la MFA' }}
            </button>
            <button type="button" class="border-2 border-ink px-4 py-2 text-xs font-bold uppercase" @click="cancelSetup">
              Annuler
            </button>
          </div>
        </form>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import type { AdminMfaSetupResult } from '~/composables/useAdminAuth'
import { formatAdminError } from '~/composables/useAssetUrl'

definePageMeta({ layout: 'admin', middleware: 'admin-auth' })

const { fetchMfaStatus, setupMfa, enableMfa, disableMfa } = useAdminAuth()

const loading = ref(true)
const saving = ref(false)
const status = ref<{ enabled: boolean, pending_setup: boolean } | null>(null)
const setup = ref<AdminMfaSetupResult | null>(null)
const enableCode = ref('')
const disablePassword = ref('')
const disableCode = ref('')
const message = ref('')
const error = ref('')

onMounted(load)

async function load() {
  loading.value = true
  try {
    status.value = await fetchMfaStatus()
  } finally {
    loading.value = false
  }
}

async function startSetup() {
  saving.value = true
  message.value = ''
  error.value = ''
  try {
    setup.value = await setupMfa()
    enableCode.value = ''
  } catch (err) {
    error.value = formatAdminError(err)
  } finally {
    saving.value = false
  }
}

function cancelSetup() {
  setup.value = null
  enableCode.value = ''
  error.value = ''
}

async function onEnable() {
  if (!setup.value) return
  saving.value = true
  message.value = ''
  error.value = ''
  try {
    await enableMfa(enableCode.value.trim())
    message.value = 'MFA activée avec succès.'
    setup.value = null
    await load()
  } catch (err) {
    error.value = formatAdminError(err)
  } finally {
    saving.value = false
  }
}

async function onDisable() {
  saving.value = true
  message.value = ''
  error.value = ''
  try {
    await disableMfa(disablePassword.value, disableCode.value.trim())
    message.value = 'MFA désactivée.'
    disablePassword.value = ''
    disableCode.value = ''
    await load()
  } catch (err) {
    error.value = formatAdminError(err)
  } finally {
    saving.value = false
  }
}
</script>
