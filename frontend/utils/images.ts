import { resolveImageUrl } from '~/composables/useAssetUrl'

/** Logo officiel Riflet Automobile (photo de profil Facebook) — copie locale stable */
export const LOGO_URL = '/images/riflet-logo.jpg'

const unsplash = (id: string, width = 1200) =>
  `https://images.unsplash.com/${id}?auto=format&fit=crop&w=${width}&q=80`

/** Images Unsplash (licence Unsplash — usage gratuit) */
export const UNSPLASH_IMAGES = {
  /** Parc automobile / véhicules d'occasion */
  usedCars: unsplash('photo-1706609331822-a844b579976a', 900),
  /** Inspection véhicule en atelier */
  technicalInspection: unsplash('photo-1727893467393-24bc37e8a117', 900),
  /** Commandes climatisation automobile */
  airConditioning: unsplash('photo-1773962375418-9f13f00553e7', 900),
  /** Citroën Berlingo utilitaire */
  citroenBerlingo: unsplash('photo-1768389533475-edc8b2bb9c7d', 1200),
} as const

export const VOLVO_IMAGES = {
  /** Volvo V60 blanche — ERIK SETH / Unsplash (licence Unsplash) */
  hero: unsplash('photo-1678120958515-ad620ef2b0c9', 1920),
  about: unsplash('photo-1606664515524-ed2f786a0bd6', 1400),
  newsPrimary: unsplash('photo-1619682817481-e094139ff227', 1200),
  newsSecondary: unsplash('photo-1609521263047-f8f205293f24', 1200),
  services: [
    unsplash('photo-1618843479313-40f8afb4b4d8', 900),
    unsplash('photo-1606664515524-ed2f786a0bd6', 900),
    UNSPLASH_IMAGES.usedCars,
    unsplash('photo-1609521263047-f8f205293f24', 900),
    UNSPLASH_IMAGES.technicalInspection,
    UNSPLASH_IMAGES.airConditioning,
  ],
} as const

/** Image Open Graph par défaut (partages réseaux sociaux) — URL HTTPS stable */
export const OG_DEFAULT_IMAGE = VOLVO_IMAGES.hero

export function getServiceImage(order: number, uploaded?: string | null) {
  if (uploaded) return resolveImageUrl(uploaded)
  const index = Math.max(0, order - 1) % VOLVO_IMAGES.services.length
  return VOLVO_IMAGES.services[index]
}

export function getNewsFallback(index: number) {
  return index % 2 === 0 ? VOLVO_IMAGES.newsPrimary : VOLVO_IMAGES.newsSecondary
}
