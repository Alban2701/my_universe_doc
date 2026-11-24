# TODO — My Universe Doc

État des lieux du 24/11/2026. Les tâches sont classées par priorité ; chaque ligne indique le ou les fichiers concernés.

Légende : 🔴 critique (sécurité) · 🟠 important · 🟢 confort / nettoyage

---

## 1. Sécurité 🔴

### Comptes utilisateurs

- [x] Supprimer `PATCH /user/{user_id}` (n'importe qui pouvait modifier n'importe quel compte) et passer le front sur `/user/myself`
  - `backend/src/routes/user.py`, `frontend/src/pages/UpdatePassword.tsx`
- [x] Retirer le champ « id » et l'état `id` du formulaire de changement de mot de passe (inutile depuis `/myself`, l'id envoyé est ignoré par le back)
  - `frontend/src/pages/UpdatePassword.tsx` (interface `UpdateUserPayload`, `useState<number>(1)`, input `name: "id"`, `verified_payload.id`)
- [x] Mettre à jour les requêtes Postman qui pointent encore sur `/user/1`
  - `backend/postman/collections/my-universe-doc/user/patch.request.yaml`
  - `backend/postman/collections/My Universe Doc API/User/patch.request.yaml`
- [x] Exiger le mot de passe actuel pour changer de mot de passe ou d'email
  - `backend/src/models/user.py` (nouveau modèle, ex. `UpdatePassword`), `backend/src/services/user.py` (`patch_user`), `backend/src/routes/user.py` (`patch_myself`), `frontend/src/pages/UpdatePassword.tsx`
- [x] Ne plus accepter `id`, `created_at`, `updated_at` dans le body de `PATCH /user/myself` (utiliser un modèle dédié au lieu de `PartialUser`)
  - `backend/src/models/user.py`, `backend/src/routes/user.py`
- [ ] Ne pas révéler si un email existe au login : renvoyer un 401 unique « Invalid credentials » au lieu de 404 / 401
  - `backend/src/services/user.py` (`login`), `frontend/src/pages/Login.tsx` + `frontend/src/components/UI/Cards/BadCredentials.tsx` si le message dépend du code
