# 🐳 Rapport Docker - Environnement Labo Web Vulnérable

## 🔧 Architecture générale

L’environnement est composé de 3 services principaux :

| Service   | Rôle                        | Langage / Image       |
|-----------|-----------------------------|------------------------|
| `db`      | Base de données MariaDB     | `mariadb`       |
| `web`     | Application web vulnérable  | Image custom (Python)  |
| `attacker`| Machine d’attaque           | Image custom (base debian)    |

---

## 🌐 Réseaux Docker

| Réseau     | Contient les services            | Objectif                            |
|------------|----------------------------------|-------------------------------------|
| `backend`  | `db`, `web`                      | Communication privée app ↔ DB       |
| `frontend` | `web`, `attacker`                | Communication attaque ↔ app         |

> 🔒 Isolation réseau : L’attaquant **ne peut pas accéder à la base de données directement**.

---

## 📦 `docker-compose.yml` - (Résumé)

```yaml
networks:
  backend:
  frontend:

services:
  db:
    image: mariadb:latest
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: appdb
      MYSQL_USER: flask
      MYSQL_PASSWORD: flaskpass
    volumes:
      - ./db/init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "3306:3306"
    networks:
      - backend
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost", "-uroot", "-proot"]
      interval: 10s
      timeout: 5s
      retries: 10
      start_period: 30s

  web:
    build: ./web
    ports:
      - "8080:8080"
    depends_on:
      db:
        condition: service_healthy
    networks:
      - backend
      - frontend
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 20s

  attacker:
    build: ./attacker
    volumes:
      - ./attacker/output:/attacker/output
    depends_on:
      web:
        condition: service_healthy
    networks:
      - frontend
```

---

## ✅ Healthchecks

### `db` - MariaDB
- **Commande** : `mysqladmin ping -h localhost -uroot -proot`
- Vérifie que la base est accessible.
- `start_period`: 30s (nécessaire car MySQL est lent au démarrage)

### `web` - Serveur Python
- **Commande** : `curl -f http://localhost:8080`
- Vérifie que le serveur web répond bien.
- `start_period`: 20s

### `attacker`
- Aucun `healthcheck` (non nécessaire ici).

---

## 🧪 Test d'isolement réseau

| Depuis     | Vers       | Accessible ? | Méthode               |
|------------|------------|--------------|------------------------|
| attacker   | web        | ✅ Oui       | `curl http://web:8080` |
| attacker   | db         | ❌ Non       | `mysql -h db ...` → échec |
| web        | db         | ✅ Oui       | via MySQL Connector    |

---

## 💡 Recommandations

- ✅ **Ajouter une page dédiée `/health`** dans l’app web pour un healthcheck plus propre (évite un faux 200 sur une page d’erreur).
- ⏳ Adapter les `start_period` si tes services mettent plus de temps à démarrer.
- 🔐 Supprimer le port `3306:3306` si la base ne doit pas être exposée à l’hôte.

---

## 📌 Commandes utiles

### Vérifier l’état de santé des conteneurs :
```bash
docker ps
docker inspect --format='{{json .State.Health}}' <container_name> | jq
```

---

Rapport généré automatiquement avec ❤️ par ChatGPT.