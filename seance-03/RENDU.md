@'
# Rendu Séance 3

**Nom et prénom :** ADEOUL Koffi Prosper
**Identifiant GitHub :** prosperadeoul-hub
**Date de soumission :** 26/06/2026

## Résumé de la séance
Au cours de cette séance, l'outil Kind (Kubernetes IN Docker) a été installé afin de provisionner un cluster Kubernetes local nommé `anfa`. Après avoir configuré l'outil CLI `kubectl` sur un namespace dédié `anfa`, nous avons déployé le service de stockage objet MinIO en appliquant séquentiellement trois manifestes YAML (PersistentVolumeClaim, Deployment, et Service). Les propriétés fondamentales de Kubernetes ont été éprouvées, notamment le mécanisme de *self-healing* en supprimant un pod à chaud, la scalabilité horizontale du déploiement en passant à 3 replicas, ainsi que l'initialisation d'un Ingress Controller Nginx pour la gestion du routage réseau.

## Étapes principales
1. **Installation de Kind et kubectl, création du cluster `anfa`** : Téléchargement des outils via Windows Package Manager et initialisation du plan de contrôle Kubernetes s'exécutant au sein d'un conteneur Docker isolé.
2. **Création du namespace `anfa` et configuration de kubectl** : Isolation logique de nos futures ressources et configuration du contexte courant pour éviter l'usage systématique de l'argument `-n anfa` dans le terminal.
3. **Déploiement de MinIO via 3 manifestes YAML** : Allocation d'un volume persistant de 2 Go (`minio-pvc.yaml`), instanciation du contrôleur d'application (`minio-deployment.yaml`), et exposition réseau via un port de nœud stable (`minio-service.yaml`).
4. **Observation du self-healing après suppression manuelle d'un pod** : Élimination ciblée du pod MinIO actif et constatation de sa réinstanciation automatisée par le gestionnaire de déploiement afin de satisfaire l'état cible initial.
5. **Scaling du Deployment de 1 à 3 replicas, puis retour à 1** : Ajustement à la volée de la charge pour distribuer dynamiquement les instances de pods, puis rollback à la configuration standalone.
6. **Activation de l'Ingress Controller nginx** : Déploiement des briques d'infrastructure d'entrée Nginx adaptées au fonctionnement réseau de Kind.

## Captures d'écran

### Console MinIO accessible via port-forward
![Console MinIO](captures/console-minio.png)

### Self-healing observé
![Pod recréé](captures/self-healing.png)

### Scaling à 3 replicas
![3 replicas MinIO](captures/scaling-3-replicas.png)

## Réponses aux exercices d'application

### Exercice 1 : QCM conceptuel

* **1.1 Réponse : B. Kubernetes orchestre des conteneurs sur un cluster de machines, en s'appuyant sur un container runtime (containerd, Docker, CRI-O).**
  * *Justification :* Kubernetes n'est pas un moteur de conteneurisation en soi, mais un orchestrateur de haut niveau qui pilote et coordonne des agents d'exécution tiers (les runtimes) répartis sur plusieurs serveurs.

* **1.2 Réponse : B. etcd**
  * *Justification :* `etcd` est la base de données distribuée clé-valeur hautement disponible qui sert de source unique de vérité et stocke de façon persistante toute la configuration et l'état réel du cluster Kubernetes.

* **1.3 Réponse : C. Scheduler**
  * *Justification :* Le rôle unique du `Scheduler` est de surveiller les pods nouvellement créés sans nœud assigné et de sélectionner le nœud de calcul (Worker) le plus adapté en fonction des ressources demandées et des contraintes du cluster.

* **1.4 Réponse : C. À l'API Server.**
  * *Justification :* L'**API Server** est le point d'entrée central et l'unique composant du Control Plane avec lequel la CLI `kubectl` interagit directement pour valider, traiter et exécuter les requêtes REST.

* **1.5 Réponse : B. Le contrôleur du Deployment détecte l'écart et demande à l'API Server de recréer un pod.**
  * *Justification :* C'est le principe de la boucle de contrôle et du *self-healing* de Kubernetes : le Controller Manager compare continuellement l'état désiré (1 replica) à l'état réel (0 pod suite à la suppression) et converge automatiquement vers la consigne.

