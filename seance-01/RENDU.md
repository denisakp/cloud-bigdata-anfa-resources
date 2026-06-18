# Rendu Séance 1
**Nom et prénom :** SENOU Kokou Audrey
## Résumé de la séance

## Étapes principales
- creation et lancement  de l image MinIO sur docker
- l administration de MinIO en commandeavec mc
- preparation du référentiel d'Anfa via Python
- mise en place de docker-compose
## Capture d'écran
## Difficultés rencontrées
- lors de la creation du fichier docker-compose j ai une un probleme d indentation ce qui a fait que j ai une erreur Map keys must be unique sur volumes: 
 apres avoir bien indenté ca s est corrigé
 - les commandes doivent etre lancé dans un terminal bash pas un powershell
## Exercices d'application

# Exercice 1.

1.1- D. Open source obligatoire.
Le NIST définit les critères techniques du cloud computing, pas le type de licence logicielle utilisé.

1.2- C. SaaS.
Il s'agit d'une application finale prête à l'emploi et accessible directement via un navigateur web.

1.3- D. SaaS.
Ce modèle permet d'exécuter du code à la demande basé sur des événements, sans gérer de serveur permanent.

1.4- C. Cloud hybride.
Il permet d'allier un cloud privé pour la sécurité des données bancaires et un cloud public pour l'élasticité du calcul.

1.5- B. La situation où une entreprise ne peut plus changer de fournisseur sans coûts ou risques majeurs.
C'est la définition exacte de l'enfermement propriétaire ou de la dépendance exclusive envers un fournisseur.

1.6- C. Un service open source est forcément moins performant qu'un service managé propriétaire.
C'est faux car l'open source propulse la majorité des infrastructures cloud de haute performance (ex: Linux, Kubernetes).

# Exercice 2.


Pour chacun des services suivants, indiquez son modèle de service (IaaS, PaaS, SaaS, ou FaaS) et expliquez votre choix en une ligne.

| Service | Modèle | Justification |
| :--- | :--- | :--- |
| **Google Compute Engine** | **IaaS** | Il fournit des machines virtuelles brutes où l'on gère totalement l'OS et l'infrastructure. |
| **AWS Lambda** | **FaaS** | Il exécute du code à la demande basé sur des événements sans aucune gestion de serveur. |
| **Snowflake** | **SaaS** | C'est une plateforme d'analyse de données clé en main, entièrement managée et prête à l'utilisation. |
| **Heroku** | **PaaS** | Il fournit un environnement complet pour déployer et exécuter des applications sans gérer l'infrastructure. |
| **Microsoft 365** | **SaaS** | Ce sont des applications bureautiques finales accessibles directement en ligne par les utilisateurs. |
| **Databricks** | **PaaS** | Il fournit une plateforme managée optimisée pour le développement et l'exécution de clusters Apache Spark. |
| **Microsoft Azure Functions** | **FaaS** | C'est un service de calcul serverless qui exécute du code uniquement lors du déclenchement d'événements. |
| **Tableau Online** | **SaaS** | C'est un outil de Business Intelligence accessible en ligne pour créer et consulter des tableaux de bord. |


# Exercice 3

3.1 Commande docker run
Détail des options :

-d : Mode "détaché" (detached). Lance le conteneur en arrière-plan et libère instantanément le terminal de l'hôte.

--name analyse-anfa : Assigne un nom personnalisé et unique (analyse-anfa) au conteneur pour pouvoir l'identifier, l'arrêter ou le manipuler facilement, à la place d'un ID ou d'un nom généré aléatoirement.

-p 8888:8888 : Redirige le port (mappage de ports). Il associe le port 8888 de la machine hôte au port 8888 à l'intérieur du conteneur, permettant d'accéder à l'application depuis l'extérieur.

-v /home/koffi/notebooks:/notebooks : Crée un volume de type bind mount. Il partage le dossier local /home/koffi/notebooks de la machine hôte avec le dossier /notebooks situé à l'intérieur du conteneur, assurant la persistance des fichiers créés.

