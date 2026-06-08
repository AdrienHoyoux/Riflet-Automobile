/** Textes par défaut du site (utilisés si le champ admin est vide). */
export const ADMIN_DEFAULTS = {
  homeServices: {
    title: { fr: 'Nos services', de: 'Unsere Dienstleistungen', nl: 'Onze diensten' },
    subtitle: {
      fr: 'Entretien, réparation et vente de véhicules toutes marques à Malmedy.',
      de: 'Wartung, Reparatur und Fahrzeugverkauf aller Marken in Malmedy.',
      nl: 'Onderhoud, reparatie en verkoop van voertuigen alle merken in Malmedy.',
    },
  },
  homeWhy: {
    title: { fr: 'Pourquoi nous choisir ?', de: 'Warum uns wählen?', nl: 'Waarom voor ons kiezen?' },
  },
  aboutPage: {
    title: { fr: 'À propos', de: 'Über uns', nl: 'Over ons' },
    subtitle: {
      fr: 'Découvrez Riflet Automobile, votre garage toutes marques à Malmedy.',
      de: 'Entdecken Sie Riflet Automobile, Ihre markenunabhängige Werkstatt in Malmedy.',
      nl: 'Ontdek Riflet Automobile, uw garage alle merken in Malmedy.',
    },
  },
  servicesPage: {
    title: { fr: 'Nos services', de: 'Unsere Dienstleistungen', nl: 'Onze diensten' },
    subtitle: {
      fr: 'Des prestations complètes pour votre véhicule toutes marques, particuliers et professionnels.',
      de: 'Umfassende Leistungen für Ihr Fahrzeug aller Marken, für Privat- und Geschäftskunden.',
      nl: 'Volledige diensten voor uw voertuig alle merken, particulieren en professionals.',
    },
  },
} as const

export type AdminLocale = 'fr' | 'de' | 'nl'

export function adminFieldValue(value: string | undefined | null, fallback: string): string {
  return value?.trim() || fallback
}

export function pickLocaleText(
  record: Record<AdminLocale, string>,
  locale: AdminLocale,
): string {
  return record[locale] || record.fr
}
