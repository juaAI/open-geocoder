from fastapi import APIRouter, Depends
from fastapi_limiter.depends import RateLimiter
from requests import get

from ..util import check_lat_lon
from os import environ

PHOTON_URL = "http://photon:2322/"
RATE_LIMIT = environ["rate-limit"]
RATE_RESET = environ["rate-reset"]

router = APIRouter()

@router.get(
    "/by_name", 
    dependencies=[Depends(RateLimiter(
        times=RATE_LIMIT, 
        seconds=RATE_RESET,
        ))]
    )
def by_name(
    name: str, 
    language: str="en", 
    limit:Optional[int] = None, 
    lat:Optional[float] = None, 
    lon:Optional[float] = None):   
    '''
    Returns geoJSON with Coordinates and Information about desired place
    
    Usage:
        Search "Berlin", or "10551 Berlin" or even "Alexander Platz, Berlin"
    
    Args:
        name:str      object/location/area of interest        
    
    Optional:
        language:str  language for query and response
        limit:int     max results
        lat:float     weight search results after given lat (prefer results arround given lat/lon)
        lon:float     weight search results after given lon (prefer results arround given lat/lon)
    '''

    query_params = "&limit="
    query = PHOTON_URL + "api/?q=" + name + "&lang=" + language + query_params 
    
    if limit is None:
        query = query + str(1)
    else:
        query = query + str(limit)
    if lat is not None and lon is not None:
        check = check_lat_lon(lat, lon)
        if check is None:
            return check
        else:
            query = query + "&lat=" + str(lat) + "&lon=" + str(lon)        
    resp = get(query)

    if resp.status_code == 200:
        return resp.json()
    else:
        return {"status":"error"}


@router.get(
    "/reverse", 
    dependencies=[Depends(RateLimiter(
        times=RATE_LIMIT, 
        seconds=RATE_RESET,
        ))]
    )
def reverse(
    lat:float, 
    lon:float
    ):   
    '''
    Returns geoJSON with information about desired location

    Args:
        lat:float    latitude of desired location
        lon:float    longitude of desired location
    '''

    if check_lat_lon(lat, lon):
        query = PHOTON_URL + "reverse"
        query = query + "?lat=" + str(lat) + "&lon=" + str(lon)    
        resp = get(query)

        if resp.status_code == 200:
            return resp.json()        
        else:
            return {"status":"error"}    
    else:
        return wrong_coordinate_message