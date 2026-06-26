# Rendu Séance 2

**Nom :** NGARTOBAYE OUMAROU BILLY

---

# Résumé de la séance

L'objectif de cette séance était de passer de la conteneurisation manuelle à l'automatisation et à l'orchestration avancée avec Docker.

Nous avons créé une image Docker optimisée puis automatisé le déploiement d'une infrastructure complète grâce à **Docker Compose**, comprenant :

* un serveur de stockage objet **MinIO** ;
* une application Python de traitement des données ;
* un environnement **Jupyter Notebook** pour l'exploration interactive.

---

# Étapes accomplies

## 1. Dockerfile & Multi-stage

Création d'une image basée sur **python:3.11-slim** puis implémentation d'un **Dockerfile multistage** afin de réduire la taille de l'image finale.

---

## 2. Orchestration multi-services

Mise en place d'une architecture complète avec Docker Compose :

* **MinIO** : serveur de stockage objet.
* **MinIO Client (mc)** : création automatique des buckets et chargement des données initiales.
* **afa-app** : application Python utilisant Pandas et Boto3.
* **Jupyter Notebook** : environnement d'analyse des données.

---

## 3. Automatisation

Utilisation des fonctionnalités suivantes :

* `healthcheck`
* `depends_on`

afin de garantir que MinIO soit complètement démarré avant le lancement de l'application.

---

## 4. Diagnostic

Résolution de plusieurs problèmes :

* synchronisation entre les services ;
* erreurs réseau ;
* erreurs de casse dans les paramètres utilisés avec **boto3**.

---

# Résultat

L'application **afa-app** s'exécute correctement.

Elle :

* se connecte au bucket **anfa-raw** ;
* lit le fichier **bus.csv** ;
* affiche correctement son contenu grâce à **Pandas**.

Le notebook **Jupyter** permet ensuite une exploration interactive des données via le réseau interne Docker.

---

# Difficultés rencontrées

## Synchronisation asynchrone

L'application essayait d'accéder aux données avant que MinIO soit prêt.

Solution :

* ajout d'un **healthcheck** sur le service **minio** ;
* utilisation de la condition `service_completed_successfully` sur le conteneur d'initialisation.

---

## Conflits de noms

Des conteneurs existaient déjà.

Solution :

* suppression des anciens conteneurs avec :

```bash
docker rm -f
```

* renommage des services afin d'améliorer leur lisibilité.

---

# Captures d'écran

## 1. Vérification des logs de l'application

![Vérification du traitement des données par l'application](captures/verif-logs.png)

Cette capture montre l'application **afa-app** lisant correctement le fichier **bus.csv** depuis MinIO et affichant le DataFrame Pandas dans la console.

---

## 2. Exploration des données sous Jupyter

![Exploration interactive des données via Jupyter Notebook](captures/jupyter.png)

Cette capture montre le notebook **exploration_minio.ipynb** accédant aux données de MinIO via l'adresse interne :

```
http://minio:9000
```

et affichant le contenu du fichier **bus.csv**.

---

# Architecture de la solution

![Architecture de la solution](captures/architecture-solution.png)

---

# Exercices d'application - Séance 2

# Exercice 1 : QCM conceptuel

### 1.1

**Réponse : C**

Les conteneurs partagent le noyau de l'hôte, contrairement aux machines virtuelles qui possèdent leur propre noyau.

### 1.2

**Réponse : B**

Une image est le modèle (build-time) tandis qu'un conteneur est son exécution (run-time).

### 1.3

**Réponse : B**

Les **Namespaces** (PID, Mount, Network...) permettent l'isolation des processus.

### 1.4

**Réponse : A**

Les **cgroups** permettent de limiter et surveiller la consommation CPU et mémoire.

### 1.5

**Réponse : B**

Sous macOS, Docker fonctionne grâce à une machine virtuelle Linux légère.

### 1.6

**Réponse : B**

DotCloud était une plateforme PaaS ayant ouvert sa technologie de conteneurisation sous le nom de Docker.

### 1.7

**Réponse : C**

Docker a démocratisé la conteneurisation grâce à un format d'image standardisé et une interface simple.

### 1.8

**Réponse : B**

L'OCI définit les standards ouverts garantissant l'interopérabilité des conteneurs.

---

# Exercice 2 : Lecture et analyse d'un Dockerfile

## 2.1

### FROM

Définit l'image de base.

### WORKDIR

Définit le répertoire de travail du conteneur.

### COPY

Copie les fichiers de l'hôte vers le conteneur.

### RUN

Exécute une commande pendant la construction de l'image.

### EXPOSE

Indique le port utilisé par l'application.

### CMD

Définit la commande exécutée au démarrage du conteneur.

---

## 2.2

La directive **EXPOSE** est uniquement informative.

L'option :

```bash
-p
```

sert réellement à publier un port du conteneur sur la machine hôte.

---

## 2.3

### Problème 1

Image trop volumineuse :

```dockerfile
python:3.11
```

Correction :

```dockerfile
python:3.11-slim
```

### Problème 2

Le conteneur s'exécute avec les privilèges root.

Correction :

Créer un utilisateur dédié avec :

```dockerfile
USER
```

---

# Exercice 3 : Diagnostic

## 3.1

### a)

Le fichier `requirements.txt` n'est pas encore présent lorsque la commande :

```dockerfile
RUN pip install
```

est exécutée.

### b)

Il faut inverser les instructions :

```dockerfile
COPY requirements.txt .
RUN pip install -r requirements.txt
```

### c)

Chaque instruction du Dockerfile crée une couche indépendante exécutée dans l'ordre.

---

## 3.2

### a)

Dans un conteneur, `localhost` désigne le conteneur lui-même.

### b)

Il faut utiliser le nom du service Docker Compose :

```
db
```

---

# Exercice 4 : Optimisation d'image

## a)

Les problèmes identifiés sont :

1. Utilisation de `ubuntu:22.04`, trop lourde.
2. Multiplication des instructions `RUN`.
3. Installation d'outils de développement inutiles.
4. Exécution en tant que root.

---

## b)

Optimisations proposées :

* utiliser `python:3.11-slim` ;
* regrouper les commandes `apt-get` dans un seul `RUN` ;
* supprimer les fichiers temporaires avec :

```bash
rm -rf /var/lib/apt/lists/*
```

* utiliser un utilisateur non privilégié.

---

# Exercice 5 : Mini-cas d'architecture

## 5.1

### script-python

Traitement batch.

### minio

Stockage des données.

### jupyter

Exploration interactive.

---

## 5.2

Politique de redémarrage :

```
on-failure
```

Le script ne doit pas fonctionner en permanence mais doit redémarrer automatiquement en cas d'erreur.

---

## 5.3

Deux méthodes pour transmettre une date :

1. Variables d'environnement :

```bash
-e DATE=2026-06-26
```

2. Montage d'un fichier de configuration.

La méthode recommandée est l'utilisation des variables d'environnement.

---

## 5.4

Principe de responsabilité unique :

Chaque conteneur doit assurer une seule responsabilité.

Cela facilite :

* la maintenance ;
* les mises à jour ;
* le déploiement ;
* la montée en charge indépendante des services.

---

## 5.5

```yaml
services:
  script-python:
    build: .
    environment:
      - DATE=2026-06-26

  minio:
    image: minio/minio
    command: server /data

  jupyter:
    image: jupyter/datascience-notebook

    volumes:
      - ./data:/home/jovyan/work

    depends_on:
      - minio
```
