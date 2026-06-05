export default defineNuxtRouteMiddleware(async (to) => {
  const loginPath = '/admin/login'

  if (to.path === loginPath) {
    return
  }

  if (!to.path.startsWith('/admin')) {
    return
  }

  const { checkSession } = useAdminAuth()
  const ok = await checkSession()
  if (!ok) {
    return navigateTo(loginPath)
  }
})
