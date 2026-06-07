<template>
  <div>
    <h1 class="font-display text-4xl">Tableau de bord</h1>
    <p class="mt-2 text-smoke">Gérez le contenu du site vitrine Riflet Automobile.</p>

    <div class="mt-10 grid gap-4 sm:grid-cols-2">
      <NuxtLink
        v-for="card in cards"
        :key="card.to"
        :to="card.to"
        class="card block !p-6 transition hover:-translate-y-1 hover:shadow-hard"
      >
        <h2 class="font-display text-2xl">{{ card.title }}</h2>
        <p class="mt-2 text-sm text-smoke">{{ card.text }}</p>
      </NuxtLink>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: 'admin', middleware: 'admin-auth' })

const cards = [
  { to: '/admin/parametres', title: 'Paramètres', text: 'Textes, horaires, coordonnées — aperçu à côté de chaque section.' },
  { to: '/admin/actualites', title: 'Actualités', text: 'Publier et modifier les articles.' },
  { to: '/admin/vehicules', title: 'Véhicules', text: 'Ajouter des voitures d\'occasion.' },
  { to: '/admin/avis', title: 'Avis', text: 'Ajouter des avis à la main et choisir les 6 de l\'accueil.' },
  { to: '/admin/messages', title: 'Messages', text: 'Consulter les demandes de contact.' },
  { to: '/admin/comptes', title: 'Comptes', text: 'Ajouter ou supprimer des accès admin.' },
  { to: '/admin/securite', title: 'Sécurité', text: 'Mot de passe et authentification à deux facteurs (MFA).' },
]
</script>
