import type { SiteSettings } from '~/types/api'
import { LOGO_URL } from '~/utils/images'

export function useLogoUrl(settings?: Ref<SiteSettings | null> | SiteSettings | null) {
  const config = useRuntimeConfig()

  return computed(() => {
    const value = settings && 'value' in settings ? settings.value : settings
    const url = value?.logo_url || LOGO_URL
    if (url.startsWith('/')) {
      return `${config.public.siteUrl}${url}`
    }
    return url
  })
}
