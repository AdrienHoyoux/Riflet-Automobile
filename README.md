# Riflet Automobile — Site vitrine

Application web full-stack pour le garage **Riflet Automobile** à Malmedy (Belgique).

- **Frontend** : Nuxt 3, Tailwind CSS, GSAP, i18n (FR / DE / NL)
- **Backend** : Django REST Framework + Admin
- **Base de données** : MySQL 8
- **Déploiement** : Docker Compose (3 conteneurs séparés)

## Fonctionnalités

- Site vitrine responsive avec animations GSAP
- Multilingue : français (par défaut), allemand, néerlandais
- Services du garage modifiables via l'admin Django
- Actualités publiables par le client (admin)
- Formulaire de contact
- Logo officiel (photo de profil Facebook) dans l'en-tête, le hero et le pied de page
- Section avis clients Google sur la page d'accueil
- SEO : meta tags, JSON-LD, sitemap, robots.txt

## Démarrage rapide

### Prérequis

- [Docker](https://www.docker.com/) et Docker Compose

### Lancement

```bash
cp .env.example .env
docker compose up --build
```

| Service   | URL                                      |
|-----------|------------------------------------------|
| Site web  | http://localhost:3000                    |
| API       | http://localhost:8000/api/               |
| Admin     | http://localhost:8000/admin/             |

**Identifiants admin par défaut** (modifiables dans `.env`) :
- Utilisateur : `admin`
- Mot de passe : `admin123`

## Administration du contenu

Le client peut mettre à jour son site via l'interface Django Admin :

1. **Paramètres du site** — coordonnées, horaires, textes « À propos », logo, note Google
2. **Services** — ajouter/modifier/désactiver les prestations
3. **Actualités** — publier des articles multilingues avec images
4. **Avis clients** — gérer les avis Google affichés sur l'accueil
5. **Messages de contact** — consulter les demandes reçues

Chaque contenu éditorial possède des champs en **français**, **allemand** et **néerlandais**.

## Structure du projet

```
├── docker-compose.yml
├── backend/          # Django + DRF
│   ├── config/       # Settings Django
│   └── garage/       # Modèles, API, Admin, seed
└── frontend/         # Nuxt 3
    ├── components/
    ├── composables/
    ├── locales/      # Traductions UI
    └── pages/
```

## API REST

| Endpoint              | Méthode | Description              |
|-----------------------|---------|--------------------------|
| `/api/settings/`      | GET     | Infos du garage          |
| `/api/services/`      | GET     | Liste des services       |
| `/api/news/`          | GET     | Liste des actualités     |
| `/api/news/<slug>/`   | GET     | Détail d'une actualité   |
| `/api/reviews/`       | GET     | Avis clients Google      |
| `/api/contact/`       | POST    | Envoi formulaire contact |

## Données initiales

Les données proviennent des informations publiques du garage :

- [Page Facebook Riflet Automobile](https://www.facebook.com/p/Riflet-Automobile-100089580491690/)
- [Fiche Bottin.be](https://www.bottin.be/fr/fiche-locale/bhjdcbefghijccgeggdc--riflet-automobile--malmedy.htm)

Adresse : Avenue de Norvège 3, 4960 Malmedy  
Téléphone : 080 39 99 81  
E-mail : hoyouxadrien09@outlook.com

### Avis Google

Des avis exemple sont chargés via `seed_data`. Pour synchroniser les vrais avis depuis Google :

1. Créer une clé [Google Places API (New)](https://developers.google.com/maps/documentation/places/web-service/get-api-key)
2. Ajouter `GOOGLE_PLACES_API_KEY` dans `.env`
3. Exécuter :

```bash
docker compose exec backend python manage.py sync_google_reviews
```

Les avis peuvent aussi être modifiés manuellement dans l'admin Django (**Avis clients**).

## Développement local (sans Docker)

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
# Configurer MySQL et variables .env
python manage.py migrate
python manage.py seed_data
python manage.py runserver
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Production

1. Modifier `.env` : `DJANGO_DEBUG=False`, clé secrète forte, mots de passe sécurisés
2. Mettre à jour `NUXT_PUBLIC_SITE_URL` avec le domaine final
3. Configurer un reverse proxy (Nginx) avec HTTPS
4. Remplacer `runserver` par Gunicorn dans le Dockerfile backend

## Licence

Projet réalisé pour Riflet Automobile.
