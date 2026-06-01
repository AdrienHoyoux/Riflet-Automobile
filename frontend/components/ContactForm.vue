<template>
  <form class="space-y-5" novalidate @submit.prevent="handleSubmit">
    <div class="grid gap-5 sm:grid-cols-2">
      <div>
        <label for="name" class="mb-2 block text-[10px] font-bold uppercase tracking-street text-ink">
          {{ $t('contact.form.name') }} *
        </label>
        <input
          id="name"
          v-model="form.name"
          type="text"
          required
          class="input-field"
        >
      </div>
      <div>
        <label for="email" class="mb-2 block text-[10px] font-bold uppercase tracking-street text-ink">
          {{ $t('contact.form.email') }} *
        </label>
        <input
          id="email"
          v-model="form.email"
          type="email"
          required
          class="input-field"
        >
      </div>
    </div>

    <div>
      <label for="phone" class="mb-2 block text-[10px] font-bold uppercase tracking-street text-ink">
        {{ $t('contact.form.phone') }}
      </label>
      <input
        id="phone"
        v-model="form.phone"
        type="tel"
        :pattern="phonePattern"
        class="input-field"
      >
    </div>

    <div>
      <label for="subject" class="mb-2 block text-[10px] font-bold uppercase tracking-street text-ink">
        {{ $t('contact.form.subject') }} *
      </label>
      <input
        id="subject"
        v-model="form.subject"
        type="text"
        required
        class="input-field"
      >
    </div>

    <div>
      <label for="message" class="mb-2 block text-[10px] font-bold uppercase tracking-street text-ink">
        {{ $t('contact.form.message') }} *
      </label>
      <textarea
        id="message"
        v-model="form.message"
        required
        rows="5"
        minlength="10"
        class="input-field resize-y"
      />
    </div>

    <div v-if="successMessage" class="border-2 border-ink bg-acid px-4 py-3 text-sm font-medium text-ink">
      {{ successMessage }}
    </div>
    <div v-if="errorMessage" class="border-2 border-ink bg-ink px-4 py-3 text-sm font-medium text-chalk">
      {{ errorMessage }}
    </div>

    <button
      type="submit"
      class="btn-primary w-full sm:w-auto"
      :disabled="loading"
    >
      {{ loading ? $t('contact.form.sending') : $t('contact.form.submit') }}
    </button>
  </form>
</template>

<script setup lang="ts">
import type { ContactFormData } from '~/types/api'
import { formatApiErrors } from '~/utils/formErrors'
import { isValidPhone, PHONE_REGEX } from '~/utils/phone'

const { t } = useI18n()
const loading = ref(false)
const successMessage = ref('')
const errorMessage = ref('')

const phonePattern = PHONE_REGEX.source

const form = reactive<ContactFormData>({
  name: '',
  email: '',
  phone: '',
  subject: '',
  message: '',
})

const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

function validateForm(): string | null {
  if (!form.name.trim()) {
    return t('contact.form.nameRequired')
  }
  if (!form.email.trim()) {
    return t('contact.form.emailRequired')
  }
  if (!EMAIL_REGEX.test(form.email.trim())) {
    return t('contact.form.emailInvalid')
  }
  if (!isValidPhone(form.phone)) {
    return t('contact.form.phoneInvalid')
  }
  if (!form.subject.trim()) {
    return t('contact.form.subjectRequired')
  }
  if (form.message.trim().length < 10) {
    return t('contact.form.messageTooShort')
  }
  return null
}

function getSubmitErrorMessage(err: unknown): string {
  const fetchErr = err as {
    message?: string
    statusCode?: number
    data?: unknown
  }

  const fromBody = formatApiErrors(fetchErr.data)
  if (fromBody) {
    return fromBody
  }

  if (typeof fetchErr.message === 'string' && fetchErr.message.trim()) {
    return fetchErr.message
  }

  if (fetchErr.statusCode && fetchErr.statusCode >= 500) {
    return t('contact.form.serverError')
  }

  return t('contact.form.error')
}

async function handleSubmit() {
  loading.value = true
  successMessage.value = ''
  errorMessage.value = ''

  const validationError = validateForm()
  if (validationError) {
    errorMessage.value = validationError
    loading.value = false
    return
  }

  try {
    await submitContact(form)
    successMessage.value = t('contact.form.success')
    form.name = ''
    form.email = ''
    form.phone = ''
    form.subject = ''
    form.message = ''
  } catch (err: unknown) {
    errorMessage.value = getSubmitErrorMessage(err)
  } finally {
    loading.value = false
  }
}
</script>
