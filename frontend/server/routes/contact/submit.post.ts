import type { ContactFormData } from '~/types/api'
import { formatApiErrors } from '~/utils/formErrors'

/** Proxy vers Django — évite les appels client vers localhost ou CORS en production. */
export default defineEventHandler(async (event) => {
  const body = await readBody<ContactFormData>(event)
  const config = useRuntimeConfig()
  const apiBase = (config.apiBaseServer || config.public.apiBase) as string

  try {
    return await $fetch<{ detail: string }>(`${apiBase}/api/contact/`, {
      method: 'POST',
      body,
    })
  } catch (error: unknown) {
    const fetchError = error as { statusCode?: number; data?: unknown }
    const message =
      formatApiErrors(fetchError.data) ||
      'Impossible d\'envoyer le message. Vérifiez les champs du formulaire.'

    throw createError({
      statusCode: fetchError.statusCode || 502,
      message,
      data: fetchError.data,
    })
  }
})
