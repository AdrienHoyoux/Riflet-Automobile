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
      <nav class="mb-8 space-y-6 lg:mb-0 lg:w-56">
        <div v-for="group in linkGroups" :key="group.label">
          <p class="mb-2 text-[10px] font-bold uppercase tracking-street text-smoke">{{ group.label }}</p>
          <div class="flex flex-col gap-2">
            <NuxtLink
              v-for="link in group.links"
              :key="link.to"
              :to="link.to"
              class="border-2 border-ink px-4 py-2 text-xs font-bold uppercase tracking-street transition hover:bg-acid"
              active-class="!bg-ink !text-chalk"
            >
              {{ link.label }}
            </NuxtLink>
          </div>
        </div>
        <a
          href="/"
          target="_blank"
          class="inline-block border-2 border-dashed border-ink px-4 py-2 text-xs font-bold uppercase tracking-street hover:bg-acid"
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

const linkGroups = [
  {
    label: 'Général',
    links: [{ to: '/admin', label: 'Tableau de bord' }],
  },
  {
    label: 'Pages du site',
    links: [
      { to: '/admin/accueil', label: "Page d'accueil" },
      { to: '/admin/page-a-propos', label: 'Page À propos' },
      { to: '/admin/services', label: 'Page Services' },
      { to: '/admin/actualites', label: 'Actualités' },
      { to: '/admin/vehicules', label: 'Véhicules' },
      { to: '/admin/avis', label: 'Avis clients' },
    ],
  },
  {
    label: 'Garage',
    links: [
      { to: '/admin/parametres', label: 'Coordonnées & horaires' },
      { to: '/admin/messages', label: 'Messages contact' },
    ],
  },
  {
    label: 'Compte',
    links: [
      { to: '/admin/comptes', label: 'Comptes admin' },
      { to: '/admin/securite', label: 'Sécurité' },
    ],
  },
]

async function onLogout() {
  await logout()
  await navigateTo('/admin/login')
}
</script>
