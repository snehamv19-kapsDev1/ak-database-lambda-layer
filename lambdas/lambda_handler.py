import json
from db_service import (
    create_item,
    get_item,
    update_item,
    delete_item,
    get_all_items,
    batch_create_items
)

########################################
# SAFE JSON PARSER
########################################
def parse_body(event):
    try:
        return json.loads(event.get("body") or "{}")
    except Exception:
        return {}


########################################
# RESPONSE WRAPPER
########################################
def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(body)
    }


########################################
# LAMBDA HANDLER
########################################
def lambda_handler(event, context):

    print("EVENT:", json.dumps(event))

    method = event.get("httpMethod", "")
    path = event.get("path", "")
    path_params = event.get("pathParameters") or {}

    item_id = path_params.get("id")
    body = parse_body(event)

    try:

        ########################################
        # GET ALL ITEMS
        ########################################
        if method == "GET" and path == "/items":
            result = get_all_items()
            return response(200, result)

        ########################################
        # BATCH CREATE
        ########################################
        if method == "POST" and path == "/items":
            items = body.get("items", [])
            result = batch_create_items(items)
            return response(201, result)

        ########################################
        # CREATE SINGLE ITEM
        ########################################
        if method == "POST" and path == "/item":
            if "id" not in body:
                return response(400, {"error": "Missing id in request body"})

            result = create_item(body)
            return response(201, result)

        ########################################
        # GET SINGLE ITEM
        ########################################
        if method == "GET" and path.startswith("/item/"):
            if not item_id:
                return response(400, {"error": "Missing item id"})

            result = get_item(item_id)
            return response(200, result)

        ########################################
        # UPDATE ITEM
        ########################################
        if method == "PUT":
            if not item_id:
                return response(400, {"error": "Missing item id"})

            result = update_item(item_id, body)
            return response(200, result)

        ########################################
        # DELETE ITEM
        ########################################
        if method == "DELETE":
            if not item_id:
                return response(400, {"error": "Missing item id"})

            result = delete_item(item_id)
            return response(200, result)

        ########################################
        # FALLBACK
        ########################################
        return response(404, {"error": "Route not found"})

    except Exception as e:
        print("ERROR:", str(e))
        return response(500, {"error": str(e)})