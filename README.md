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
| Admin site | http://localhost:3000/admin/login |
| Admin Django | http://localhost:8000/django-admin/ |

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

L'**admin Django** (`/django-admin/`) reste disponible pour les réglages avancés.

### Administration en production

| Panneau | URL |
|---------|-----|
| **Admin du site** (recommandé) | https://rifletautomobile.be/admin/login |
| **Admin Django** (avancé) | https://rifletautomobile.be/django-admin/ |

Identifiants : variables `ADMIN_USERNAME` et `ADMIN_PASSWORD` (Hostinger → Docker Manager → variables d'environnement). Compte créé par `seed_data` au premier démarrage.

Si la MFA est activée : mot de passe puis code à 6 chiffres (Google Authenticator).

Chaque contenu éditorial possède des champs en **français**, **allemand** et **néerlandais**.

## Structure du projet

```
├── docker-compose.yml      # Production (Hostinger VPS + Traefik, rifletautomobile.be)
├── docker-compose.dev.yml  # Developpement local
├── .env.production.example # Variables pour la mise en prod
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

Les messages sont **enregistrés dans l'admin** (`Messages de contact`) **et** envoyés par e-mail à `CONTACT_EMAIL`.

### Option recommandée : une seule boîte (pas de noreply)

**Vous n'avez pas besoin** d'une adresse `noreply@` séparée. Utilisez la même boîte pour envoyer et recevoir :

| Variable | Rôle |
|----------|------|
| `CONTACT_EMAIL` | Reçoit les messages + affichée sur le site |
| `EMAIL_HOST_USER` | **Même adresse** — compte SMTP qui envoie |
| `DEFAULT_FROM_EMAIL` | **Même adresse** — expéditeur affiché |

```env
CONTACT_EMAIL=hoyouxadrien@gmail.com
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=465
EMAIL_USE_TLS=False
EMAIL_USE_SSL=True
EMAIL_HOST_USER=hoyouxadrien@gmail.com
EMAIL_HOST_PASSWORD=mot_de_passe_application_gmail
DEFAULT_FROM_EMAIL=hoyouxadrien@gmail.com
```

Quand vous aurez `contact@rifletautomobile.be` chez Hostinger, mettez **la même adresse** partout et `EMAIL_HOST=smtp.hostinger.com`.

Le champ **Répondre à** (`Reply-To`) contient l'e-mail du visiteur : vous répondez directement au client, pas à votre propre boîte.

**Gmail** : [mot de passe d'application](https://myaccount.google.com/apppasswords) (validation 2 étapes requise).

### Autres options (si besoin)

| Option | Avantage | Inconvénient |
|--------|----------|--------------|
| **Admin seulement** | Gratuit, zéro config | Pas d'e-mail : laissez `EMAIL_HOST` vide |
| **Une boîte garage** | Simple, suffisant pour un petit site | — |
| **Service transactionnel** (Resend, Brevo…) | Envoi sans boîte réelle, `noreply@` possible via DNS | Compte + clé API + config domaine |
| **Boîte noreply dédiée** | Sépare envoi auto / contact humain | 2e boîte à gérer (souvent inutile ici) |

### Tester

Redémarrez le backend puis :

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

Domaine : **`rifletautomobile.be`**

1. hPanel → **Domaines** → `rifletautomobile.be` → **DNS** :
   - **A** `@` → IP du VPS
   - **A** `www` → IP du VPS (ou **CNAME** `www` → `rifletautomobile.be`)
2. hPanel → **VPS** → **Docker Manager** → déployez le modèle **Traefik** (catalogue)
3. Attendez que Traefik soit **Running** (certificat Let's Encrypt automatique)

### Étape B — Déployer Riflet Automobile

1. **Docker Manager** → **Compose** → **Compose from URL**
2. URL du **dépôt GitHub** (obligatoire pour que le build inclue le code source) :

   `https://github.com/AdrienHoyoux/Riflet-Automobile`

   *(N'utilisez pas l'URL raw du seul fichier `docker-compose.yml` — le build échouerait sans le code backend/frontend.)*
3. **Nom du projet** : `riflet-automobile`
4. Ajoutez les **variables d'environnement** :

| Variable | Valeur pour votre VPS |
|----------|----------------------|
| `DJANGO_SECRET_KEY` | longue chaîne aléatoire |
| `DJANGO_ALLOWED_HOSTS` | `rifletautomobile.be,www.rifletautomobile.be,backend` |
| `CORS_ALLOWED_ORIGINS` | `https://rifletautomobile.be,https://www.rifletautomobile.be` |
| `CSRF_TRUSTED_ORIGINS` | `https://rifletautomobile.be,https://www.rifletautomobile.be` |
| `NUXT_PUBLIC_SITE_URL` | `https://rifletautomobile.be` |
| `NUXT_PUBLIC_API_BASE` | `https://rifletautomobile.be` |
| `MYSQL_PASSWORD` | mot de passe fort |
| `MYSQL_ROOT_PASSWORD` | mot de passe fort |
| `ADMIN_PASSWORD` | mot de passe admin |

5. Cliquez **Deploy** — le premier build peut prendre 5–10 min
6. **Données initiales** : `seed_data` s'exécute **automatiquement** au démarrage du conteneur `riflet_backend` (voir `backend/docker-entrypoint.sh`). Dans **View logs** du backend, cherchez :
   - `Seeding initial data...`
   - `Données initialisées avec succès.`

   **Vous n'avez en principe pas besoin** de lancer `seed_data` à la main.

### Relancer seed_data sur Hostinger (si besoin)

Le terminal du VPS (SSH ou hPanel) n'est **pas** dans le conteneur Django : `python manage.py` y échoue (`manage.py not found`).

**Méthode 1 — Terminal du conteneur (recommandé)**  
Docker Manager → projet `riflet-automobile` → conteneur **backend** (`riflet_backend`) → **Terminal** / **Console** :

```bash
python manage.py seed_data
```

**Méthode 2 — SSH sur le VPS**

```bash
docker ps
docker exec riflet_backend python manage.py seed_data
```

Si le nom diffère (ex. `riflet-automobile-backend-1`), utilisez celui affiché par `docker ps`.

**Méthode 3 — Redémarrer le backend**  
⋮ → **Restart** sur le conteneur backend → `seed_data` repasse au démarrage.

Connexion admin : `https://rifletautomobile.be/admin/login` (identifiants `ADMIN_USERNAME` / `ADMIN_PASSWORD`).

### Depannage si le deploiement echoue

| Erreur probable | Solution |
|-----------------|----------|
| **`project not found`** | Creez un **nouveau** deploiement (pas Update). Nom : `riflet-automobile` |
| Fichier compose introuvable | Utilisez l'URL raw de `docker-compose.yml` (etape B) |
| `network traefik-proxy not found` | Votre Traefik utilise `network_mode: host` (pas de réseau `traefik-proxy`) — le compose Riflet n'en a plus besoin ; mettez à jour le repo |
| Reseau avec un autre nom | Uniquement si vous utilisez le modele Traefik **avec** reseau partage — definissez `TRAEFIK_NETWORK=nom_du_reseau` |
| Build frontend timeout / OOM | Relancez **Update** ; un VPS 2 Go+ est recommande |
| Repo prive inaccessible | Ajoutez une [deploy key GitHub](https://www.hostinger.com/support/how-to-deploy-from-private-github-repository-on-hostinger-docker-manager/) |
| Conteneurs en Restarting | **View logs** → souvent mot de passe MySQL incorrect (voir ci-dessous) |
| `Access denied for user 'riflet_user'` | Mot de passe MySQL incohérent entre backend et base — voir **Dépannage MySQL** |
| `Host(\`\`)` dans les logs | DNS pas encore propagé ou mauvais domaine dans Traefik — vérifiez `rifletautomobile.be` |
| `ENOENT package.json` ou `manage.py not found` | Terminal **hors** conteneur — ouvrez le terminal du conteneur **backend**, ou `docker exec riflet_backend ...` |
| `python manage.py` ne marche pas (Hostinger) | Normal sur le VPS : utilisez le terminal du conteneur `riflet_backend` ou `docker exec` (voir ci-dessus) |

*(repo privé : deploy key requise — voir [doc Hostinger](https://www.hostinger.com/support/how-to-deploy-from-private-github-repository-on-hostinger-docker-manager/))*

### Dépannage MySQL (`Access denied for user 'riflet_user'`)

MySQL enregistre le mot de passe **au premier démarrage** (volume `mysql_data`). Si vous changez `MYSQL_PASSWORD` dans Hostinger ensuite, le backend utilise le nouveau mot de passe mais MySQL garde l'ancien.

**1. Vérifier les mots de passe actuels (SSH)**

```bash
docker exec riflet_backend env | grep MYSQL
docker exec riflet_mysql env | grep MYSQL
```

Les valeurs `MYSQL_PASSWORD` doivent être **identiques** dans les deux conteneurs.

**2. Solution rapide (site neuf, pas de données à garder)**

1. Docker Manager → supprimez le projet `riflet-automobile` **en cochant la suppression des volumes**
2. Définissez `MYSQL_PASSWORD` et `MYSQL_ROOT_PASSWORD` (mots de passe forts, **identiques à chaque redeploy**)
3. Redéployez → `seed_data` passera automatiquement au démarrage du backend

**3. Garder les données — réaligner le mot de passe MySQL**

```bash
# Remplacez NOUVEAU_MDP et ROOT_MDP par vos variables Hostinger
docker exec -it riflet_mysql mysql -uroot -pROOT_MDP -e "ALTER USER 'riflet_user'@'%' IDENTIFIED BY 'NOUVEAU_MDP'; FLUSH PRIVILEGES;"
docker restart riflet_backend
```

Puis vérifiez les logs du backend (`Données initialisées avec succès`).

### Reconstruction complète (tout supprimer et redéployer)

À utiliser si MySQL, les médias ou la config sont cassés. **Toutes les données** (base MySQL, photos uploadées, messages) seront **effacées**. `seed_data` recréera le contenu de démo au redémarrage.

#### Méthode A — Docker Manager Hostinger (recommandé)

1. hPanel → **VPS** → **Docker Manager**
2. Projet `riflet-automobile` → **⋮** → **Delete** / **Supprimer**
3. **Cochez « Remove volumes »** / **« Supprimer les volumes »** (obligatoire)
4. Confirmez la suppression — attendez que les conteneurs et volumes disparaissent
5. **Compose** → **Compose from URL** → même URL GitHub qu'avant
6. Nom du projet : `riflet-automobile`
7. Renseignez **toutes** les variables (copiez `.env.production.example`) :
   - `MYSQL_PASSWORD` et `MYSQL_ROOT_PASSWORD` : mots de passe forts, **à noter**
   - `DJANGO_SECRET_KEY`, `ADMIN_PASSWORD`, etc.
8. **Deploy** — premier build : 5–10 min
9. **View logs** du conteneur `riflet_backend` → attendez :
   ```
   Données initialisées avec succès.
   Starting application...
   ```

Ne faites pas seulement **Update** après un changement de `MYSQL_PASSWORD` : sans suppression des volumes, MySQL garde l'ancien mot de passe.

#### Méthode B — SSH sans supprimer le projet hPanel (recommandé si le projet existe déjà)

Gardez le projet et les **variables d'environnement** dans Docker Manager. Seuls conteneurs et volumes sont recréés.

```bash
# 1. Arrêter les conteneurs Riflet (noms fixes dans docker-compose.yml)
docker stop riflet_frontend riflet_backend riflet_mysql 2>/dev/null || true
docker rm riflet_frontend riflet_backend riflet_mysql 2>/dev/null || true

# 2. Lister les volumes (noms possibles selon le déploiement Hostinger)
docker volume ls | grep -E 'riflet|mysql_data|media_data'

# 3. Supprimer les volumes MySQL + médias (adaptez si les noms diffèrent)
docker volume rm riflet-automobile_mysql_data riflet-automobile_media_data 2>/dev/null || true
docker volume rm mysql_data media_data 2>/dev/null || true

# 4. Vérifier que tout est parti
docker ps -a | grep riflet
docker volume ls | grep -E 'riflet|mysql_data|media_data'
```

**5. Redémarrer le build** — au choix :

- **hPanel** → Docker Manager → projet `riflet-automobile` → **⋮** → **Update** (ou **Restart** si Update relance le compose)
- **Ou SSH** si vous connaissez le dossier du déploiement Hostinger :

```bash
cd /docker/riflet-automobile   # chemin indicatif — voir note ci-dessous
docker compose up -d --build
```

**Trouver le dossier du projet sur le VPS :**

```bash
docker inspect riflet_backend --format '{{.Config.Labels}}' 2>/dev/null
# ou, après suppression des conteneurs, chercher le compose :
find / -name "docker-compose.yml" 2>/dev/null | grep -i riflet
```

**6. Vérifier les logs**

```bash
docker logs -f riflet_backend
```

Attendez `Données initialisées avec succès.` — `seed_data` repasse au démarrage.

> **Avant l'étape 1** : vérifiez que `MYSQL_PASSWORD` et `MYSQL_ROOT_PASSWORD` dans hPanel sont corrects et **identiques** à ce que vous voulez utiliser. Les nouveaux volumes MySQL prendront ces valeurs.

#### Méthode C — SSH avec `docker compose down -v` (si vous avez le dossier du projet)

```bash
cd /chemin/vers/le/projet   # dossier contenant docker-compose.yml
docker compose down -v
docker compose up -d --build
```

#### Vérification après reconstruction

```bash
docker ps
docker exec riflet_backend env | grep MYSQL_PASSWORD
docker exec riflet_mysql env | grep MYSQL_PASSWORD
docker logs riflet_backend --tail 30
```

Les deux `MYSQL_PASSWORD` doivent être identiques. Le site : `https://rifletautomobile.be` — admin : `/admin/login`.

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
| `DJANGO_ALLOWED_HOSTS` | `rifletautomobile.be,www.rifletautomobile.be,backend` |
| `CORS_ALLOWED_ORIGINS` | `https://rifletautomobile.be,https://www.rifletautomobile.be` |
| `CSRF_TRUSTED_ORIGINS` | `https://rifletautomobile.be,https://www.rifletautomobile.be` |
| `NUXT_PUBLIC_SITE_URL` | `https://rifletautomobile.be` |
| `NUXT_PUBLIC_API_BASE` | `https://rifletautomobile.be` |
| `MYSQL_*` | mots de passe forts |

### 3. Lancer l'application

```bash
docker compose up -d --build
docker compose exec backend python manage.py seed_data
```

### 4. Nginx + HTTPS

```bash
cp deploy/nginx/riflet.conf.example /etc/nginx/sites-available/riflet
ln -s /etc/nginx/sites-available/riflet /etc/nginx/sites-enabled/
nginx -t && systemctl reload nginx
certbot --nginx -d rifletautomobile.be -d www.rifletautomobile.be
```

Le fichier `deploy/nginx/riflet.conf.example` est déjà configuré pour `rifletautomobile.be`.
Modèle complet des variables : `.env.production.example`.

### Mises à jour

```bash
cd /var/www/Riflet-Automobile
git pull
docker compose up -d --build
```

## Licence

Projet réalisé pour Riflet Automobile.
