<template>
  <div class="min-h-screen bg-chalk text-ink">
    <header class="border-b-2 border-ink bg-ink text-chalk">
      <div class="container-custom flex h-16 items-center justify-between">
        <div>
          <p class="font-display text-xl tracking-wide">RIFLET — Administration</p>
          <p v-if="username" class="text-xs text-chalk/70">{{ username }}</p>
        </div>
        <button type="button" class="text-xs font-bold uppercase tracking-street hover:underline" @click="onLogout">
          Déconnexion
        </button>
      </div>
    </header>

    <div class="container-custom py-8 lg:flex lg:gap-8">
      <nav class="mb-8 flex flex-wrap gap-2 lg:mb-0 lg:w-56 lg:flex-col">
        <NuxtLink
          v-for="link in links"
          :key="link.to"
          :to="link.to"
          class="border-2 border-ink px-4 py-2 text-xs font-bold uppercase tracking-street transition hover:bg-acid"
          active-class="!bg-ink !text-chalk"
        >
          {{ link.label }}
        </NuxtLink>
        <a
          href="/"
          target="_blank"
          class="border-2 border-dashed border-ink px-4 py-2 text-xs font-bold uppercase tracking-street hover:bg-acid"
        >
          Voir le site
        </a>
      </nav>

      <main class="min-w-0 flex-1">
        <slot />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
const { username, logout } = useAdminAuth()

const links = [
  { to: '/admin', label: 'Tableau de bord' },
  { to: '/admin/parametres', label: 'Paramètres' },
  { to: '/admin/services', label: 'Services' },
  { to: '/admin/actualites', label: 'Actualités' },
  { to: '/admin/vehicules', label: 'Véhicules' },
  { to: '/admin/avis', label: 'Avis clients' },
  { to: '/admin/messages', label: 'Messages' },
  { to: '/admin/comptes', label: 'Comptes' },
  { to: '/admin/securite', label: 'Sécurité' },
]

async function onLogout() {
  await logout()
  await navigateTo('/admin/login')
}
</script>
