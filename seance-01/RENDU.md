# Rendu séance 01

**Nom et prénom :** AHLI Kossi Sitsofe Pedro

## Résumé de la séance

A l'issue de cette première séance voici mon résumé :

- présentation et prise de contact
- explication du déroulement du cours, mise en place des termes de conduite et d'examination
- Début du cours et presentation du contexte du projet du cours : Anfa
-Points essentiels retenues : definition du cloud computing selon nsit, caractéristique essentiels du cloud,les modèles de service, modèles de déploiement, explication du piège de vendorlock-in

## Etapes principales

## Captures d'écran

![capture d'écran compte minio http://localhost:9001/browser/anfa-raw/referentiel%2Fbus.csv](captures/bucket-anfa-raw.png)

## Difficultés rencontrées

- aucune

## Exercices d'application

### Exercice 1 : QCM conceptuel

**1.1** Réponse : **D. Open source obligatoire**
Les 5 caractéristiques essentielles du NIST sont le libre-service à la demande, l'accès réseau étendu, la mutualisation des ressources, l'élasticité rapide et le service mesuré ; l'open source n'en fait pas partie, un cloud peut être 100 % propriétaire et rester conforme à la définition du NIST.

**1.2** Réponse : **C. SaaS**
Gmail est une application complète et prête à l'emploi, accessible depuis un navigateur, sans que l'utilisateur ait à gérer un quelconque serveur, runtime ou infrastructure sous-jacente.

**1.3** Réponse : **D. FaaS**
Le besoin décrit (réagir à un évènement, exécution très courte, aucun serveur dédié à maintenir en permanence) correspond exactement au modèle serverless/FaaS, facturé à l'exécution.

**1.4** Réponse : **C. Cloud hybride**
Le cloud hybride permet de garder les données sensibles et réglementées dans un environnement privé/contrôlé tout en exploitant l'élasticité du cloud public pour les traitements non sensibles.

**1.5** Réponse : **B. La situation où une entreprise ne peut plus changer de fournisseur sans coûts ou risques majeurs**
Le vendor lock-in désigne la dépendance technique ou contractuelle qui rend la migration vers un autre fournisseur coûteuse, risquée ou complexe.

**1.6** Réponse : **C. Un service open source est forcément moins performant qu'un service managé propriétaire**
La performance dépend de l'implémentation et de l'ingénierie, pas de la licence du logiciel ; de nombreuses briques open source (Kafka, Spark, Postgres...) sont aussi performantes que des équivalents propriétaires, et sont d'ailleurs souvent utilisées par les fournisseurs cloud eux-mêmes en interne.

### Exercice 2 : Classification de services

| Service | Modèle | Justification |
|---|---|---|
| Google Compute Engine (machine virtuelle) | IaaS | Fournit une VM brute : l'utilisateur gère l'OS, le réseau et tout ce qui est installé au-dessus. |
| AWS Lambda | FaaS | Exécute une fonction à la demande, en réponse à un évènement, sans aucun serveur à provisionner ni maintenir. |
| Snowflake (entrepôt de données) | PaaS | Plateforme de données managée sur laquelle on construit ses propres schémas, requêtes et pipelines, sans gérer l'infrastructure ni le moteur sous-jacent. |
| Heroku | PaaS | Permet de déployer son propre code applicatif sans gérer ni serveur, ni OS, ni configuration réseau. |
| Microsoft 365 (Word, Excel en ligne) | SaaS | Application bureautique complète et prête à l'emploi, utilisée directement via navigateur. |
| Databricks (Spark managé) | PaaS | Plateforme managée pour exécuter du code Spark/notebooks ; l'utilisateur gère son code, pas les clusters ni l'infrastructure. |
| Microsoft Azure Functions | FaaS | Équivalent d'AWS Lambda chez Microsoft : exécution de fonctions évènementielles sans gestion de serveur. |
| Tableau Online | SaaS | Outil de visualisation de données complet et prêt à l'emploi, accessible en ligne sans installation. |

### Exercice 3 : Lecture et interprétation

#### 3.1 Commande `docker run`

- `-d` : lance le conteneur en mode détaché (arrière-plan), le terminal n'est pas bloqué.
- `--name analyse-anfa` : donne un nom explicite (`analyse-anfa`) au conteneur plutôt qu'un nom aléatoire généré par Docker.
- `-p 8888:8888` : mappe le port 8888 de la machine hôte vers le port 8888 du conteneur, rendant le serveur Jupyter joignable depuis l'hôte.
- `-v /home/koffi/notebooks:/notebooks` : monte (bind mount) le dossier hôte `/home/koffi/notebooks` dans le conteneur à l'emplacement `/notebooks`, pour que les notebooks survivent à la suppression du conteneur.
- `-e JUPYTER_TOKEN=anfa-token` : définit une variable d'environnement lue par l'image, ici utilisée pour fixer le jeton d'authentification d'accès à l'interface Jupyter.
- `jupyter/pyspark-notebook` : nom de l'image Docker utilisée pour créer le conteneur (image officielle Jupyter avec PySpark préinstallé).

**Synthèse** : cette commande démarre en arrière-plan un conteneur nommé `analyse-anfa`, basé sur l'image `jupyter/pyspark-notebook`, en exposant le serveur Jupyter sur le port 8888 de l'hôte et en montant un dossier local pour persister les notebooks. L'accès à l'interface web est protégé par le jeton `anfa-token` transmis via une variable d'environnement.

#### 3.2 Lecture d'un `docker-compose.yml`

**a. URLs d'accès** : `http://localhost:9000` (API S3 de MinIO) et `http://localhost:9001` (console web d'administration MinIO), conformément au mapping de ports `9000:9000` et `9001:9001`.

