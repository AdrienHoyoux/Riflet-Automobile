# Riflet Automobile — Site vitrine

Application web full-stack pour le garage **Riflet Automobile** à Malmedy (Belgique).

- **Frontend** : Nuxt 3, Tailwind CSS, GSAP, i18n (FR / DE / NL)
- **Backend** : Django REST Framework + Admin
- **Base de données** : MySQL 8
- **Déploiement** : Docker Compose (3 conteneurs séparés)

## Fonctionnalités

- Site vitrine responsive avec animations GSAP
- Multilingue : français (par défaut), allemand, néerlandais
- Services du garage modifiables via l'admin
- Actualités publiables par le client (admin)
- **Véhicules d'occasion** — catalogue public + gestion depuis l'admin
- **Panneau d'administration** intégré au site (`/admin/login`)
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
| Admin site| http://localhost:3000/admin/login        |
| Admin Django | http://localhost:8000/admin/          |

**Identifiants admin par défaut** (modifiables dans `.env`) :
- Utilisateur : `admin`
- Mot de passe : `admin123`

## Administration du contenu

Le client peut mettre à jour son site via le **panneau d'administration** du site (recommandé) :

**URL** : `/admin/login` (ex. `http://localhost:3000/admin/login`)

Utilisez les identifiants définis dans `.env` (`ADMIN_USERNAME` / `ADMIN_PASSWORD`). L'utilisateur doit être **staff** (créé automatiquement par `seed_data`).

| Section | Contenu modifiable |
|---------|-------------------|
| **Paramètres** | Coordonnées, horaires, textes « À propos », URLs des photos (logo, hero) |
| **Actualités** | Créer, modifier, publier des articles multilingues |
| **Véhicules** | Ajouter des voitures d'occasion (marque, prix, km, photo, description FR/DE/NL) |
| **Avis** | Ajouter des avis à la main, choisir les 6 de l'accueil (sync Google optionnelle, payante) |
| **Messages** | Consulter les demandes reçues via le formulaire de contact |
| **Sécurité** | Activer la MFA (Google Authenticator, etc.) via QR code |
| **Comptes** | Créer ou supprimer des accès à l'administration du site |

### Authentification à deux facteurs (MFA)

1. Connectez-vous à `/admin/login`
2. Allez dans **Sécurité** → **Configurer la MFA**
3. Scannez le **QR code** avec Google Authenticator (ou équivalent)
4. Saisissez le code à 6 chiffres pour confirmer

Une fois activée, chaque connexion demande le mot de passe **puis** un code TOTP généré par l'application mobile.

L'**admin Django** (`/admin/`) reste disponible pour les services et les réglages avancés.

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

## Formulaire de contact — réception par e-mail (SMTP)

Les messages sont **enregistrés dans l'admin Django** (`Messages de contact`) **et** envoyés par e-mail à `CONTACT_EMAIL`.

| Variable | Rôle |
|----------|------|
| `CONTACT_EMAIL` | Boîte qui **reçoit** les messages (+ affichée sur le site) |
| `EMAIL_HOST_USER` | Compte SMTP qui **envoie** les notifications |
| `DEFAULT_FROM_EMAIL` | Adresse affichée comme expéditeur |

**Actuellement** : adresse perso du développeur. **Plus tard** : remplacez par l'e-mail du garage.

```env
CONTACT_EMAIL=hoyouxadrien@gmail.com
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=465
EMAIL_USE_TLS=False
EMAIL_USE_SSL=True
EMAIL_HOST_USER=hoyouxadrien@gmail.com
EMAIL_HOST_PASSWORD=mot_de_passe_application_sans_espaces
DEFAULT_FROM_EMAIL=hoyouxadrien@gmail.com
```

Pour passer à l'e-mail du garage (ex. `contact@hoyouxcorp.com` via Hostinger) :

1. Modifiez `CONTACT_EMAIL`, `EMAIL_HOST_USER` et `DEFAULT_FROM_EMAIL`
2. Adaptez `EMAIL_HOST` / `EMAIL_PORT` (Hostinger : `smtp.hostinger.com`, port 465)
3. Redémarrez le backend : `docker compose up -d --force-recreate backend`
4. Relancez `python manage.py seed_data` pour mettre à jour l'e-mail affiché sur le site

**Gmail** : [mot de passe d'application](https://myaccount.google.com/apppasswords) (sans espaces).

### Tester

```bash
docker exec -it riflet_backend python manage.py test_email
```

## Données initiales

Les données proviennent des informations publiques du garage :

- [Page Facebook Riflet Automobile](https://www.facebook.com/p/Riflet-Automobile-100089580491690/)
- [Fiche Bottin.be](https://www.bottin.be/fr/fiche-locale/bhjdcbefghijccgeggdc--riflet-automobile--malmedy.htm)

Adresse : Avenue de Norvège 3, 4960 Malmedy  
Téléphone : 080 39 99 81  
E-mail : hoyouxadrien@gmail.com

### Avis clients (gratuit, sans API)

Dans **Admin → Avis** :

1. **Ajouter un avis** — copiez nom, note et texte depuis Google Maps / Facebook (aucune API requise).
2. Cochez jusqu'à **6 avis** et **Enregistrer la sélection** pour l'accueil.
3. Renseignez le **bloc Google** (note moyenne, nombre total, lien Maps) à la main depuis votre fiche Google.

**Option payante** : synchronisation automatique via `GOOGLE_PLACES_API_KEY` (Google Places API, facturation après le crédit mensuel). Bouton repliable dans l'admin ou commande `sync_google_reviews`.

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
| `DOMAIN` | `hoyouxcorp.com` |
| `DJANGO_SECRET_KEY` | longue chaîne aléatoire |
| `DJANGO_ALLOWED_HOSTS` | `hoyouxcorp.com,www.hoyouxcorp.com,backend` |
| `CORS_ALLOWED_ORIGINS` | `https://hoyouxcorp.com,https://www.hoyouxcorp.com` |
| `CSRF_TRUSTED_ORIGINS` | `https://hoyouxcorp.com,https://www.hoyouxcorp.com` |
| `NUXT_PUBLIC_SITE_URL` | `https://hoyouxcorp.com` |
| `NUXT_PUBLIC_API_BASE` | `https://hoyouxcorp.com` |
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
| `Host(\`\`)` dans les logs | Variable `DOMAIN` manquante — ajoutez `DOMAIN=hoyouxcorp.com` |
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
