import json
from service import CrudService

service = CrudService()

def handler(event, context):
    print("EVENT:", event)

    method = event.get("httpMethod")
    body = json.loads(event.get("body", "{}"))
    params = event.get("queryStringParameters") or {}

    table = params.get("table", "doctor")
    env = params.get("env", "dev")

    if method == "POST":
        return service.create(env, table, body)

    if method == "GET":
        return service.read(env, table, params)

    if method == "PUT":
        return service.update(env, table, body)

    if method == "DELETE":
        return service.delete(env, table, params)

    return {
        "statusCode": 400,
        "body": json.dumps({"message": "Unsupported method"})
    }