**b. Suppression du conteneur puis `docker compose up -d`** : les données ne sont **pas perdues**. `docker rm` supprime uniquement le conteneur (le processus et son système de fichiers en couche), pas les volumes nommés qui lui sont attachés, sauf si on ajoute explicitement l'option `-v`. Ici, les données sont stockées dans le volume nommé `minio-data` (déclaré en bas du fichier et monté sur `/data`), qui existe indépendamment du conteneur. `docker compose up -d` recrée un nouveau conteneur `anfa-minio` et le rattache au même volume `minio-data` existant, donc les données déposées dans MinIO sont conservées.

**c. Problème de sécurité** : les identifiants `MINIO_ROOT_USER`/`MINIO_ROOT_PASSWORD` sont écrits en clair dans le fichier (mot de passe trivial `secret`), ce qui est risqué si le fichier est versionné dans un dépôt Git ou partagé. En production, il faudrait utiliser un mot de passe fort, ne pas committer ces secrets (variables passées via un `.env` non versionné ou un gestionnaire de secrets), et exposer la console (port 9001) derrière HTTPS/un reverse proxy plutôt qu'en HTTP direct.

### Exercice 4 : Diagnostic

**a. Cause précise** : l'erreur `InvalidAccessKeyId` signifie que la chaîne `anfa-admin` utilisée comme `aws_access_key_id` n'est pas reconnue par MinIO comme une clé d'accès valide pour l'API S3. Le script utilise les identifiants root (`anfa-admin` / `anfa-password-2026`) au lieu de la clé applicative dédiée que l'étudiant a lui-même créée via `mc` (`anfa-app-key` / `anfa-app-secret-2026`), et c'est cette dernière qui est attendue pour un accès programmatique.

**b. Correction du code** :

```python
import boto3

s3 = boto3.client(
    "s3",
    endpoint_url="http://localhost:9000",
    aws_access_key_id="anfa-app-key",
    aws_secret_access_key="anfa-app-secret-2026",
    region_name="us-east-1",
)
s3.upload_file("trajets.csv", "anfa-raw", "trajets.csv")
```

