"""  # je décris le but du script: déposer le référentiel statique dans MinIO
upload_referentiel.py  # je donne le nom du fichier
Dépose le référentiel statique d'Anfa (lignes, arrêts, bus, tarifs)  # j'explique ce que fait le script
dans un bucket MinIO local.  # je précise la destination
"""

from pathlib import Path  # j'importe Path pour manipuler les chemins de fichiers

import boto3  # j'importe boto3 pour interagir avec S3/MinIO
from botocore.exceptions import ClientError  # j'importe l'exception ClientError pour gérer les erreurs

MINIO_ENDPOINT = "http://localhost:9000"  # je définis l'endpoint MinIO local
MINIO_ACCESS_KEY = "anfa-app-key"  # je définis la clé d'accès pour MinIO
MINIO_SECRET_KEY = "anfa-app-secret-2026"  # je définis la clé secrète pour MinIO
BUCKET_NAME = "anfa-raw"  # je définis le nom du bucket cible

s3 = boto3.client(  # je crée un client S3 pointant vers MinIO
    "s3",
    endpoint_url=MINIO_ENDPOINT,
    aws_access_key_id=MINIO_ACCESS_KEY,
    aws_secret_access_key=MINIO_SECRET_KEY,
    region_name="us-east-1",
)

# bloc 2 : verifier l'accessibilité du bucket et uploader les fichiers

def verifier_bucket(nom_bucket: str) -> None:  # je vérifie que le bucket existe et est accessible
    try:
        s3.head_bucket(Bucket=nom_bucket)  # j'interroge le bucket pour confirmer son accessibilité
        print(f"[OK]   Bucket '{nom_bucket}' accessible.")  # j'indique que le bucket est accessible
    except ClientError as e:
        print(f"[ERREUR] Bucket '{nom_bucket}' inaccessible : {e}")  # je signale l'erreur rencontrée
        print("         Avez-vous bien créé le bucket et la clé applicative en partie 3 ?")  # je donne une piste de résolution
        raise  # je remonte l'exception après l'affichage

def uploader_fichier(chemin_local: Path, cle_objet: str) -> None:  # j'uploade un fichier local vers le bucket
    print(f"[UP]   {chemin_local.name} -> s3://{BUCKET_NAME}/{cle_objet}")  # j'affiche l'opération en cours
    s3.upload_file(  # j'appelle l'API pour envoyer le fichier
        Filename=str(chemin_local),
        Bucket=BUCKET_NAME,
        Key=cle_objet,
    )


# bloc 3 : lister les objets du bucket

def lister_objets(nom_bucket: str) -> None:  # je liste les objets présents dans le bucket
    print(f"\nContenu du bucket '{nom_bucket}'")  # j'affiche un en-tête
    reponse = s3.list_objects_v2(Bucket=nom_bucket)  # je récupère la liste des objets
    if "Contents" not in reponse:  # j'inspecte la réponse pour savoir si le bucket est vide
        print(" (vide)")  # j'indique que le bucket est vide
        return
    for obj in reponse["Contents"]:  # je parcours chaque objet retourné
        taille_ko = obj["Size"] / 1024  # je convertis la taille en kilo-octets
        print(f"  - {obj['Key']:35s} ({taille_ko:6.1f} Ko)")  # j'affiche la clé et la taille

# bloc 4 : Programme principal

def main() -> None:  # je définis le flux principal du script
    dossier_data = Path(__file__).parent.parent / "data" / "referentiel"  # je construis le chemin vers le dossier des données
    
    verifier_bucket(BUCKET_NAME)  # je vérifie que le bucket est accessible
    
    fichiers_a_uploader = sorted(dossier_data.glob("*.csv"))  # je liste et trie les fichiers CSV à uploader
    if not fichiers_a_uploader:  # j'ai aucune source à uploader
        print(f"[ERREUR] Aucun fichier CSV trouvé dans {dossier_data}")  # j'affiche une erreur si aucun fichier
        return
        
    for chemin in fichiers_a_uploader:  # je parcours chaque fichier trouvé
        cle = f"referentiel/{chemin.name}"  # je construis la clé S3 sous le préfixe referentiel/
        uploader_fichier(chemin, cle)  # j'uploade le fichier
        
    lister_objets(BUCKET_NAME)  # je liste le contenu du bucket après upload
    print(f"\n[OK]   Upload du référentiel Anfa terminé.")  # je confirme la fin du processus

if __name__ == "__main__":  # je vérifie si le script est exécuté directement
    main()  # j'exécute la fonction principale

