import type {
  ContactFormData,
  CustomerReview,
  NewsArticle,
  PaginatedResponse,
  ReviewSubmitData,
  Service,
  SiteSettings,
  UsedVehicle,
  WhyChooseItem,
} from '~/types/api'
import { OG_DEFAULT_IMAGE } from '~/utils/images'

export function useApiBase() {
  const config = useRuntimeConfig()

  if (import.meta.server) {
    return (config.apiBaseServer || config.public.apiBase) as string
  }

  // Navigateur : si on n'est pas en local, toujours same-origin (/api → Django via Traefik)
  // Même si le build a embarqué localhost:8000 par erreur.
  if (typeof window !== 'undefined') {
    const host = window.location.hostname
    if (host !== 'localhost' && host !== '127.0.0.1') {
      return ''
    }
  }

  return (config.public.apiBase as string) || 'http://localhost:8000'
}

export function getLocalizedField<T extends Record<string, unknown>>(
  item: T,
  field: string,
  lang: string,
) {
  const key = `${field}_${lang}` as keyof T
  const fallback = `${field}_fr` as keyof T
  return (item[key] || item[fallback] || '') as string
}

export function useLocalizedField<T extends Record<string, unknown>>(
  item: T,
  field: string,
  locale?: string,
) {
  const { locale: currentLocale } = useI18n()
  return getLocalizedField(item, field, locale || currentLocale.value)
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

export async function fetchWhyChooseItems() {
  const apiBase = useApiBase()
  return $fetch<WhyChooseItem[]>(`${apiBase}/api/why-items/`)
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

export async function fetchVehicles() {
  const apiBase = useApiBase()
  const data = await $fetch<PaginatedResponse<UsedVehicle> | UsedVehicle[]>(`${apiBase}/api/vehicles/`)
  return Array.isArray(data) ? data : data.results
}

export async function fetchVehicle(slug: string) {
  const apiBase = useApiBase()
  return $fetch<UsedVehicle>(`${apiBase}/api/vehicles/${slug}/`)
}

export async function submitContact(form: ContactFormData) {
  // Même origine → Nitro → backend (Traefik route /api/* vers Django, pas Nuxt)
  return $fetch<{ detail: string }>('/contact/submit', {
    method: 'POST',
    body: form,
  })
}

export async function submitReview(form: ReviewSubmitData) {
  return $fetch<{ detail: string }>('/reviews/submit', {
    method: 'POST',
    body: form,
  })
}

export function useSeoMetaTags(title: string, description: string, image?: string) {
  const config = useRuntimeConfig()
  const siteUrl = (config.public.siteUrl as string).replace(/\/$/, '')
  const route = useRoute()
  const { locale } = useI18n()

  useSeoMeta({
    title,
    description,
    ogTitle: title,
    ogDescription: description,
    ogType: 'website',
    ogUrl: `${siteUrl}${route.fullPath}`,
    ogImage: image || OG_DEFAULT_IMAGE,
    ogLocale: locale.value === 'fr' ? 'fr_BE' : locale.value === 'de' ? 'de_BE' : 'nl_BE',
    twitterCard: 'summary_large_image',
    twitterTitle: title,
    twitterDescription: description,
    twitterImage: image || OG_DEFAULT_IMAGE,
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