**c. Pourquoi le root fonctionne sur la console mais pas ici** : la console web s'authentifie avec les identifiants root réellement actifs sur le serveur, donc si l'étudiant saisit exactement les bons identifiants dans le navigateur, la connexion réussit. Mais utiliser le compte root pour l'accès applicatif est une mauvaise pratique : c'est précisément pour cela que des clés applicatives dédiées (créées via `mc`) existent, afin d'appliquer le principe de moindre privilège (l'application n'a accès qu'au strict nécessaire), de pouvoir révoquer l'accès d'une application sans toucher au compte root, et de tracer les accès par clé. Par ailleurs, si les variables `MINIO_ROOT_USER`/`MINIO_ROOT_PASSWORD` ont été modifiées après la création du volume de données, MinIO ne les réinitialise pas (elles ne sont lues qu'au tout premier démarrage sur un volume vide) : un identifiant root déclaré dans le `docker-compose.yml` peut donc ne plus correspondre à celui réellement actif sur le serveur, ce qui peut expliquer un rejet côté API alors que la console a été testée avec d'autres identifiants.

### Exercice 5 : Mini-cas d'architecture

**a. Deux limites concrètes de l'architecture actuelle**

1. Le traitement est mensuel et manuel (export CSV une fois par mois, traité sur un PC) : il n'y a aucune ingestion continue de données, ce qui est incompatible avec le besoin de prédictions quasi temps réel (chaque heure).
2. La capacité de calcul est limitée au PC unique du data scientist : aucune élasticité pour absorber les pics (vendredi soir, fêtes), aucun partage natif des résultats avec les autres analystes, et un point de défaillance unique (panne du PC, absence de Toyi).

**b. Besoin de la direction → caractéristique NIST**

| Besoin | Caractéristique NIST | Pourquoi |
|---|---|---|
| Prédictions quasi temps réel chaque heure | Libre-service à la demande | Le calcul peut être déclenché automatiquement (ex. job planifié) chaque heure, sans attendre une intervention manuelle d'un administrateur côté fournisseur. |
| Tableau de bord partagé sans installation locale | Accès réseau étendu | Le dashboard est consultable par tous les analystes via navigateur, depuis n'importe quel poste, sans rien installer. |
| Augmenter la capacité de calcul lors des pics | Élasticité rapide | Les ressources de calcul peuvent être ajoutées ou retirées automatiquement et rapidement pour absorber les pics du vendredi soir et des fêtes. |
| Maîtriser les coûts | Service mesuré | La facturation à l'usage réel (pay-as-you-go) permet de payer uniquement les ressources consommées et d'ajuster les coûts à l'activité réelle. |
| Conserver les données clients dans un environnement contrôlé | Mutualisation des ressources *(fit le plus faible)* | C'est ici la caractéristique la plus en tension avec le besoin : la mutualisation implique de ne pas contrôler le matériel physique sous-jacent. Répondre réellement à cette exigence de conformité relève donc davantage du choix du modèle de **déploiement** (cloud privé/hybride, voir d.) que d'une caractéristique NIST en tant que telle. |

**c. Modèle de service par composant**

- **(i) Tableau de bord partagé** → **SaaS** : besoin d'un outil de visualisation complet et prêt à l'emploi (type Tableau Online/Power BI), utilisable directement par les analystes sans rien installer ni administrer.
- **(ii) Calcul des prédictions à l'heure** → **FaaS** : un traitement court, déclenché périodiquement (toutes les heures), correspond bien au modèle serverless qui ne facture que le temps d'exécution sans maintenir de serveur en continu.
- **(iii) Stockage des données clients** → **IaaS** (stockage objet/bloc managé, type S3/MinIO) : ce niveau d'infrastructure laisse à l'entreprise le contrôle du chiffrement, des politiques d'accès et de la localisation des données, ce qui est important pour la conformité, tout en évitant de gérer le matériel physique.

**d. Modèle de déploiement recommandé : cloud hybride.**
Les données clients sensibles restent dans un environnement privé/contrôlé (cloud privé ou on-premise) pour satisfaire la contrainte de conformité, tandis que les traitements de prédiction et le tableau de bord — qui ont surtout besoin d'élasticité et d'accès partagé — peuvent s'exécuter sur du cloud public en consommant des données agrégées/anonymisées. Cela permet de concilier la maîtrise réglementaire des données sensibles avec l'élasticité et la mutualisation des coûts offertes par le cloud public.

**e. Trois stratégies pour limiter le vendor lock-in**

1. Privilégier des briques open source et des formats de données standards et portables (PostgreSQL, Parquet/CSV, API compatibles S3 comme MinIO, Kafka) plutôt que des services 100 % propriétaires fermés.
2. Conteneuriser les applications (Docker/Kubernetes) afin qu'elles puissent être redéployées telles quelles chez un autre fournisseur ou en interne, sans réécriture.
3. Décrire l'infrastructure en *Infrastructure as Code* (ex. Terraform) de façon déclarative et la plus indépendante possible des API propriétaires d'un seul fournisseur, afin de pouvoir reproduire l'environnement ailleurs si nécessaire.
