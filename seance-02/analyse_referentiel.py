import boto3
import pandas as pd
import io


# Configuration (Note : dans le docker-compose, on pointera vers le service 'minio')
s3 = boto3.client(
    "s3",
    endpoint_url="http://minio:9000",
    aws_access_key_id="anfa-admin",  
    aws_secret_access_key="anfa-password-2026",  
)

def analyser():
    
    print("Lecture du fichier bus.csv depuis MinIO...")
    obj = s3.get_object(Bucket="anfa-raw", Key="referentiel/bus.csv")
    df = pd.read_csv(io.BytesIO(obj['Body'].read()))
    print(df.head())

if __name__ == "__main__":
    analyser()

    