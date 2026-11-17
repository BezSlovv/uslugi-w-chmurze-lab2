
import boto3
import html
import os

BUCKET = "raport-koszykow-szablony"
KEY = "template.html"


def lambda_handler(event, context):
    # Odczyt parametru z adresu URL
    params = event.get("queryStringParameters") or {}
    imie = (params.get("imie") or "").strip()

    # Brak imienia - blad HTTP 400
    if not imie:
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "text/plain; charset=utf-8"
            },
            "body": "Podaj imie w adresie, np. ?imie=Ola"
        }

    # Polaczenie z S3 w LocalStack
    endpoint = os.environ.get(
        "AWS_ENDPOINT_URL",
        "http://localhost.localstack.cloud:4566"
    )
    s3 = boto3.client("s3", endpoint_url=endpoint)

    # Pobranie szablonu z bucketu
    response = s3.get_object(Bucket=BUCKET, Key=KEY)
    template = response["Body"].read().decode("utf-8")

    # Bezpieczne podstawienie imienia do HTML
    safe_imie = html.escape(imie, quote=True)
    result = template.replace("{{IMIE}}", safe_imie)

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "text/html; charset=utf-8"
        },
        "body": result
    }
