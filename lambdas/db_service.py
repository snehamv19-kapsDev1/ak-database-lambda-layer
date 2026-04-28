import boto3
import json
import os

s3 = boto3.client("s3")

BUCKET = os.environ["BUCKET"]
ENV = os.environ["ENV"]
SERVICE = os.environ["SERVICE"]

PREFIX = f"{ENV}-jsvm-database/{ENV}-{SERVICE}-table"


########################################
# CRUD
########################################
def create_item(item):
    item_id = item["id"]
    key = f"{PREFIX}/{item_id}.json"
    print("BUCKET " + BUCKET)
    s3.put_object(
        Bucket=BUCKET,
        Key=key,
        Body=json.dumps(item)
    )
    return {"message": "Created", "id": item_id}

def get_item(item_id):
    key = f"{PREFIX}/{item_id}.json"

    obj = s3.get_object(Bucket=BUCKET, Key=key)
    return json.loads(obj["Body"].read())


def update_item(item_id, item):
    key = f"{PREFIX}/{item_id}.json"

    s3.put_object(
        Bucket=BUCKET,
        Key=key,
        Body=json.dumps(item)
    )
    return {"message": "Updated", "id": item_id}


def delete_item(item_id):
    key = f"{PREFIX}/{item_id}.json"

    s3.delete_object(Bucket=BUCKET, Key=key)
    return {"message": "Deleted", "id": item_id}


########################################
# BATCH / LIST
########################################
def get_all_items():
    response = s3.list_objects_v2(Bucket=BUCKET, Prefix=PREFIX)

    items = []
    for obj in response.get("Contents", []):
        data = s3.get_object(Bucket=BUCKET, Key=obj["Key"])
        items.append(json.loads(data["Body"].read()))

    return items


def batch_create_items(items):
    results = []

    for item in items:
        item_id = item["id"]
        key = f"{PREFIX}/{item_id}.json"

        s3.put_object(
            Bucket=BUCKET,
            Key=key,
            Body=json.dumps(item)
        )

        results.append({"id": item_id, "status": "created"})

    return results



# import uuid
# from s3_repository import S3Repository
#
# class CrudService:
#     def __init__(self):
#         self.repo = S3Repository()
#
#     def create(self, env, table, data):
#         data["id"] = str(uuid.uuid4())
#         db = self.repo.read_db(env, table)
#
#         db["items"].append(data)
#         self.repo.write_db(env, table, db)
#
#         return {"statusCode": 201, "body": data}
#
#     def read(self, env, table, params):
#         db = self.repo.read_db(env, table)
#
#         if "id" in params:
#             item = next((x for x in db["items"] if x["id"] == params["id"]), None)
#             return {"statusCode": 200, "body": item}
#
#         return {"statusCode": 200, "body": db}
#
#     def update(self, env, table, data):
#         db = self.repo.read_db(env, table)
#
#         for i, item in enumerate(db["items"]):
#             if item["id"] == data["id"]:
#                 db["items"][i] = data
#                 break
#
#         self.repo.write_db(env, table, db)
#         return {"statusCode": 200, "body": data}
#
#     def delete(self, env, table, params):
#         db = self.repo.read_db(env, table)
#
#         db["items"] = [x for x in db["items"] if x["id"] != params["id"]]
#
#         self.repo.write_db(env, table, db)
#         return {"statusCode": 200, "body": {"deleted": True}}