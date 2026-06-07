# Déploiement manuel sur Hostinger (SSH + docker compose)

Guide pour gérer le projet **sans** Docker Manager « Compose from URL ».

## Prérequis

- VPS Hostinger avec Docker installé
- Traefik déjà déployé (modèle catalogue hPanel)
- DNS `rifletautomobile.be` → IP du VPS (A `@` et `www`)
- Traefik doit voir le réseau Docker du projet. Dans la config Traefik, ajouter si besoin :
  ```
  --providers.docker.network=riflet-automobile_default
  ```

## 1. Arrêter l’ancien déploiement Docker Manager

Si le projet tournait via hPanel → **Docker Manager** :

1. Supprimez le projet `riflet-automobile` dans hPanel **ou**
2. SSH :
   ```bash
   docker stop riflet_frontend riflet_backend riflet_mysql 2>/dev/null || true
   docker rm riflet_frontend riflet_backend riflet_mysql 2>/dev/null || true
   ```

Ne gardez **qu’une seule** stack Riflet sur le VPS.

## 2. Première installation (SSH)

```bash
ssh root@VOTRE_IP_VPS

mkdir -p /var/www && cd /var/www
git clone https://github.com/AdrienHoyoux/Riflet-Automobile.git
cd Riflet-Automobile

cp .env.production.example .env
nano .env
```

Renseignez au minimum :

| Variable | Exemple |
|----------|---------|
| `DJANGO_SECRET_KEY` | longue chaîne aléatoire |
| `MYSQL_PASSWORD` | mot de passe fort (noté) |
| `MYSQL_ROOT_PASSWORD` | autre mot de passe fort |
| `ADMIN_PASSWORD` | mot de passe admin site |
| `NUXT_PUBLIC_SITE_URL` | `https://rifletautomobile.be` |
| `NUXT_PUBLIC_API_BASE` | `https://rifletautomobile.be` |

**Ne pas** mettre `localhost:8000` dans les variables Nuxt.

```bash
chmod +x deploy/hostinger.sh
./deploy/hostinger.sh install
```

Ou sans script :

```bash
docker compose -p riflet-automobile --env-file .env up -d --build
```

Premier build : **5–10 minutes**.

## 3. Vérifier

```bash
docker ps
docker logs riflet_backend --tail 40
```

Attendu dans les logs :

```
Données initialisées avec succès.
Starting application...
```

- Site : https://rifletautomobile.be  
- Admin : https://rifletautomobile.be/admin/login  
- Django : https://rifletautomobile.be/django-admin/

Identifiants admin : `ADMIN_USERNAME` / `ADMIN_PASSWORD` du fichier `.env`.

## 4. Mises à jour

```bash
cd /var/www/Riflet-Automobile
./deploy/hostinger.sh update
```

Équivalent :

```bash
git pull origin main
docker compose -p riflet-automobile --env-file .env up -d --build
```

Rebuild **frontend** seul (après changement Nuxt) :

```bash
docker compose -p riflet-automobile --env-file .env up -d --build frontend
```

## 5. Commandes utiles

```bash
./deploy/hostinger.sh logs          # logs backend (seed, erreurs)
docker logs riflet_frontend --tail 30
docker compose -p riflet-automobile ps

# Test e-mail contact
docker exec riflet_backend python manage.py test_email

# Réinitialiser MySQL + médias (site neuf)
./deploy/hostinger.sh reset-volumes
./deploy/hostinger.sh install
```

## 6. Repo privé

```bash
git clone git@github.com:AdrienHoyoux/Riflet-Automobile.git
```

Configurez une clé SSH sur le VPS ou un token GitHub.

## Dépannage rapide

| Problème | Action |
|----------|--------|
| `No such image: …-backend:latest` | Les images n'ont **pas été buildées** — voir section ci-dessous |
| `rfielt-atuomobile-backend` (faute) | Nom de projet Docker Manager mal orthographié → recréer `riflet-automobile` |
| `Access denied riflet_user` | `./deploy/hostinger.sh reset-volumes` puis `install` avec bons mots de passe |
| Admin Django sur `/admin` | `git pull` + rebuild — voir README (Traefik `/admin` → Nuxt) |
| Login appelle `localhost:8000` | Rebuild frontend + `.env` sans localhost |
| 502 / pas de HTTPS | Traefik Running + DNS propagé |

## Docker Manager : coller seulement le YAML ne suffit pas

Si vous créez un projet en collant **uniquement** `docker-compose.yml` dans hPanel (sans dépôt Git) :

```
backend Skipped No image to be pulled
No such image: xxx-backend:latest
```

**Cause** : les services `backend` et `frontend` utilisent `build:` (Dockerfile + code source). Sans le dossier `backend/`, `frontend/`, etc., Docker **ne peut pas construire** les images. Il cherche une image déjà existante → erreur.

**Solutions** :

1. **SSH (recommandé)** : `git clone` + `./deploy/hostinger.sh install` (voir ci-dessus)
2. **Docker Manager → Compose from URL** : URL GitHub du dépôt entier  
   `https://github.com/AdrienHoyoux/Riflet-Automobile`  
   (pas l'URL raw du seul fichier compose)
3. Nom du projet : **`riflet-automobile`** (sans faute de frappe)

Le bouton Deploy/Update doit lancer un **build** (5–10 min), pas seulement un pull MySQL.
