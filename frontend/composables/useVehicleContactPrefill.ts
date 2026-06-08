import type { UsedVehicle } from '~/types/api'

export function useVehicleContactPrefill() {
  const route = useRoute()
  const { t, locale } = useI18n()
  const config = useRuntimeConfig()
  const localePath = useLocalePath()

  const vehicleSlug = computed(() => {
    const value = route.query.vehicule
    return typeof value === 'string' ? value.trim() : ''
  })

  const vehicle = ref<UsedVehicle | null>(null)
  const vehicleSold = ref(false)
  const loading = ref(false)

  watch(
    vehicleSlug,
    async (slug) => {
      vehicle.value = null
      vehicleSold.value = false

      if (!slug) return

      loading.value = true
      try {
        const data = await fetchVehicle(slug)
        if (data.is_sold) {
          vehicleSold.value = true
          return
        }
        vehicle.value = data
      } catch {
        vehicle.value = null
      } finally {
        loading.value = false
      }
    },
    { immediate: true },
  )

  function buildPrefill(source: UsedVehicle) {
    const title = getLocalizedField(source, 'title', locale.value)
    const numberLocale = locale.value === 'fr' ? 'fr-BE' : locale.value === 'de' ? 'de-BE' : 'nl-BE'
    const mileage = `${new Intl.NumberFormat(numberLocale).format(source.mileage)} km`
    const price = new Intl.NumberFormat(numberLocale, {
      style: 'currency',
      currency: 'EUR',
      maximumFractionDigits: 0,
    }).format(Number(source.price))
    const fuel = t(`vehicles.fuel.${source.fuel_type}`)
    const url = `${config.public.siteUrl}${localePath(`/vehicules/${source.slug}`)}`

    return {
      subject: t('vehicles.contact_subject', { title }),
      message: t('vehicles.contact_message', {
        title,
        brand: source.brand,
        model: source.model_name,
        year: source.year,
        mileage,
        price,
        fuel,
        slug: source.slug,
        url,
      }),
    }
  }

  return {
    vehicleSlug,
    vehicle,
    vehicleSold,
    loading,
    buildPrefill,
  }
}
