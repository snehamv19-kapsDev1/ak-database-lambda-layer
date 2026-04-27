import boto3
import json

s3 = boto3.client("s3")

BUCKET = "jsvm-database"

class S3Repository:

    def get_key(self, env, table):
        return f"{env}-{table}-db.json"

    def read_db(self, env, table):
        key = self.get_key(env, table)

        try:
            obj = s3.get_object(Bucket=BUCKET, Key=key)
            return json.loads(obj["Body"].read().decode("utf-8"))
        except s3.exceptions.NoSuchKey:
            return {"items": []}

    def write_db(self, env, table, data):
        key = self.get_key(env, table)

        s3.put_object(
            Bucket=BUCKET,
            Key=key,
            Body=json.dumps(data),
            ContentType="application/json"
        )