-e JUPYTER_TOKEN=anfa-token : Définit une variable d'environnement au sein du conteneur. Ici, elle configure le jeton de sécurité (anfa-token) requis pour s'authentifier lors de la connexion à l'interface de Jupyter.

jupyter/pyspark-notebook : Spécifie l'image Docker officielle à télécharger (depuis Docker Hub) et à utiliser pour instancier le conteneur. Elle contient l'environnement prêt à l'emploi avec Jupyter et Apache Spark.

Explication globale de la commande :
Cette commande lance en arrière-plan un conteneur nommé analyse-anfa basé sur un environnement Jupyter préconfiguré avec Apache Spark. Elle expose l'interface Web de Jupyter sur le port 8888, sécurise son accès avec le mot de passe anfa-token, et synchronise les scripts avec le dossier local de l'utilisateur pour éviter de perdre le travail à l'arrêt du conteneur.

3.2 Lecture d'un docker-compose.yml
a. À quelles adresses (URL) ce service est-il accessible depuis le navigateur de l'hôte ?

Pour l'API MinIO (stockage) : http://localhost:9000

Pour la Console d'administration Web : http://localhost:9001 (spécifié explicitement par l'option --console-address ":9001" dans la commande).

b. Que se passe-t-il si on supprime le conteneur anfa-minio avec docker rm puis qu'on relance docker compose up -d ? Les données déposées dans MinIO sont-elles perdues ? Justifiez.
Non, les données ne sont pas perdues. * Justification : Le fichier utilise un volume Docker nommé (minio-data) déclaré de manière indépendante en bas du script. Le cycle de vie d'un volume nommé est totalement séparé de celui du conteneur ; ainsi, lorsque le conteneur est supprimé, le volume reste intact sur le disque de l'hôte et se reconnecte automatiquement au nouveau conteneur lors du prochain docker compose up.

c. Citez un problème de sécurité dans ce fichier qu'il faudrait corriger pour une utilisation en production.
Il y a deux failles majeures (vous pouvez citer l'une d'elles) :

Identifiants secrets écrits en clair : Le mot de passe de l'administrateur (secret) est inscrit directement en texte brut dans le fichier de configuration. En production, il faudrait utiliser des variables d'environnement externes (fichier .env non suivi) ou un gestionnaire de secrets (Docker Secrets).

Utilisation du tag :latest : L'image utilise la version latest. En production, cela peut provoquer des ruptures de service ou des comportements imprévus lors d'une mise à jour automatique. Il faut figer une version spécifique (ex: minio/minio:RELEASE.2026-X-X).
		
# Exercice 4

Voici le diagnostic précis pour l'étudiant :

a. Quelle est la cause précise de l'erreur ?
La cause de l'erreur InvalidAccessKeyId est l'utilisation d'identifiants incorrects dans le script Python. L'étudiant a configuré aws_access_key_id="anfa-admin" et aws_secret_access_key="anfa-password-2026", or ces clés d'accès n'existent pas ou ne correspondent à aucune clé applicative valide configurée dans l'instance MinIO pour cette API.

b. Comment corriger le code ?
Il faut remplacer les identifiants globaux par la clé applicative (Access Key) et le mot de passe secret (Secret Key) qu'il a réellement créés via l'outil mc (anfa-app-key et anfa-app-secret-2026).

c. Pourquoi MinIO refuse-t-il les identifiants anfa-admin / anfa-password-2026 dans ce contexte, alors qu'ils fonctionnent pour se connecter à la console web ?
MinIO refuse ces identifiants pour deux raisons possibles selon la configuration :

Erreur de saisie (Faute de frappe) : Si l'on regarde le fichier de configuration de l'exercice précédent (ou les configurations par défaut), le mot de passe de l'administrateur racine (Root) était secret. L'étudiant tente d'utiliser anfa-password-2026, qui n'est pas le bon mot de passe associé au compte anfa-admin.

