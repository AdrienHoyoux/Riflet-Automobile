export default defineEventHandler(async () => {
  const config = useRuntimeConfig()
  const apiBase = config.apiBaseServer || config.public.apiBase

  const staticPages = [
    '/',
    '/services',
    '/actualites',
    '/a-propos',
    '/contact',
    '/de',
    '/de/services',
    '/de/actualites',
    '/de/a-propos',
    '/de/contact',
    '/nl',
    '/nl/services',
    '/nl/actualites',
    '/nl/a-propos',
    '/nl/contact',
  ]

  try {
    const news = await $fetch<Array<{ slug: string }>>(`${apiBase}/api/news/`)
    const articles = news.flatMap((article) => [
      `/actualites/${article.slug}`,
      `/de/actualites/${article.slug}`,
      `/nl/actualites/${article.slug}`,
    ])
    return [...staticPages, ...articles]
  } catch {
    return staticPages
  }
})