* **1.6 Réponse : B. NodePort**
  * *Justification :* Le service de type **NodePort** expose l'application à l'extérieur du cluster en ouvrant un port statique dédié (entre 30000 et 32767) directement sur l'adresse IP de chacun des nœuds physiques ou virtuels.

* **1.7 Réponse : B. Elle modifie la spécification de l'état souhaité (spec.replicas) au niveau du Deployment.**
  * *Justification :* La commande `kubectl scale` n'agit pas directement sur les pods mais met à jour de façon déclarative la ressource Deployment, qui se charge ensuite d'instancier ou de détruire les pods pour atteindre la nouvelle cible.

* **1.8 Réponse : B. Isoler logiquement des ressources au sein d'un même cluster.**
  * *Justification :* Les `Namespaces` agissent comme des frontières virtuelles pour partitionner un même cluster physique en plusieurs sous-environnements (par exemple : dev, staging, prod) sans interférence mutuelle.

* **1.9 Réponse : B. Kind crée des conteneurs Docker qui simulent des nœuds Kubernetes.**
  * *Justification :* Fidèle à son nom (*Kubernetes IN Docker*), Kind automatise l'infrastructure locale en encapsulant chaque nœud (control-plane et worker) sous la forme d'un conteneur Docker isolé contenant l'ensemble des composants requis (kubelet, container runtime, etc.).

---

### Exercice 2 : Lecture et interprétation d'un manifeste

* **2.1 Rôle de `selector.matchLabels` et son lien avec `template.metadata.labels` :**
  Le champ `selector.matchLabels` agit comme un filtre ou un critère de sélection. Il indique au contrôleur de Deployment quelles étiquettes il doit rechercher pour identifier et manager ses pods. Pour que le Deployment fonctionne correctement, cette valeur doit correspondre exactement aux étiquettes déclarées dans `template.metadata.labels`, qui définit les labels collés sur les pods lors de leur création.

* **2.2 Nombre de pods créés et comportement en cas de panne de l'un d'eux :**
  Ce manifeste demande la création de **2 pods** simultanément. Si l'un des deux pods subit une panne ou est supprimé manuellement, la boucle de contrôle du Deployment détecte immédiatement un écart entre l'état souhaité (2) et l'état réel (1). Kubernetes ordonne alors instantanément à l'API Server de recréer un nouveau pod pour restaurer la consigne.

* **2.3 L'application peut utiliser le nom d'hôte `minio` grâce au composant de DNS interne (CoreDNS) intégré nativement à Kubernetes.** Dès qu'un objet Service nommé `minio` est déclaré dans le même namespace, Kubernetes enregistre automatiquement ce nom dans son serveur DNS local, permettant aux autres pods de résoudre ce nom en l'adresse IP virtuelle stable du Service.

* **2.4 Conséquence pour l'API Python si aucun Service n'est configuré pour elle :**
  Si aucun Service n'est configuré pour l'API Python, celle-ci sera totalement isolée au sein du réseau privé du cluster. Bien qu'elle fonctionne en interne, aucun utilisateur externe, Ingress Controller ou autre application située en dehors de ses pods directs ne pourra lui envoyer de requêtes réseau ou communiquer avec elle.

* **2.5 Manifeste YAML d'un Service Kubernetes interne (type ClusterIP) pour l'API :**
  ```yaml
  apiVersion: v1
  kind: Service
  metadata:
    name: anfa-api-service
    namespace: anfa
  spec:
    type: ClusterIP
    selector:
      app: anfa-api
    ports:
      - name: http
        port: 80 
        targetPort: 8000

---

### Exercice 3 : Diagnostic

#### 3.1 Le pod qui ne démarre pas

* **a. Signification du statut `ImagePullBackOff` :**
  Ce statut signifie que Kubernetes a tenté à plusieurs reprises de télécharger (pull) l'image du conteneur depuis le registre (par exemple Docker Hub), mais que l'opération a échoué. Par conséquent, le cluster se met en phase d'attente exponentielle (BackOff) avant de faire une nouvelle tentative de téléchargement.

* **b. Cause probable du problème dans ce cas précis :**
  La cause est une erreur de frappe dans le nom de l'image spécifiée dans le manifeste : il est écrit `minio/miniooo:latest` (avec trois "o") au lieu de `minio/minio:latest`. Comme cette image n'existe pas sur le Docker Hub, Kubernetes ne peut pas la récupérer.

* **c. Commande `kubectl` pour inspecter les événements précis du pod :**
  ```powershell
  kubectl describe pod minio-7d9f8b6c5-x2k9p

