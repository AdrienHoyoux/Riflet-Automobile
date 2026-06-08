<template>
  <div>
    <h1 class="font-display text-4xl">Tableau de bord</h1>
    <p class="mt-2 text-smoke">Modifiez le site page par page, comme dans le menu de gauche.</p>

    <section v-for="group in groups" :key="group.label" class="mt-10">
      <h2 class="text-xs font-bold uppercase tracking-street text-smoke">{{ group.label }}</h2>
      <div class="mt-4 grid gap-4 sm:grid-cols-2">
        <NuxtLink
          v-for="card in group.cards"
          :key="card.to"
          :to="card.to"
          class="card block !p-6 transition hover:-translate-y-1 hover:shadow-hard"
        >
          <h3 class="font-display text-2xl">{{ card.title }}</h3>
          <p class="mt-2 text-sm text-smoke">{{ card.text }}</p>
        </NuxtLink>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: 'admin', middleware: 'admin-auth' })

const groups = [
  {
    label: 'Pages du site',
    cards: [
      {
        to: '/admin/accueil',
        title: "Page d'accueil",
        text: 'Bloc services, « Pourquoi nous choisir » et arguments.',
      },
      {
        to: '/admin/page-a-propos',
        title: 'Page À propos',
        text: 'En-tête, photo et texte de présentation du garage.',
      },
      {
        to: '/admin/services',
        title: 'Page Services',
        text: 'En-tête de la page et liste des prestations (cartes).',
      },
      { to: '/admin/actualites', title: 'Actualités', text: 'Articles et nouvelles du garage.' },
      { to: '/admin/vehicules', title: 'Véhicules', text: 'Voitures d\'occasion en vente.' },
      { to: '/admin/avis', title: 'Avis clients', text: 'Avis affichés sur l\'accueil.' },
    ],
  },
  {
    label: 'Garage & compte',
    cards: [
      {
        to: '/admin/parametres',
        title: 'Coordonnées & horaires',
        text: 'Nom, logo, bannière, adresse, téléphone, horaires.',
      },
      { to: '/admin/messages', title: 'Messages', text: 'Demandes reçues via le formulaire de contact.' },
      { to: '/admin/comptes', title: 'Comptes admin', text: 'Accès à cette interface.' },
      { to: '/admin/securite', title: 'Sécurité', text: 'Mot de passe et double authentification.' },
    ],
  },
]
</script>
