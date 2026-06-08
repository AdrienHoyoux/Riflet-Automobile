import type { SiteSettings } from '~/types/api'
import { formatAdminError, normalizeImageUrlForStorage } from '~/composables/useAssetUrl'

export function useAdminSettingsForm() {
  const form = ref<SiteSettings | null>(null)
  const saving = ref(false)
  const message = ref('')
  const error = ref('')

  async function loadSettings() {
    form.value = await adminFetch<SiteSettings>('settings/')
  }

  async function saveSettings() {
    if (!form.value) return false

    saving.value = true
    message.value = ''
    error.value = ''

    try {
      form.value = await adminFetch<SiteSettings>('settings/', {
        method: 'PATCH',
        body: {
          ...form.value,
          logo_url: normalizeImageUrlForStorage(form.value.logo_url),
          hero_image_url: normalizeImageUrlForStorage(form.value.hero_image_url),
          about_image_url: normalizeImageUrlForStorage(form.value.about_image_url),
        },
      })
      message.value = 'Modifications enregistrées.'
      return true
    } catch (err) {
      error.value = formatAdminError(err)
      return false
    } finally {
      saving.value = false
    }
  }

  return {
    form,
    saving,
    message,
    error,
    loadSettings,
    saveSettings,
  }
}
