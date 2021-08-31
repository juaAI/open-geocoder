'''
Wraps the photon OSM API and implements 
rate limiting and SSL encryption
'''

import yaml
import aioredis
import uvicorn
from os import environ
from sys import argv

from starlette.responses import RedirectResponse

from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter

from routes import geo

# develop version without docker
dev = False
if len(argv) > 1:
    if argv[1] == "--standalone":
        dev = True


# init app
app = FastAPI(
    title="Open Geocoder API (based on komoot photon)",
    description='Open Geocoder API makes it easy to search for locations aswell as reverse searching for coordinates.',
    version=0.1,
    redoc_url=None
)
app.add_middleware(GZipMiddleware, minimum_size=1000)

@app.on_event("startup")
async def startup():
    '''
    Initializes redis for caching of API requests
    and rate limiting
    '''
    if dev:
        redis = await aioredis.from_url(
            "redis://localhost", 
            encoding="iso-8859-1", 
            decode_responses=True
            )
    else:
        redis = await aioredis.from_url(
            "redis://redis", 
            encoding="iso-8859-1", 
            decode_responses=True
            )
    await FastAPILimiter.init(redis)

# index entrypoint
@app.get("/")
def index():
    ''' Redirects to the docs
    '''
    resp = RedirectResponse(url='/docs')
    return resp

# mount routes
app.include_router(
    geo.router,
    prefix="/v1/geo",
    tags=["Geocoding"],
    responses={404: {"description": "Not found"}}
    )

# allow cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    if dev:
        uvicorn.run(
            app, 
            host="0.0.0.0", 
            port=8082,
            ssl_keyfile="certs/privkey.pem",
            ssl_certfile="certs/cert.pem",
            log_config="log_config.yaml"
        )    
    else:
        uvicorn.run(
            app, 
            host="0.0.0.0", 
            port=443,
            ssl_keyfile=environ["certkey"],
            ssl_certfile=environ["cert"],
            log_config="log_config.yaml"
        )