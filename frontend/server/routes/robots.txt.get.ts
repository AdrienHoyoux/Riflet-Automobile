/** robots.txt dynamique — URL sitemap en prod (plus de localhost). */
export default defineEventHandler(() => {
  const config = useRuntimeConfig()
  const siteUrl = String(config.public.siteUrl || 'http://localhost:3000').replace(/\/$/, '')

  const lines = [
    'User-agent: *',
    'Allow: /',
    'Disallow: /admin',
    'Disallow: /admin/',
    '',
    `Sitemap: ${siteUrl}/sitemap.xml`,
  ]

  return lines.join('\n')
})
