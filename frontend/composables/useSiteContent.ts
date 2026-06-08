import type { Ref } from 'vue'
import type { SiteSettings } from '~/types/api'

/** Texte multilingue depuis les paramètres du site, avec repli sur i18n. */
export function useSettingsField(
  settings: Ref<SiteSettings | null | undefined>,
  fieldPrefix: string,
  fallbackKey: string,
) {
  const { locale, t } = useI18n()

  return computed(() => {
    const settingsValue = settings?.value
    if (settingsValue) {
      const key = `${fieldPrefix}_${locale.value}` as keyof SiteSettings
      const value = settingsValue[key]
      if (typeof value === 'string' && value.trim()) {
        return value
      }
    }
    return t(fallbackKey)
  })
}

export function localizedWhyText(
  item: { text_fr: string; text_de?: string; text_nl?: string },
  locale: string,
) {
  const key = `text_${locale}` as 'text_fr' | 'text_de' | 'text_nl'
  return item[key]?.trim() || item.text_fr
}
