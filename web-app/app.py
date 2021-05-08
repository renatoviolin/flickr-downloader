from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, HTMLResponse
import logging
import asyncio
from flickr import FlickrImageDownload
import yaml
from zipfile import ZipFile
import glob
import os


# %% --------------------------------------------------------------
app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')
logger = logging.getLogger('uvicorn.error')

with open('config.yaml') as stream:
    config = yaml.safe_load(stream)


@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse('index.html', context={'request': request})


@app.post('/search')
async def search(request: Request):
    try:
        r = await request.json()
        query = r.get('query')
        tags = r.get('tags')
        max_download = int(r.get('max_download'))

        flickr_api = FlickrImageDownload(flickr_id=config['id'],
                                         flickr_secret=config['secret'],
                                         path='static/downloads')
        result = flickr_api.get_url(query, tags, max_download)
        return JSONResponse(status_code=200, content={'result': result})
    except Exception as ex:
        logger.error(ex)
        return JSONResponse(status_code=400, content={'error': ex})


@app.post('/download')
async def download(request: Request):
    try:
        r = await request.json()
        links = r.get('links')
        prefix = r.get('tags')
        prefix = '_'.join(prefix.split())
        if len(prefix) == 0:
            prefix = 'no_tags'
        scale_w = int(r.get('scale_w', 0))
        scale_h = int(r.get('scale_h', 0))
        flickr_api = FlickrImageDownload(flickr_id=config['id'],
                                         flickr_secret=config['secret'],
                                         path='static/downloads',
                                         prefix=prefix)
        result = flickr_api.download_from_url(links, scale_w, scale_h)

        zip_name = f'static/downloads/{prefix}.zip'
        files = glob.glob(f'static/downloads/{prefix}*')
        with ZipFile(zip_name, 'w') as zip_file:
            for f in files:
                zip_file.write(f)
                os.remove(f)
        zip_file.close()

        return JSONResponse(status_code=200, content={'result': zip_name})
    except Exception as ex:
        logger.error(ex)
        return JSONResponse(status_code=400, content={'error': ex})
