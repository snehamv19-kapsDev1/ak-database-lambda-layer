import json
from db_service import (
    create_item,
    get_item,
    update_item,
    delete_item,
    get_all_items,
    batch_create_items
)


def lambda_handler(event, context):
    method = event.get("httpMethod")
    resource = event.get("resource")
    path_params = event.get("pathParameters") or {}
    item_id = path_params.get("id")

    try:
        if resource == "/items" and method == "GET":
            return response(200, get_all_items())

        if resource == "/items" and method == "POST":
            body = json.loads(event["body"])
            return response(200, batch_create_items(body))

        if method == "POST":
            body = json.loads(event["body"])
            return response(200, create_item(body))

        if method == "GET":
            return response(200, get_item(item_id))

        if method == "PUT":
            body = json.loads(event["body"])
            return response(200, update_item(item_id, body))

        if method == "DELETE":
            return response(200, delete_item(item_id))

        return response(400, {"error": "Unsupported route"})

    except Exception as e:
        return response(500, {"error": str(e)})


def response(code, body):
    return {
        "statusCode": code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body)
    }


# import json
# from service import CrudService
#
# service = CrudService()
#
# def handler(event, context):
#     print("in handler EVENT:", event)
#
#     method = event.get("httpMethod")
#     body = json.loads(event.get("body", "{}"))
#     params = event.get("queryStringParameters") or {}
#
#     table = params.get("table", "doctor")
#     env = params.get("env", "dev")
#
#     if method == "POST":
#         return service.create(env, table, body)
#
#     if method == "GET":
#         return service.read(env, table, params)
#
#     if method == "PUT":
#         return service.update(env, table, body)
#
#     if method == "DELETE":
#         return service.delete(env, table, params)
#
#     return {
#         "statusCode": 400,
#         "body": json.dumps({"message": "Unsupported method"})
#     }