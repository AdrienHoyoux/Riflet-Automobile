/** Extrait un message lisible depuis une réponse d'erreur Django REST Framework. */
export function formatApiErrors(data: unknown): string | null {
  if (!data || typeof data !== 'object') {
    return null
  }

  const obj = data as Record<string, unknown>

  if (typeof obj.detail === 'string' && obj.detail.trim()) {
    return obj.detail
  }

  if (Array.isArray(obj.detail)) {
    const parts = obj.detail.map(String).filter(Boolean)
    if (parts.length) {
      return parts.join(' ')
    }
  }

  const messages: string[] = []
  for (const value of Object.values(obj)) {
    if (Array.isArray(value)) {
      messages.push(...value.map(String).filter(Boolean))
    } else if (typeof value === 'string' && value.trim()) {
      messages.push(value)
    }
  }

  return messages.length ? messages.join(' ') : null
}
