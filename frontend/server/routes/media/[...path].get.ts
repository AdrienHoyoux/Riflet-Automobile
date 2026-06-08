/** Proxy /media/* vers Django (si Traefik envoie la requête au conteneur Nuxt). */
export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig()
  const pathParam = getRouterParam(event, 'path')
  const subPath = Array.isArray(pathParam) ? pathParam.join('/') : (pathParam || '')
  const backend = String(config.apiBaseServer || 'http://backend:8000').replace(/\/$/, '')
  const target = `${backend}/media/${subPath}`

  return proxyRequest(event, target)
})
