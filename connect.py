import boto3
from dotenv import load_dotenv
import os

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION")
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
DYNAMO_TABLE = os.getenv("DYNAMO_TABLE", "AppUsers")

# Connexion DynamoDB
dynamodb = boto3.resource(
    "dynamodb",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

def get_users_table():
    """Retourne la table DynamoDB des utilisateurs."""
    return dynamodb.Table(DYNAMO_TABLE)
