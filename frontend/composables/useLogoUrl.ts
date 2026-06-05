import type { SiteSettings } from '~/types/api'
import { resolveImageUrl } from '~/composables/useAssetUrl'
import { LOGO_URL } from '~/utils/images'

export function useLogoUrl(settings?: Ref<SiteSettings | null> | SiteSettings | null) {
  return computed(() => {
    const value = settings && 'value' in settings ? settings.value : settings
    const url = value?.logo_url || LOGO_URL
    return resolveImageUrl(url)
  })
}