#### 3.2 Le PVC qui ne se lie pas
* **a. Signification du statut Pending pour un PersistentVolumeClaim :**
    Le statut Pending (En attente) indique que la demande de stockage formulée par le PVC n'a pas encore pu être satisfaite. Kubernetes est en attente de trouver ou de créer un volume physique (PersistentVolume) qui correspond exactement aux critères demandés.

* **b. Cause probable du problème au vu du manifeste :**
    La capacité de stockage demandée est de 500 Go (storage: 500Gi). C'est une taille beaucoup trop élevée pour un environnement de développement local s'exécutant via Kind. Le provisionneur de stockage par défaut du cluster local n'a pas la capacité nécessaire disponible sur le disque dur de la machine hôte.

* **c. Commande kubectl pour inspecter la cause du blocage du PVC :**
    ```PowerShell
    kubectl describe pvc data-pvc

#### 3.3 Le port-forward qui échoue
* **a. Cause logique de l'échec de la commande port-forward :**
La commande kubectl port-forward établit une redirection réseau directe vers les pods ciblés par un service. Si le Deployment est en statut Pending, aucun pod n'est actif ni en cours d'exécution (Running). Il est donc techniquement impossible de transférer du trafic vers un conteneur qui n'existe pas encore.

* **b. Commande kubectl pour inspecter l'état et comprendre le blocage :**

    ```PowerShell
    kubectl get pods

* **c. Ordre logique des étapes de déploiement et de vérification :**

 - Appliquer les manifestes déclaratifs dans l'ordre : le stockage d'abord (minio-pvc.yaml), puis le contrôleur applicatif (minio-deployment.yaml).

 - Vérifier la bonne santé des pods avec la commande kubectl get pods pour s'assurer qu'ils passent bien au statut Running.

 - Appliquer le manifeste du Service (minio-service.yaml) pour exposer les ports.

 - Lancer la redirection de port avec kubectl port-forward une fois que l'infrastructure interne est totalement prête et active.

---

### Exercice 4 : De Docker Compose à Kubernetes

