from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os, httpx
from dotenv import load_dotenv
from typing import Union

# Initialize FastAPI and environment variables
app = FastAPI()
load_dotenv()

GITHUB_API = os.getenv('GITHUB_API')
PIPEDRIVE_API = os.getenv('PIPEDRIVE_API')

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Routes
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/gists")
async def get_gists(username: Union[str, None] = None, gist_id: Union[str, None] = None):
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

@app.get("/pipedrive")
async def get_pipedrive(api_key: Union[str, None] = None, deal_id: Union[str, None] = None):
    async with httpx.AsyncClient() as client:
        if api_key:
            # Get all deals for a user
            response = await client.get(f'https://api.pipedrive.com/v1/deals?api_key={PIPEDRIVE_API}')
        elif deal_id:
            # Get a single deal
            response = await client.get(f'https://api.pipedrive.com/v1/deals/{deal_id}?api_key={PIPEDRIVE_API}')
        else:
            # Get all deals
            response = await client.get(f'https://api.pipedrive.com/v1/deals?api_key={PIPEDRIVE_API}')
        return response.json()