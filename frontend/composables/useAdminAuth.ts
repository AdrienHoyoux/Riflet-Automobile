const TOKEN_KEY = 'riflet_admin_token'

export interface AdminLoginResult {
  mfaRequired: boolean
  pendingToken?: string
  username?: string
}

export interface AdminMfaSetupResult {
  secret: string
  qr_code: string
  otpauth_url: string
}

export function useAdminToken() {
  return useState<string | null>('adminToken', () => {
    if (import.meta.client) {
      return localStorage.getItem(TOKEN_KEY)
    }
    return null
  })
}

export function useAdminAuth() {
  const token = useAdminToken()
  const username = useState<string | null>('adminUsername', () => null)
  const mfaEnabled = useState<boolean>('adminMfaEnabled', () => false)

  function saveSession(newToken: string, newUsername: string, isMfaEnabled = false) {
    token.value = newToken
    username.value = newUsername
    mfaEnabled.value = isMfaEnabled
    if (import.meta.client) {
      localStorage.setItem(TOKEN_KEY, newToken)
    }
  }

  function clearSession() {
    token.value = null
    username.value = null
    mfaEnabled.value = false
    if (import.meta.client) {
      localStorage.removeItem(TOKEN_KEY)
    }
  }

  function authHeaders(): HeadersInit {
    if (!token.value) return {}
    return { Authorization: `Token ${token.value}` }
  }

  async function login(user: string, password: string): Promise<AdminLoginResult> {
    const apiBase = useApiBase()
    const data = await $fetch<{
      token?: string
      username?: string
      mfa_required?: boolean
      pending_token?: string
      mfa_enabled?: boolean
    }>(`${apiBase}/api/admin/login/`, {
      method: 'POST',
      body: { username: user, password },
    })

    if (data.mfa_required && data.pending_token) {
      return {
        mfaRequired: true,
        pendingToken: data.pending_token,
        username: data.username,
      }
    }

    if (data.token && data.username) {
      saveSession(data.token, data.username, Boolean(data.mfa_enabled))
      return { mfaRequired: false }
    }

    throw new Error('Connexion impossible.')
  }

  async function verifyMfaLogin(pendingToken: string, code: string) {
    const apiBase = useApiBase()
    const data = await $fetch<{ token: string, username: string }>(`${apiBase}/api/admin/login/mfa/`, {
      method: 'POST',
      body: { pending_token: pendingToken, code },
    })
    saveSession(data.token, data.username, true)
    return data
  }

  async function logout() {
    const apiBase = useApiBase()
    try {
      if (token.value) {
        await $fetch(`${apiBase}/api/admin/logout/`, {
          method: 'POST',
          headers: authHeaders(),
        })
      }
    } finally {
      clearSession()
    }
  }

  async function checkSession() {
    if (!token.value) return false
    const apiBase = useApiBase()
    try {
      const data = await $fetch<{ username: string, mfa_enabled?: boolean }>(`${apiBase}/api/admin/me/`, {
        headers: authHeaders(),
      })
      username.value = data.username
      mfaEnabled.value = Boolean(data.mfa_enabled)
      return true
    } catch {
      clearSession()
      return false
    }
  }

  async function fetchMfaStatus() {
    return adminFetch<{ enabled: boolean, pending_setup: boolean }>('mfa/status/')
  }

  async function setupMfa() {
    return adminFetch<AdminMfaSetupResult>('mfa/setup/', { method: 'POST' })
  }

  async function enableMfa(code: string) {
    return adminFetch<{ detail: string, enabled: boolean }>('mfa/enable/', {
      method: 'POST',
      body: { code },
    })
  }

  async function disableMfa(password: string, code: string) {
    return adminFetch<{ detail: string, enabled: boolean }>('mfa/disable/', {
      method: 'POST',
      body: { password, code },
    })
  }

  return {
    token,
    username,
    mfaEnabled,
    authHeaders,
    login,
    verifyMfaLogin,
    logout,
    checkSession,
    clearSession,
    fetchMfaStatus,
    setupMfa,
    enableMfa,
    disableMfa,
  }
}

export async function adminFetch<T>(path: string, options: {
  method?: string
  body?: unknown
} = {}) {
  const apiBase = useApiBase()
  const { authHeaders } = useAdminAuth()
  return $fetch<T>(`${apiBase}/api/admin/${path}`, {
    method: (options.method || 'GET') as 'GET' | 'POST' | 'PATCH' | 'DELETE',
    body: options.body,
    headers: authHeaders(),
  })
}

export async function adminUpload(
  file: File,
  folder: 'settings' | 'news' | 'vehicles' | 'services' = 'settings',
) {
  const apiBase = useApiBase()
  const { authHeaders } = useAdminAuth()
  const formData = new FormData()
  formData.append('file', file)
  formData.append('folder', folder)

  return $fetch<{ url: string, absolute_url: string }>(`${apiBase}/api/admin/upload/`, {
    method: 'POST',
    body: formData,
    headers: authHeaders(),
  })
}