- [ ] Typer la réponse de `PATCH /user/myself` avec `ReturnedUser` au lieu de `PartialUser` (le hash n'est pas renvoyé aujourd'hui, mais le champ `password: null` apparaît dans la réponse et rien n'empêche une future régression)
  - `backend/src/routes/user.py`, `backend/src/repositories/user.py` (`patch_user`)

### Sessions

- [ ] Vérifier l'expiration du token **présenté** et non du premier token de l'utilisateur (`get_token_by_user_id` lit `rows[0]`)
  - `backend/src/repositories/session_token.py`, `backend/src/services/user.py` (`is_logged_in`), `backend/src/middlewares/auth.py`
- [ ] Simplifier le middleware : une seule requête « token valide + non expiré → user » au lieu de `get_user_with_session_token` puis `is_logged_in`
  - `backend/src/middlewares/auth.py`, `backend/src/repositories/user.py` (`get_user_with_session_token`)
- [ ] Stocker un hash du token (SHA-256) en base plutôt que la valeur brute
  - `backend/src/repositories/session_token.py`, `backend/src/repositories/user.py`
- [ ] Aligner la durée du cookie (1 jour) et celle du token (7 jours)
  - `backend/src/routes/user.py` (`max_age`), `backend/src/repositories/session_token.py` (`expires_in_days`)
- [ ] Logout : `delete_cookie` avec le même `secure` que le login (actuellement `secure=False` en dur) ; décider si le logout supprime toutes les sessions ou seulement la courante
  - `backend/src/routes/user.py` (`logout`), `backend/src/services/user.py`
- [ ] Utiliser des dates timezone-aware partout (`datetime.now()` vs `datetime.now(timezone.utc)` mélangés)
  - `backend/src/repositories/session_token.py`
- [ ] Ajouter un nettoyage des tokens expirés (`delete_expired_token` n'est jamais appelé)
  - `backend/src/server.py` (lifespan / tâche périodique)

### Contrôle d'accès (aucun aujourd'hui)

- [ ] À la création d'un univers, insérer `user_universe (creator)` dans la même transaction
  - `backend/src/repositories/universe.py` (`create_universe` → `execute_transactional`), test dans `backend/tests/integration/test_universe_repository.py`
- [ ] À la création d'une entité, définir le rôle du créateur (`user_entity`) si nécessaire
  - `backend/src/repositories/entity.py`, `backend/src/repositories/user_entity.py`
- [ ] Créer un service d'autorisation (ex. `can_read_universe`, `can_edit_entity`, `can_admin_entity` en tenant compte de l'héritage parent → enfants)
  - nouveau `backend/src/services/authorization.py`, `backend/src/repositories/user_entity.py`, `backend/src/repositories/user.py` (`get_user_role`), `backend/src/factory.py`
- [ ] Brancher les vérifications (403) sur chaque route
  - `backend/src/routes/universe.py` : `GET /{id}`, `PATCH /{id}`, `DELETE /{id}`, `GET /{id}/first-entities`, `GET /{id}/entities`
  - `backend/src/routes/entity.py` : toutes les routes
  - `backend/src/routes/text_block.py` : toutes les routes
- [ ] Supprimer ou réserver à un admin les routes qui renvoient tout : `GET /universe/`, `GET /entity/`
  - `backend/src/routes/universe.py`, `backend/src/routes/entity.py` (+ services / controllers / repositories correspondants)
- [ ] Corriger `is_user_superadmin_universe` : il renvoie `True` dès qu'un rôle existe, même `NULL` ou `contributor`
  - `backend/src/services/universe.py`
- [ ] Corriger `is_super_admin` : lève une erreur si l'utilisateur n'a aucun rôle dans l'univers (au lieu de renvoyer `False`)
  - `backend/src/services/user.py`

### Secrets et données

- [ ] Ne plus écrire le mot de passe de la base dans les logs (`print(self.conninfo)`)
  - `backend/src/db_connection.py` ligne 38
- [ ] Ne plus logger les patchs utilisateur (`print(model_patch)` contient le hash du mot de passe)
  - `backend/src/repositories/user.py` (`patch_user`)
- [ ] Sortir les identifiants de la base du compose : variables dans un `.env` (gitignoré) + `env_file`
  - `docker-compose.yaml`, `docker-compose-example.yaml`, nouveau `.env.example`
- [ ] Retirer `docker-compose.yaml` de l'index git (il est dans le `.gitignore` mais toujours suivi) : `git rm --cached docker-compose.yaml`
  - `docker-compose.yaml`, `.gitignore`
- [ ] Ne plus charger le jeu de démo (4 comptes avec le mot de passe « azer ») en production : séparer schéma et seed
  - `backend/src/data/99.sql` → déplacer dans un dossier `seed/` monté uniquement par `backend/docker-compose.test.yaml` et `e2e/docker-compose.e2e.yaml`
  - `docker-compose.yaml`, `docker-compose-example.yaml` (volume `./backend/src/data:/docker-entrypoint-initdb.d`)
- [ ] Ajouter une limitation des tentatives de connexion (rate limiting sur `/user/login` et `/user/signup`)
  - `frontend/nginx.conf` (`limit_req_zone`) ou middleware backend
- [ ] Ajouter `Strict-Transport-Security` une fois le HTTPS en place
  - `frontend/nginx.conf`

---

## 2. Déploiement & infra 🟠

- [ ] Copier le code dans l'image backend au lieu de le monter en volume (`COPY . .`) ; corriger `CMD`
  - `backend/Dockerfile`, `backend/.dockerignore`
- [ ] Retirer les volumes `.:/app` des services `api` et `frontend` (inutile pour nginx, dangereux en prod) et la `command` qui pointe sur `backend/start_uvicorn.py`
  - `docker-compose.yaml`, `docker-compose-example.yaml`
- [ ] Utiliser un utilisateur non-root dans l'image backend
  - `backend/Dockerfile`
- [ ] Mettre en place le HTTPS (le cookie `secure` l'exige hors `IN_DEV`) : Caddy / certbot / reverse proxy
  - `frontend/nginx.conf`, `docker-compose.yaml`, `deployment.md`
- [ ] Ajouter `restart: unless-stopped` sur `api` et `frontend`
  - `docker-compose.yaml`, `docker-compose-example.yaml`
- [ ] Harmoniser la healthcheck de la base (`pg_isready -U postgres` en dur vs `$$POSTGRES_USER`)
  - `docker-compose.yaml`
- [ ] Décider du sort de `backend/docker-compose.yaml` (doublon de la stack racine, mêmes noms de conteneurs `myd_api` / `myd_db`) : supprimer ou renommer en `docker-compose.dev.yaml` avec des noms distincts
  - `backend/docker-compose.yaml`
- [ ] Prévoir une sauvegarde de la base (`pg_dump` planifié)
  - nouveau script `scripts/backup.sh`, `deployment.md`
- [ ] Mettre en place un outil de migrations (Alembic, dbmate…) : `00.sql` + `01.sql` ne sont joués qu'à la création du volume
  - `backend/src/data/`, `backend/requirements.txt`

---

## 3. CI 🟠

- [ ] Corriger le déclencheur `pull_request` du lint frontend (pointe sur `backend/**` et `frontend-integration-test.yml` qui n'existe pas)
  - `.github/workflows/frontend-lint.yml` → `paths: ["frontend/**", ".github/workflows/frontend-lint.yml"]`
- [ ] Aligner la version de Python : CI en 3.12.10, Dockerfile en 3.13.13, README « 3.13 minimum »
  - `.github/workflows/unit-integration-test.yml`, `.github/workflows/e2e-test.yml`, `backend/Dockerfile`, `README.md`
- [ ] Ajouter un job `pnpm build` (+ `tsc --noEmit`) pour détecter les erreurs de typage du front
  - `.github/workflows/frontend-lint.yml`
- [ ] Remplacer la boucle « Wait for DB » par `docker compose up -d --wait`
  - `.github/workflows/unit-integration-test.yml`
- [ ] Ajouter `ruff format --check` au job lint
  - `.github/workflows/unit-integration-test.yml`

---

## 4. Backend — qualité du code 🟢

- [ ] Supprimer le script de debug qui hache « azer » à l'import
  - `backend/src/utils/pw_hash.py`
- [ ] Retirer `pytest` et `colorama` des dépendances de prod ; `PyJWT` est inutilisé
  - `backend/requirements.txt`
- [ ] Remplacer les `print` / `traceback.print` par le module `logging`
  - `backend/src/routes/*.py`, `backend/src/db_connection.py`, `backend/src/middlewares/auth.py`, `backend/start_uvicorn.py`
- [ ] **Centraliser la gestion des erreurs** (aujourd'hui triplée : le service lève une `HTTPException`, le controller l'attrape et la relève, la route refait pareil, et les 500 renvoient `str(e)`, donc le détail SQL, au client)
  - [ ] Définir les exceptions métier : `NotFoundError`, `ForbiddenError`, `ConflictError`, `InvalidCredentialsError` (garder `SessionExpiredError`, `SessionNotFoundError`, `UserNotFoundError`)
    - `backend/src/errors/errors.py`
  - [ ] Faire lever ces exceptions par les services à la place des `HTTPException` (les services ne doivent plus importer FastAPI)
    - `backend/src/services/entity.py` (17 occurrences), `backend/src/services/text_block.py` (8), `backend/src/services/user.py` (5), `backend/src/services/universe.py` (2)
  - [ ] `unoptional(..., to_raise="HttpException")` lève une 404 HTTP depuis un utilitaire : remplacer par `NotFoundError`
    - `backend/src/utils/unoptional.py`, `backend/src/middlewares/auth.py` (seul appelant avec `"HttpException"`)
  - [ ] Ajouter les exception handlers globaux : `errors.Error` → 404 / 403 / 409 / 401 selon une table de correspondance ; `Exception` → log + 500 avec un message générique
    - `backend/src/server.py`
  - [ ] Supprimer tous les `try/except` des controllers (le 404 sur `None` est déjà levé par le service, ne pas le tester deux fois)
    - `backend/src/controllers/entity.py`, `backend/src/controllers/text_block.py`, `backend/src/controllers/universe.py`, `backend/src/controllers/user.py`
  - [ ] Supprimer tous les `try/except` des routes : une route = récupérer les entrées → appeler le controller → renvoyer le résultat (seule exception : la gestion des cookies dans `login` / `logout`)
    - `backend/src/routes/entity.py`, `backend/src/routes/text_block.py`, `backend/src/routes/universe.py`, `backend/src/routes/user.py`
  - [ ] Décider du rôle des controllers une fois vidés : les garder (conversion modèle métier → modèle de réponse, ex. `ReturnedUser`) ou appeler directement les services depuis les routes
    - `backend/src/controllers/*.py`, `backend/src/factory.py`
  - [ ] Garder les `JSONResponse` dans le middleware d'auth : il s'exécute avant FastAPI, les exception handlers ne s'appliquent pas à lui
    - `backend/src/middlewares/auth.py`
  - [ ] Adapter les tests qui attendent une `HTTPException` (`pytest.raises(NotFoundError)` etc.)
    - `backend/tests/units/services/test_universe_service.py`, `backend/tests/units/services/test_user_service.py`, `backend/tests/units/utils/test_unoptional.py`
- [ ] Remplacer `GET /user/logout` par `POST` (action avec effet de bord)
  - `backend/src/routes/user.py`, `frontend/src/components/UI/Cards/ProfileActionCard.tsx` (ligne 15), Postman
- [ ] Corriger les origines CORS (slash final → ne matchent jamais)
  - `backend/src/server.py` : `"http://localhost:5173"`, `"http://localhost:5174"`
- [ ] Ajouter une vraie route `/health` (qui teste la base) et l'utiliser dans les healthchecks
  - `backend/src/server.py`, `docker-compose.yaml`, `docker-compose-example.yaml`, `e2e/docker-compose.e2e.yaml`
- [ ] Unifier les imports (`from src.models…` vs `from models…` mélangés, d'où le `pythonpath = . src`)
  - `backend/src/**/*.py`, `backend/pytest.ini`, `backend/start_uvicorn.py`
- [ ] Uniformiser la langue des docstrings (FR dans `services/universe.py`, EN ailleurs)
  - `backend/src/services/universe.py`, `backend/src/db_connection.py`
- [ ] Nettoyer le code commenté
  - `backend/start_uvicorn.py` (bloc log-level)
- [ ] Corriger le schéma : `DEFAULT 'now()'` (chaîne) → `DEFAULT NOW()`, et `updated_at` sans valeur par défaut
  - `backend/src/data/00.sql` (ou future migration)
- [ ] La table `differences` n'a qu'un `id` et `commits` n'est lié à aucune entité / univers : compléter le modèle avant d'implémenter la validation
  - `backend/src/data/00.sql`, `backend/src/models/commit.py`

---

## 5. Frontend — qualité du code 🟢

- [ ] Supprimer la page de démo `/dnd`
  - `frontend/src/pages/DragAndDrop.tsx`, `frontend/src/App.jsx` (route `/dnd`)
- [ ] Supprimer la dépendance `dotenv` (inutilisée)
  - `frontend/package.json`, `frontend/pnpm-lock.yaml`
- [ ] Vérifier / supprimer les fichiers non utilisés
  - `frontend/src/assets/react.svg`, `frontend/public/vite.svg`, `frontend/src/App.css`, `frontend/src/globals.css`
- [ ] Retirer les `console.log` (~30)
  - `frontend/src/fetchers.ts`, `frontend/src/pages/{Login,Signup,UpdatePassword,MyDoc}.tsx`, `frontend/src/components/UI/Modals/**`, `frontend/src/components/UI/Panels/PanelUniverse.tsx`, `frontend/src/components/UI/Button/ProfileButton.tsx`
- [ ] Centraliser les appels API dans `fetchers.ts` (doublons dans les modales, `PanelEntity`, `DnDTextBlock`, `MyDoc`)
  - `frontend/src/fetchers.ts` + composants cités
- [ ] Ajouter `credentials: "include"` à `fetchMe` et aux `fetch("/api/user/me")`
  - `frontend/src/fetchers.ts`, `frontend/src/pages/MyDoc.tsx`
- [ ] `fetchSignup` avale l'erreur et renvoie `undefined` → la relancer
  - `frontend/src/fetchers.ts`
- [ ] Passer `App.jsx` / `main.jsx` en `.tsx`
  - `frontend/src/App.jsx`, `frontend/src/main.jsx`, `frontend/index.html`
- [ ] Corriger le `tsconfig` (`module: commonjs` → `ESNext`, `moduleResolution: bundler`, `strict`, alias `paths` à suffixer par `/*`)
  - `frontend/tsconfig.json`
- [ ] Réactiver la règle Biome `noUnusedImports`
  - `frontend/biome.json`
- [ ] Afficher les erreurs à l'utilisateur au lieu de `throw` dans un handler (ex. mots de passe différents)
  - `frontend/src/pages/UpdatePassword.tsx`, `frontend/src/pages/Signup.tsx`

---

## 6. Fonctionnalités à ajouter 🟠

Par ordre logique (chaque étape s'appuie sur la précédente).

- [ ] **Édition persistante des text blocks** : sauvegarder contenu et ordre (l'API existe : `PATCH /text-block/{id}`, `PATCH /text-block/`), création et suppression de blocs
  - `frontend/src/components/UI/TextBlock/DnDTextBlock.tsx` (`handleDragEnd`, `handleTextChange` ne font que du state local), `frontend/src/components/UI/TextBlock/TextBlocks.tsx`, `frontend/src/fetchers.ts`
- [ ] **Rendu Markdown** des blocs (le schéma indique `content` en markdown) avec bascule lecture / édition
  - `frontend/src/components/UI/TextBlock/TextBlocks.tsx`, `frontend/package.json` (ex. `react-markdown`)
- [ ] **Gestion des membres et invitations** : routes + service (le repository existe), UI d'invitation / acceptation
  - nouveaux `backend/src/routes/invitation.py`, `backend/src/services/invitation.py`, `backend/src/controllers/invitation.py`, `backend/src/factory.py`, `backend/src/server.py` ; `backend/src/repositories/invitation.py` ; UI dans `frontend/src/components/UI/Panels/PanelSettings.tsx`
- [ ] **Attribution des rôles** (univers et entités) via l'UI
  - `backend/src/repositories/user_entity.py` (ajouter insert / update / delete), `backend/src/routes/universe.py`, `backend/src/routes/entity.py`, front : `PanelSettings.tsx`
- [ ] **Visibilité par bloc** (`user_text_block`) et **noms non découverts** (`not_discovered_name`) appliqués côté API pour les lecteurs
  - `backend/src/repositories/text_block.py`, `backend/src/repositories/entity.py`, `backend/src/services/entity.py`, `backend/src/services/text_block.py`
- [ ] **Commentaires** (entité / bloc / réponses) : routes + service + UI (le repository existe)
  - nouveaux `backend/src/routes/comment.py`, `backend/src/services/comment.py`, `backend/src/controllers/comment.py` ; `backend/src/repositories/comment.py` ; nouveau composant front
- [ ] **Commits & validation** : un éditeur propose, un admin accepte / refuse, calcul des différences
  - `backend/src/data/00.sql` (compléter `commits` / `differences`), `backend/src/repositories/commit.py`, nouveaux route / service / controller, UI de revue
- [ ] **Versionnement de l'univers** (champ `version`, actuellement forcé à `1` à la création)
  - `backend/src/repositories/universe.py`
- [ ] **Profil utilisateur** : modifier bio / avatar (`picture` en `bytea`, à envisager en fichier)
  - `frontend/src/pages/UpdatePassword.tsx` → page profil, `backend/src/routes/user.py`

---

## 7. Tests 🟠

- [ ] Tests des routes avec `httpx.AsyncClient` / `TestClient` (aucun aujourd'hui), en particulier les 401 / 403
  - nouveau `backend/tests/api/`
- [ ] Tests unitaires des services entity et du futur service d'autorisation
  - nouveaux `backend/tests/units/services/test_entity_service.py`, `test_authorization_service.py`
- [ ] Test d'intégration : la création d'un univers crée bien le rôle `creator`
  - `backend/tests/integration/test_universe_repository.py`
- [ ] Tests e2e : login / logout / signup, changement de mot de passe, édition et réordonnancement de blocs, refus d'accès à un univers d'un autre utilisateur
  - nouveaux fichiers dans `e2e/tests/`
- [ ] Ajouter un test `@pytest.mark.smoke` (référencé dans la doc mais inexistant) ou retirer le marqueur
  - `e2e/tests/test_smoke.py`, `e2e/pytest.ini`

---

## 8. Nettoyage du dépôt 🟢

- [ ] Supprimer l'export HTML du README backend
  - `backend/README.html`
- [ ] Garder une seule collection Postman (doublon `My Universe Doc API` / `my-universe-doc`) et la mettre à jour (text-block, universe…)
  - `backend/postman/collections/`
- [ ] Corriger ou supprimer `.gitattributes` (contient des extensions sans attribut, sans effet)
  - `.gitattributes`
- [ ] Nettoyer le `.gitignore` racine (template Python générique : Django, Flask, Scrapy, Marimo…) et ajouter `node_modules/`, `dist/`, `e2e/test-results/`
  - `.gitignore`

---

## 9. Documentation 🟠

- [ ] **README racine**
  - `README.md` :
    - étape « copier `docker-compose-example.yaml` → `docker-compose.yaml` et `.env.example` → `.env` »
    - aligner la version de Python
    - lister les **trois** workflows (le lint frontend manque dans « defined by two workflows »)
    - mentionner les comptes de démo (`alban@mail.com` / `azer`…) et qu'ils ne doivent pas exister en prod
    - ajouter une section « État d'avancement / Roadmap » (cf. section 6)
    - ajouter le tableau des technos
- [ ] **README backend** : réécrire (en anglais, comme le reste)
  - `backend/README.md` : phrase inachevée « Devrait s'afficher des message », port 8000 annoncé alors qu'il n'est pas exposé dans la stack racine, ajouter l'architecture routes → controllers → services → repositories, les variables d'environnement (`POSTGRES_*`, `DATABASE_NAME`, `SERVER_PORT`, `IN_DEV`), le lancement local (`py -3.13 -m venv`, `start_uvicorn.py --reload`), le lien vers Swagger `/docs`
- [ ] **README frontend** : remplacer le template Vite (parle d'ESLint)
  - `frontend/README.md` : scripts pnpm, proxy `/api` → `localhost:8000`, alias (`@my_types`, `@components`, `@panels`), Biome, organisation `components/UI`, `Features`, `Shared`, `pages`
- [ ] **README e2e** : `tests/test_smoke.py` et `pytest -m smoke` n'existent pas ; l'arbre doit lister `test_create_entity.py` ; le bloc d'arborescence est marqué ` ```mermaid ` au lieu de ` ```text `
  - `e2e/README.md`
- [ ] **Déploiement**
  - `deployment.md` :
    - ajouter la configuration des secrets (`.env`) avant le `docker compose up`
    - préciser de ne pas charger le seed de démo
    - ajouter HTTPS (+ `ufw allow 443/tcp`) et les sauvegardes
    - section « Clean Apache » → simple vérification du port 80 (Apache n'est pas installé par défaut sur Ubuntu Server)
    - `enp0s3` est propre à VirtualBox : utiliser `hostname -I`
    - procédure de mise à jour (`git pull` + `docker compose up -d --build`)
- [ ] **À créer** : doc du modèle de données et des rôles (reprendre les `COMMENT ON` de `00.sql`, préciser implémenté / prévu)
  - nouveau `docs/data-model.md`
- [ ] **À créer** : guide de contribution (branches `main` / `dev`, CI bloquante, conventions de commit, lint)
  - nouveau `CONTRIBUTING.md`
- [ ] Mettre à jour la date de consultation de la doc Docker (« visited at 19th of May 2026 »)
  - `deployment.md`
