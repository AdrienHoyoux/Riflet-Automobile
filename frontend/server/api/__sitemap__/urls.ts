interface Paginated<T> {
  results: T[]
  next: string | null
}

function staticRoutes(): string[] {
  const pages = ['', '/services', '/actualites', '/a-propos', '/contact', '/vehicules']
  const prefixes = ['', '/de', '/nl']
  const routes: string[] = []

  for (const prefix of prefixes) {
    for (const page of pages) {
      if (!prefix && !page) routes.push('/')
      else if (!prefix) routes.push(page)
      else routes.push(page ? `${prefix}${page}` : prefix)
    }
  }

  return routes
}

function localizedSlugRoutes(base: string, slug: string): string[] {
  return [
    `${base}/${slug}`,
    `/de${base}/${slug}`,
    `/nl${base}/${slug}`,
  ]
}

async function fetchAllSlugs(apiBase: string, endpoint: string): Promise<string[]> {
  const url = `${apiBase}${endpoint}?page_size=200`
  const data = await $fetch<Paginated<{ slug: string }> | Array<{ slug: string }>>(url)
  const items = Array.isArray(data) ? data : data.results ?? []
  return items.map(item => item.slug).filter(Boolean)
}

export default defineEventHandler(async () => {
  const config = useRuntimeConfig()
  const apiBase = String(config.apiBaseServer || config.public.apiBase).replace(/\/$/, '')
  const routes = staticRoutes()

  try {
    const [newsSlugs, vehicleSlugs] = await Promise.all([
      fetchAllSlugs(apiBase, '/api/news/'),
      fetchAllSlugs(apiBase, '/api/vehicles/'),
    ])

    const articles = newsSlugs.flatMap(slug => localizedSlugRoutes('/actualites', slug))
    const vehicles = vehicleSlugs.flatMap(slug => localizedSlugRoutes('/vehicules', slug))

    return [...routes, ...articles, ...vehicles]
  } catch {
    return routes
  }
})
