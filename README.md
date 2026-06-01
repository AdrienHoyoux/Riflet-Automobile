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
docker compose -f docker-compose.dev.yml up --build
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
├── docker-compose.yml      # Production (Hostinger VPS + Traefik)
├── docker-compose.dev.yml  # Developpement local
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

## Production (VPS Hostinger + Docker Manager)

> Méthode recommandée si vous utilisez le **tableau de bord Docker** dans hPanel.

### Étape A — DNS et Traefik

1. Chez Hostinger (DNS), créez un enregistrement **A** : `@` → IP du VPS  
2. hPanel → **VPS** → **Docker Manager** → déployez le modèle **Traefik** (catalogue)  
3. Attendez que Traefik soit **Running**

### Étape B — Déployer Riflet Automobile

1. **Docker Manager** → **Compose** → **Compose from URL**
2. URL du **dépôt GitHub** (obligatoire pour que le build inclue le code source) :

   `https://github.com/AdrienHoyoux/Riflet-Automobile`

   *(N'utilisez pas l'URL raw du seul fichier `docker-compose.yml` — le build échouerait sans le code backend/frontend.)*
3. **Nom du projet** : `riflet-automobile`
4. Ajoutez les **variables d'environnement** :

| Variable | Valeur pour votre VPS |
|----------|----------------------|
| `DOMAIN` | `hoyouxcorp.tech` |
| `DJANGO_SECRET_KEY` | longue chaîne aléatoire |
| `DJANGO_ALLOWED_HOSTS` | `hoyouxcorp.tech,www.hoyouxcorp.tech,backend` |
| `CORS_ALLOWED_ORIGINS` | `https://hoyouxcorp.tech,https://www.hoyouxcorp.tech` |
| `CSRF_TRUSTED_ORIGINS` | `https://hoyouxcorp.tech,https://www.hoyouxcorp.tech` |
| `NUXT_PUBLIC_SITE_URL` | `https://hoyouxcorp.tech` |
| `NUXT_PUBLIC_API_BASE` | `https://hoyouxcorp.tech` |
| `MYSQL_PASSWORD` | mot de passe fort |
| `MYSQL_ROOT_PASSWORD` | mot de passe fort |
| `ADMIN_PASSWORD` | mot de passe admin |

5. Cliquez **Deploy** — le premier build peut prendre 5–10 min
6. Terminal conteneur **backend** :

```bash
python manage.py seed_data
```

### Depannage si le deploiement echoue

| Erreur probable | Solution |
|-----------------|----------|
| **`project not found`** | Creez un **nouveau** deploiement (pas Update). Nom : `riflet-automobile` |
| Fichier compose introuvable | Utilisez l'URL raw de `docker-compose.yml` (etape B) |
| `network traefik-proxy not found` | Votre Traefik utilise `network_mode: host` (pas de réseau `traefik-proxy`) — le compose Riflet n'en a plus besoin ; mettez à jour le repo |
| Reseau avec un autre nom | Uniquement si vous utilisez le modele Traefik **avec** reseau partage — definissez `TRAEFIK_NETWORK=nom_du_reseau` |
| Build frontend timeout / OOM | Relancez **Update** ; un VPS 2 Go+ est recommande |
| Repo prive inaccessible | Ajoutez une [deploy key GitHub](https://www.hostinger.com/support/how-to-deploy-from-private-github-repository-on-hostinger-docker-manager/) |
| Conteneurs en Restarting | **View logs** → si mot de passe MySQL change, supprimez le projet et redeployez |
| `Host(\`\`)` dans les logs | Variable `DOMAIN` manquante — ajoutez `DOMAIN=hoyouxcorp.tech` |
| `ENOENT package.json` ou `manage.py not found` | Le compose utilisait des volumes dev (`./frontend:/app`) qui écrasaient le code — mettez à jour le repo et redeployez |

*(repo privé : deploy key requise — voir [doc Hostinger](https://www.hostinger.com/support/how-to-deploy-from-private-github-repository-on-hostinger-docker-manager/))*

### Gestion via le tableau de bord

- **Logs** : ⋮ → View logs (par conteneur)
- **Redémarrage** : ⋮ → Restart
- **Mise à jour** : poussez sur GitHub → ⋮ → Update

---

## Production (VPS manuel SSH)

### 1. Préparer le serveur (Ubuntu)

```bash
# Connexion SSH (IP et mot de passe depuis hPanel Hostinger)
ssh root@VOTRE_IP_VPS

# Docker
curl -fsSL https://get.docker.com | sh
apt install -y nginx certbot python3-certbot-nginx git
```

### 2. Cloner et configurer

```bash
cd /var/www
git clone https://github.com/AdrienHoyoux/Riflet-Automobile.git
cd Riflet-Automobile
cp .env.example .env
nano .env
```

Variables importantes dans `.env` :

| Variable | Exemple production |
|----------|-------------------|
| `DJANGO_DEBUG` | `False` |
| `DJANGO_SECRET_KEY` | chaîne longue aléatoire |
| `DJANGO_ALLOWED_HOSTS` | `votre-domaine.com,www.votre-domaine.com,backend` |
| `CORS_ALLOWED_ORIGINS` | `https://votre-domaine.com,https://www.votre-domaine.com` |
| `CSRF_TRUSTED_ORIGINS` | `https://votre-domaine.com,https://www.votre-domaine.com` |
| `NUXT_PUBLIC_SITE_URL` | `https://votre-domaine.com` |
| `NUXT_PUBLIC_API_BASE` | `https://votre-domaine.com` |
| `MYSQL_*` | mots de passe forts |

### 3. Lancer l'application

```bash
docker compose up -d --build
docker compose exec backend python manage.py seed_data
```

### 4. Nginx + HTTPS

```bash
cp deploy/nginx/riflet.conf.example /etc/nginx/sites-available/riflet
nano /etc/nginx/sites-available/riflet   # remplacer VOTRE_DOMAINE
ln -s /etc/nginx/sites-available/riflet /etc/nginx/sites-enabled/
nginx -t && systemctl reload nginx
certbot --nginx -d votre-domaine.com -d www.votre-domaine.com
```

Pointer le domaine (DNS chez Hostinger) vers l'IP du VPS (enregistrement **A**).

### Mises à jour

```bash
cd /var/www/Riflet-Automobile
git pull
docker compose up -d --build
```

## Licence

Projet réalisé pour Riflet Automobile.
