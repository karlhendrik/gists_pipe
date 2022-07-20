from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
from typing import Union
from dotenv import load_dotenv
import uvicorn
import os
import httpx
import time

# Check if connection to database is successful and return the connection
try:
    client = MongoClient(os.environ.get("MONGO_URI"))
    database = client.gists_pipe

    # Collections
    gistsCollection = database.get_collection('gists')

except Exception as e:
    print(e)
    print("ERROR! Could not connect to database!")

# Initialize FastAPI and environment variables
app = FastAPI()
load_dotenv()
GITHUB_API = os.getenv('GITHUB_API')
PIPEDRIVE_API = os.getenv('PIPEDRIVE_API')
VERSION=os.getenv('VERSION')
COMPANY_NAME=os.getenv('COMPANY_NAME')

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Application routes
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post(f'/api/{VERSION}/watch/')
async def store_gists(username: str):
    gists = await get_gists_from_github(username)

    # Prepare documents
    gist_ids = {}
    for gist in gists:
        # Store the gists ids in a dictionary with additional gist information
        gist_ids[gist['id']] = gist
        gist_author = gist['owner']['login']
        epoch = time.time()

    gist_document = {
        'gists': gist_ids,
        'gist_author': gist_author,
        'epoch': epoch
    }

    # If author not found in the collection the add new gist document
    if gistsCollection.count_documents({'gist_author': gist_author}) == 0:
        # Insert new document
        gistsCollection.insert_one(gist_document)
    else:
        existing_ids = []
        existing_documents = gistsCollection.find({'gist_author': gist_author})
        # Loop through existing documents and get the gist ids
        for existing_gist in existing_documents:
            # Add the gist ids to a list
            existing_ids.append(list(existing_gist['gists'].keys()))
        # Remove duplicates from the list
        existing_ids = list(set(sum(existing_ids, [])))
        
        # Comapare the existing ids with the new ids
        for gist_id in gist_ids:
            if gist_id not in existing_ids:
                gistsCollection.insert_one(gist_document)
                return {"message": f"Changes detected for user {gist_author}"}
            return {"message": f"You are now watching new Gists for the user {gist_author}, page will refresh in 1 minute"}

    # Return status code 201 (Created)
    return Response(status_code=201)


@app.get(f'/api/{VERSION}/compare/')
async def compare_gists(username: str):
    # Sanitize string
    username = username.strip()
    # Return the gists of the given author
    documents = gistsCollection.find({'gist_author': username})
    response = {}
    # Remove ObjectID from the document
    for document in documents:
        document.pop('_id')
        response[document['epoch']] = document
    return response

# -- GitHub --
@app.get(f'/api/{VERSION}/gists')
async def get_gists_from_github(username: Union[str, None] = None, gist_id: Union[str, None] = None):
    async with httpx.AsyncClient() as client:
        headers = {'Accept': 'application/vnd.github+json','Authorization': f'token {GITHUB_API}'}
        if username:
            # Get all gists for a user
            response = await client.get(f'https://api.github.com/users/{username}/gists', headers=headers)
        elif gist_id:
            # Get a single gist
            response = await client.get(f'https://api.github.com/gists/{gist_id}', headers=headers)
        else:
            # Get all gists
            response = await client.get('https://api.github.com/gists/public', headers=headers)
        return response.json()

# -- Pipedrive --
@app.get(f'/api/{VERSION}/deals')
async def get_deals(deal_id: Union[int, None] = None):
    async with httpx.AsyncClient() as client:
        if deal_id:
            # Get a single deal
            response = await client.get(f'https://{COMPANY_NAME}.pipedrive.com/api/v1/deals/{deal_id}?api_key={PIPEDRIVE_API}')
        else:
            # Get all deals
            response = await client.get(f'https://{COMPANY_NAME}.pipedrive.com/api/v1/deals?limit=500&api_token={PIPEDRIVE_API}')
        return response.json()

@app.post(f'/api/{VERSION}/deals')
async def post_deals(deal: dict):
    async with httpx.AsyncClient() as client:
        response = await client.post(f'https://{COMPANY_NAME}.pipedrive.com/api/v1/deals?api_token={PIPEDRIVE_API}', json=deal)
        return response.json()

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, log_level="info")