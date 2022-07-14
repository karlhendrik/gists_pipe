from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os, httpx
from dotenv import load_dotenv
from typing import Union
import uvicorn

# Initialize FastAPI and environment variables
app = FastAPI()
load_dotenv()

GITHUB_API = os.getenv('GITHUB_API')
PIPEDRIVE_API = os.getenv('PIPEDRIVE_API')
VERSION=os.getenv('VERSION')

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Application routes
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

## API Endpoints

# -- Github --
@app.get(f'/api/{VERSION}/gists')
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
            # Get all gists (latest 30)
            response = await client.get('https://api.github.com/gists/public', headers=headers)
        return response.json()

# -- Pipedrive --
@app.get(f'/api/{VERSION}/deals')
async def get_deals(deal_id: Union[int, None] = None):
    async with httpx.AsyncClient() as client:
        if deal_id:
            # Get a single deal
            response = await client.get(f'https://nocompanyltd2.pipedrive.com/api/v1/deals/{deal_id}?api_key={PIPEDRIVE_API}')
        else:
            # Get all deals
            response = await client.get(f'https://nocompanyltd2.pipedrive.com/api/v1/deals?limit=500&api_token={PIPEDRIVE_API}')
        return response.json()

@app.post(f'/api/{VERSION}/deals')
async def post_deals(deal: dict):
    async with httpx.AsyncClient() as client:
        response = await client.post(f'https://nocompanyltd2.pipedrive.com/api/v1/deals?api_token={PIPEDRIVE_API}', json=deal)
        return response.json()


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, log_level="info")