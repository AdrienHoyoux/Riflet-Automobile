export interface SiteSettings {
  company_name: string
  tagline_fr: string
  tagline_de: string
  tagline_nl: string
  about_fr: string
  about_de: string
  about_nl: string
  about_title_fr: string
  about_title_de: string
  about_title_nl: string
  about_subtitle_fr: string
  about_subtitle_de: string
  about_subtitle_nl: string
  about_image_url: string
  home_services_title_fr: string
  home_services_title_de: string
  home_services_title_nl: string
  home_services_subtitle_fr: string
  home_services_subtitle_de: string
  home_services_subtitle_nl: string
  home_why_title_fr: string
  home_why_title_de: string
  home_why_title_nl: string
  services_title_fr: string
  services_title_de: string
  services_title_nl: string
  services_subtitle_fr: string
  services_subtitle_de: string
  services_subtitle_nl: string
  address: string
  city: string
  postal_code: string
  country: string
  phone: string
  email: string
  facebook_url: string
  monday_hours: string
  tuesday_hours: string
  wednesday_hours: string
  thursday_hours: string
  friday_hours: string
  saturday_hours: string
  sunday_hours: string
  latitude: string | null
  longitude: string | null
  logo_url: string
  hero_image_url: string
  google_rating: string | number
  google_review_count: number
  google_maps_url: string
}

export interface CustomerReview {
  id: number
  author_name: string
  rating: number
  content: string
  source: string
  review_date: string | null
  order: number
}

export interface WhyChooseItem {
  id: number
  text_fr: string
  text_de: string
  text_nl: string
  order: number
  is_active?: boolean
}

export interface Service {
  id: number
  title_fr: string
  title_de: string
  title_nl: string
  description_fr: string
  description_de: string
  description_nl: string
  icon: string
  image: string | null
  order: number
}

export interface NewsArticle {
  id: number
  slug: string
  title_fr: string
  title_de: string
  title_nl: string
  description_fr: string
  description_de: string
  description_nl: string
  content_fr?: string
  content_de?: string
  content_nl?: string
  image: string | null
  published_at: string
}

export interface PaginatedResponse<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

export interface UsedVehicle {
  id: number
  slug: string
  brand: string
  model_name: string
  year: number
  mileage: number
  fuel_type: string
  transmission: string
  price: string | number
  title_fr: string
  title_de: string
  title_nl: string
  description_fr: string
  description_de: string
  description_nl: string
  image: string | null
  images?: string[]
  is_sold: boolean
  order: number
}

export interface ContactFormData {
  name: string
  email: string
  phone: string
  subject: string
  message: string
  vehicle_slug?: string
}

export interface ContactMessageVehicle {
  id: number
  slug: string
  title_fr: string
  brand: string
  model_name: string
  year: number
  is_sold: boolean
}

export interface ReviewSubmitData {
  author_name: string
  rating: number
  content: string
  company?: string
}