Principe des Moindres Privilèges (Bonne pratique) : Même si le mot de passe racine était correct, la console web utilise le compte administrateur global (Root User). Pour des raisons de sécurité, les applications programmatiques (comme ce script Python via boto3) doivent utiliser des clés d'accès restreintes (Service Accounts ou App Keys) dédiées et limitées à certains buckets, et non les identifiants maîtres de l'infrastructure.

# Exercice 5

a. Deux limites concrètes de l'architecture actuelle
1.Données obsolètes (Pas de temps réel) : L'export CSV étant mensuel, les modèles prédisent la demande sur des données vieilles de plusieurs semaines, ce qui rend impossible le suivi de la demande heure par heure ou l'ajustement rapide pour les produits frais.

2.Saturation des ressources et absence de partage : L'ordinateur portable du data scientist est une ressource limitée qui ne peut pas absorber de fortes charges de calcul (pics d'activité), et centraliser les données localement empêche les autres analystes d'accéder aux résultats en temps réel.

b. Caractéristique du NIST répondant aux besoins de la direction

. Prédictions chaque heure : Libre-service à la demande (On-demand self-service), car l'infrastructure peut démarrer automatiquement les ressources de calcul chaque heure sans intervention humaine.

. Tableau de bord partagé sans installation : Accès réseau universel (Broad network access), car les analystes peuvent accéder à l'interface depuis n'importe quel appareil connecté (PC, smartphone) via un simple navigateur web.

. Augmenter la capacité lors des pics : Élasticité rapide (Rapid elasticity), car elle permet d'allouer instantanément plus de puissance de calcul le vendredi soir ou durant les fêtes, puis de la réduire ensuite.

. Maîtriser les coûts : Service mesuré (Measured service), car la PME ne paie que ce qu'elle consomme réellement (au temps de calcul exact ou au volume stocké), évitant des coûts fixes d'infrastructure.

c. Modèles de services proposés 

pour les composantsLe tableau de bord partagé -> SaaS (Software as a Service) : Utiliser une solution clé en main (comme Tableau Online ou Power BI Service) permet aux analystes d'accéder directement à l'outil via le web sans gérer de serveurs ni installer de logiciel.

Le calcul des prédictions à l'heure -> FaaS (Function as a Service) : Une fonction sans serveur (comme AWS Lambda ou Azure Functions) est idéale car elle se déclenche automatiquement chaque heure pour exécuter le script de prédiction en quelques secondes et s'arrête aussitôt, optimisant ainsi les coûts.

Le stockage des données clients -> PaaS (Platform as a Service) ou IaaS : Un modèle PaaS (comme une base de données relationnelle managée, ex: AWS RDS ou un cloud privé virtuel) est recommandé pour bénéficier de la sécurité et des sauvegardes automatisées sans avoir à gérer la maintenance physique du serveur.

d. Modèle de déploiement recommandé
Je recommande un Cloud Hybride. Il permet à la PME de stocker les données clients confidentielles sur un serveur local ou un cloud privé contrôlé à Lomé pour des impératifs de conformité réglementaire, tout en exploitant la flexibilité et la puissance d'un cloud public pour exécuter les calculs lourds de prédiction et héberger le tableau de bord.

e. Trois stratégies pour limiter le risque de vendor lock-in
Conteneuriser l'application (Docker) : Packager le code et les modèles afin qu'ils puissent être déployés instantanément chez n'importe quel fournisseur cloud.

Privilégier les briques technologiques Open Source : Utiliser des standards du marché (Python, PostgreSQL, MinIO) qui possèdent des équivalents portables partout.

Éviter les services managés propriétaires et spécifiques : Préférer des APIs standards (comme le stockage compatible S3) plutôt que des outils de stockage natifs et exclusifs à un unique fournisseur cloud.