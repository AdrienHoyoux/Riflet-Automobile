<template>
  <div class="flex min-h-screen items-center justify-center bg-ink px-4">
    <form class="w-full max-w-md border-2 border-chalk bg-chalk p-8" @submit.prevent="onSubmit">
      <h1 class="font-display text-3xl text-ink">Administration</h1>
      <p class="mt-2 text-sm text-smoke">
        {{ step === 'mfa' ? 'Saisissez le code de votre application d\'authentification.' : 'Connectez-vous pour gérer le site Riflet Automobile.' }}
      </p>

      <template v-if="step === 'credentials'">
        <label class="mt-8 block text-xs font-bold uppercase tracking-street">Identifiant</label>
        <input v-model="username" type="text" required class="mt-2 w-full border-2 border-ink px-3 py-2" autocomplete="username">

        <label class="mt-4 block text-xs font-bold uppercase tracking-street">Mot de passe</label>
        <input v-model="password" type="password" required class="mt-2 w-full border-2 border-ink px-3 py-2" autocomplete="current-password">
      </template>

      <template v-else>
        <p v-if="mfaUsername" class="mt-6 text-sm text-smoke">Compte : <strong class="text-ink">{{ mfaUsername }}</strong></p>

        <label class="mt-6 block text-xs font-bold uppercase tracking-street">Code à 6 chiffres</label>
        <input
          v-model="otpCode"
          type="text"
          inputmode="numeric"
          pattern="[0-9]*"
          maxlength="6"
          required
          class="mt-2 w-full border-2 border-ink px-3 py-2 text-center text-2xl tracking-[0.4em]"
          autocomplete="one-time-code"
          placeholder="000000"
        >

        <button type="button" class="mt-4 text-xs font-bold uppercase tracking-street text-smoke hover:text-ink" @click="backToCredentials">
          ← Retour
        </button>
      </template>

      <p v-if="error" class="mt-4 text-sm text-red-600">{{ error }}</p>

      <button type="submit" class="btn-primary mt-6 w-full justify-center" :disabled="loading">
        {{ loading ? 'Vérification...' : (step === 'mfa' ? 'Valider le code' : 'Se connecter') }}
      </button>
    </form>
  </div>
</template>

<script setup lang="ts">
import { formatAdminError } from '~/composables/useAssetUrl'

definePageMeta({ layout: false })

const { login, verifyMfaLogin, checkSession } = useAdminAuth()

const step = ref<'credentials' | 'mfa'>('credentials')
const username = ref('admin')
const password = ref('')
const otpCode = ref('')
const pendingToken = ref('')
const mfaUsername = ref('')
const error = ref('')
const loading = ref(false)

onMounted(async () => {
  if (await checkSession()) {
    await navigateTo('/admin')
  }
})

function backToCredentials() {
  step.value = 'credentials'
  otpCode.value = ''
  pendingToken.value = ''
  error.value = ''
}

async function onSubmit() {
  error.value = ''
  loading.value = true

  try {
    if (step.value === 'credentials') {
      const result = await login(username.value, password.value)
      if (result.mfaRequired && result.pendingToken) {
        step.value = 'mfa'
        pendingToken.value = result.pendingToken
        mfaUsername.value = result.username || username.value
        otpCode.value = ''
        return
      }
      await navigateTo('/admin')
      return
    }

    await verifyMfaLogin(pendingToken.value, otpCode.value.trim())
    await navigateTo('/admin')
  } catch (err) {
    error.value = formatAdminError(err)
  } finally {
    loading.value = false
  }
}
</script>
