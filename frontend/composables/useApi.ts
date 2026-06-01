import type {
  ContactFormData,
  CustomerReview,
  NewsArticle,
  PaginatedResponse,
  Service,
  SiteSettings,
} from '~/types/api'

export function useApiBase() {
  const config = useRuntimeConfig()
  if (import.meta.server) {
    return (config.apiBaseServer || config.public.apiBase) as string
  }
  return config.public.apiBase as string
}

export function useLocalizedField<T extends Record<string, unknown>>(
  item: T,
  field: string,
  locale?: string,
) {
  const { locale: currentLocale } = useI18n()
  const lang = locale || currentLocale.value
  const key = `${field}_${lang}` as keyof T
  const fallback = `${field}_fr` as keyof T
  return (item[key] || item[fallback] || '') as string
}

export async function fetchSettings() {
  const apiBase = useApiBase()
  return $fetch<SiteSettings>(`${apiBase}/api/settings/`)
}

export async function fetchServices() {
  const apiBase = useApiBase()
  const data = await $fetch<PaginatedResponse<Service> | Service[]>(`${apiBase}/api/services/`)
  return Array.isArray(data) ? data : data.results
}

export async function fetchNews() {
  const apiBase = useApiBase()
  const data = await $fetch<PaginatedResponse<NewsArticle> | NewsArticle[]>(`${apiBase}/api/news/`)
  return Array.isArray(data) ? data : data.results
}

export async function fetchNewsArticle(slug: string) {
  const apiBase = useApiBase()
  return $fetch<NewsArticle>(`${apiBase}/api/news/${slug}/`)
}

export async function fetchReviews() {
  const apiBase = useApiBase()
  const data = await $fetch<PaginatedResponse<CustomerReview> | CustomerReview[]>(`${apiBase}/api/reviews/`)
  return Array.isArray(data) ? data : data.results
}

export async function submitContact(form: ContactFormData) {
  // Même origine → Nitro → backend (Traefik route /api/* vers Django, pas Nuxt)
  return $fetch<{ detail: string }>('/contact/submit', {
    method: 'POST',
    body: form,
  })
}

export function useSeoMetaTags(title: string, description: string, image?: string) {
  const config = useRuntimeConfig()
  const siteUrl = config.public.siteUrl as string
  const { locale } = useI18n()

  useSeoMeta({
    title,
    description,
    ogTitle: title,
    ogDescription: description,
    ogImage: image || `${siteUrl}/og-default.jpg`,
    ogLocale: locale.value === 'fr' ? 'fr_BE' : locale.value === 'de' ? 'de_BE' : 'nl_BE',
    twitterCard: 'summary_large_image',
    twitterTitle: title,
    twitterDescription: description,
  })

  useHead({
    link: [
      { rel: 'canonical', href: `${siteUrl}${useRoute().fullPath}` },
    ],
  })
}

export function formatDate(dateString: string, locale: string) {
  return new Date(dateString).toLocaleDateString(
    locale === 'fr' ? 'fr-BE' : locale === 'de' ? 'de-BE' : 'nl-BE',
    { day: 'numeric', month: 'long', year: 'numeric' },
  )
}

export function phoneHref(phone: string) {
  return `tel:${phone.replace(/\s/g, '')}`
}
