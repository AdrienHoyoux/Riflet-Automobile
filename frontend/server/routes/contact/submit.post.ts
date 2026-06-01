import type { ContactFormData } from '~/types/api'

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
    const fetchError = error as { statusCode?: number; data?: { detail?: string } }
    throw createError({
      statusCode: fetchError.statusCode || 502,
      message: fetchError.data?.detail || 'Impossible d\'envoyer le message.',
    })
  }
})
