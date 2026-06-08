export function resolveImageUrl(url: string | null | undefined): string {
  if (!url) return ''

  const trimmed = url.trim()
  if (!trimmed) return ''

  const config = useRuntimeConfig()
  const mediaPath = trimmed.startsWith('/media/')
    ? trimmed
    : trimmed.match(/\/media\/[^\s?#]+/)?.[0]

  if (mediaPath) {
    const siteUrl = (config.public.siteUrl as string).replace(/\/$/, '')
    const isLocalDev = siteUrl.includes('localhost') || siteUrl.includes('127.0.0.1')
    if (isLocalDev) {
      return `${useApiBase()}${mediaPath}`
    }
    return `${siteUrl}${mediaPath}`
  }

  if (trimmed.startsWith('http://') || trimmed.startsWith('https://')) {
    return trimmed
  }

  return `${config.public.siteUrl}${trimmed.startsWith('/') ? trimmed : `/${trimmed}`}`
}

/** Extrait un chemin /media/... depuis une URL absolue ou relative. */
export function imageUrlFromPreview(preview: string | null | undefined, stored?: string | null): string {
  if (stored?.trim()) return stored
  return normalizeImageUrlForStorage(preview)
}

/** Prépare une URL image pour l'enregistrement (chemins /media/... conservés). */
export function normalizeImageUrlForStorage(url: string | null | undefined): string {
  if (!url) return ''
  const trimmed = url.trim()
  if (!trimmed) return ''

  const mediaMatch = trimmed.match(/\/media\/[^\s?#]+/)
  if (mediaMatch) return mediaMatch[0]

  if (trimmed.startsWith('http://') || trimmed.startsWith('https://')) return trimmed
  return trimmed.startsWith('/') ? trimmed : `/${trimmed}`
}

export function formatAdminError(error: unknown): string {
  const payload = (error as { data?: unknown })?.data
  if (!payload) return 'Une erreur est survenue.'
  if (typeof payload === 'string') return payload
  if (typeof payload === 'object' && payload !== null) {
    const record = payload as Record<string, unknown>
    if (typeof record.detail === 'string') return record.detail
    return Object.entries(record)
      .map(([key, value]) => {
        if (Array.isArray(value)) return `${key}: ${value.join(', ')}`
        return `${key}: ${String(value)}`
      })
      .join(' · ')
  }
  return 'Une erreur est survenue.'
}
