import uuid
from s3_repository import S3Repository

class CrudService:
    def __init__(self):
        self.repo = S3Repository()

    def create(self, env, table, data):
        data["id"] = str(uuid.uuid4())
        db = self.repo.read_db(env, table)

        db["items"].append(data)
        self.repo.write_db(env, table, db)

        return {"statusCode": 201, "body": data}

    def read(self, env, table, params):
        db = self.repo.read_db(env, table)

        if "id" in params:
            item = next((x for x in db["items"] if x["id"] == params["id"]), None)
            return {"statusCode": 200, "body": item}

        return {"statusCode": 200, "body": db}

    def update(self, env, table, data):
        db = self.repo.read_db(env, table)

        for i, item in enumerate(db["items"]):
            if item["id"] == data["id"]:
                db["items"][i] = data
                break

        self.repo.write_db(env, table, db)
        return {"statusCode": 200, "body": data}

    def delete(self, env, table, params):
        db = self.repo.read_db(env, table)

        db["items"] = [x for x in db["items"] if x["id"] != params["id"]]

        self.repo.write_db(env, table, db)
        return {"statusCode": 200, "body": {"deleted": True}}