* **4.1 Nombre de manifestes Kubernetes requis pour remplacer le fichier docker-compose.yml :**
  Il est nécessaire de créer **3 manifestes Kubernetes distincts** : un manifeste `PersistentVolumeClaim` (pour la demande de stockage persistant), un manifeste `Deployment` (pour décrire le cycle de vie, l'image et l'environnement du conteneur MinIO) et un manifeste `Service` (pour exposer de manière stable les ports réseau de l'application).

* **4.2 Différence majeure entre un volume Docker Compose et un PersistentVolumeClaim (PVC) :**
  En Docker Compose, le volume est local, directement lié au démon Docker et fortement couplé au disque de la machine hôte. À l'inverse, le `PersistentVolumeClaim` de Kubernetes découple complètement le besoin applicatif de l'infrastructure physique : le développeur exprime simplement un besoin abstrait (ex: 2 Go en lecture/écriture) et Kubernetes se charge de lui attribuer un volume réel via une `StorageClass` (disque local, stockage cloud, SAN, etc.).

* **4.3 Gestion des ports réseaux entre Docker Compose (localhost) et Kind :**
  Docker Compose mappe les ports directement sur l'interface réseau de la machine hôte (`localhost`). Dans Kind, le cluster s'exécute lui-même à l'intérieur d'un conteneur Docker isolé, ce qui empêche les ports des services Kubernetes d'être immédiatement visibles sur l'hôte. C'est pourquoi il est nécessaire d'utiliser soit une commande de tunnelisation explicite comme `kubectl port-forward`, soit de configurer au préalable des mappages spécifiques (`extraPortMappings`) dans le fichier de configuration de Kind avant la création du cluster.

* **4.4 Deux apports majeurs de Kubernetes démontrés lors des manipulations du TP :**
  1. **Le Self-healing (Auto-guérison) :** Capacité du cluster à surveiller l'état des applications en continu et à recréer automatiquement un pod sain à la seconde où l'un d'eux est supprimé ou tombe en panne.
  2. **La Scalabilité horizontale (Scaling à chaud) :** Capacité d'ajuster instantanément la puissance et le nombre d'instances d'une application en une seule commande (`kubectl scale`), distribuant ainsi dynamiquement la charge réseau sans interruption de service.

---

### Exercice 5 : Mini-cas d'architecture

* **5.1 Choix de l'objet Kubernetes le plus adapté pour chaque composant :**
  * **`pipeline-anfa` : CronJob.** Ce composant doit exécuter de manière ponctuelle une tâche de traitement batch planifiée à une heure fixe (chaque nuit à 2h00) et se terminer une fois le travail fini.
  * **`anfa-api` : Deployment.** C'est une application sans état (stateless) qui nécessite de tourner en continu, d'assurer une haute disponibilité et d'ajuster son nombre d'instances de manière flexible face aux fluctuations de charge.
  * **`anfa-dashboard` : Deployment.** Bien qu'il serve à consulter Grafana en journée uniquement, il s'agit d'une application web stateless de visualisation qui doit rester active et stable pour répondre aux requêtes des utilisateurs connectés.

* **5.2 Paramètres de l'Horizontal Pod Autoscaler (HPA) pour `anfa-api` :**
  * **`minReplicas` : 2.** Assure une haute disponibilité de base et une tolérance aux pannes en évitant d'avoir un point de défaillance unique pendant les heures creuses (la nuit).
  * **`maxReplicas` : 6 ou 8.** Permet au cluster de scaler horizontalement et d'absorber sereinement le pic massif de charge à 50 req/s au moment des heures de pointe (8h-9h).
  * **`Métrique cible` : TargetCPUUtilization = 70%.** L'utilisation du processeur est un indicateur fiable et réactif pour mesurer l'intensité des requêtes HTTP entrantes sur une API Rest en Python.

* **5.3 Type de Service à choisir pour `anfa-api` parmi ClusterIP, NodePort, LoadBalancer :**
  Le choix idéal est le type **LoadBalancer**. Étant donné que le cluster s'exécute chez un fournisseur cloud managé, l'activation de ce type va automatiquement provisionner un répartiteur de charge public chez le fournisseur cloud, offrant une adresse IP publique unique et sécurisée pour rediriger directement le trafic des téléphones des conducteurs vers les pods de l'API.

* **5.4 Gestion des mises à jour sans interruption de service par Kubernetes :**
  Kubernetes gère cela de manière totalement transparente grâce à la stratégie de **Rolling Update** (mise à jour progressive). Lors du déploiement d'une nouvelle version de l'image, Kubernetes démarre un nouveau pod à côté des anciens, attend que les sondes de démarrage confirment qu'il est sain pour lui envoyer du trafic, puis détruit un ancien pod, répétant ce cycle jusqu'à ce que l'intégralité du parc applicatif soit à jour sans aucune coupure de service pour les utilisateurs.

* **5.5 Squelette du manifeste Deployment**
apiVersion: apps/v1
kind: Deployment

metadata:
  name: anfa-api
  namespace: anfa

spec:
  replicas: 3

  selector:
    matchLabels:
      app: anfa-api

  template:
    metadata:
      labels:
        app: anfa-api

    spec:
      containers:
        - name: anfa-api
          image: anfa/api:v1

          ports:
            - containerPort: 8000

          env:
            - name: MINIO_ENDPOINT
              value: "http://minio:9000"


---


## Difficultés rencontrées

* **Incompatibilité de version Kubernetes avec le pilote Cgroups (v1 vs v2)** : Lors de l'initialisation du cluster avec l'image `v1.35.1`, le composant `kubelet` a échoué à démarrer en raison de l'absence de support cgroups v2 sur l'hôte Windows. 
*Solution :* Conformément aux recommandations de secours, le cluster a été provisionné avec succès en rétrogradant de manière stable sur l'image `kindest/node:v1.29.2`.
* **Erreurs de syntaxe et d'indentation sur les manifestes YAML** : Lors du premier `kubectl apply`, des erreurs d'arborescence (`resource name may not be empty`) sont apparues. 
*Solution :* Correction rigoureuse des alignements d'espaces sous les blocs `metadata` et `spec` pour respecter la spécification stricte de Kubernetes.
* **Erreur d'interprétation des retours à la ligne (`\`) sous Windows** : La commande multi-ligne `kubectl wait` contenant des anti-slashs Linux a provoqué des erreurs d'exécution en cascade dans PowerShell. 
*Solution :* Regroupement et exécution de l'ensemble des drapeaux de la commande sur une seule ligne continue.