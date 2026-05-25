import azure.functions as func
import json
from azure.cosmos import CosmosClient
import os

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="visitor-counter")
def visitor_counter(req: func.HttpRequest) -> func.HttpResponse:
    
    # Connect to CosmosDB
    url = os.environ["COSMOS_URL"]
    key = os.environ["COSMOS_KEY"]
    client = CosmosClient(url, credential=key)
    
    database = client.get_database_client("ResumeDB")
    container = database.get_container_client("Counter")
    
    # Get current count
    item = container.read_item(item="1", partition_key="1")
    count = item["count"] + 1
    
    # Update count
    item["count"] = count
    container upsert_item(item)
    
    # Return response with CORS header
    return func.HttpResponse(
        body=json.dumps({"count": count}),
        mimetype="application/json",
        headers={"Access-Control-Allow-Origin": "*"}
    )