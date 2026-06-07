export function resolveImageUrl(url: string | null | undefined): string {
  if (!url) return ''
  if (url.startsWith('http://') || url.startsWith('https://')) return url

  const config = useRuntimeConfig()
  if (url.startsWith('/media/')) {
    const base = import.meta.server
      ? ((config.apiBaseServer || config.public.apiBase) as string)
      : (() => {
          const publicBase = (config.public.apiBase as string) || ''
          if (publicBase.includes('localhost') || publicBase.includes('127.0.0.1')) {
            return publicBase
          }
          return ''
        })()
    return `${base}${url}`
  }

  return `${config.public.siteUrl}${url}`
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
