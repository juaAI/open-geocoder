'''
Wraps the photon OSM API and implements 
rate limiting and SSL encryption
'''

from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware

from routes import geo

from os import environ

# init app
app = FastAPI(
    title="Open Geocoder API (based on komoot photon)",
    description='Open Geocoder API makes it easy to search for locations aswell as reverse searching for coordinates.',
    version=0.1,
    redoc_url=None
)
app.add_middleware(GZipMiddleware, minimum_size=1000)

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
    uvicorn.run(
        app,  
        port=433,
        ssl_keyfile=environ["cert-key"],
        ssl_certfile=environ["cert"],
        log_config="log_config.yaml"
        )