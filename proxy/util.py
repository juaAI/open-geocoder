def check_lat_lon(lat:float,lon:float):
    '''
    Checks if given lat, lon are formatted right
    In this API, lats between -90 and 90 are beingt used, 
    lons between -180 and 180 are being used (european).
    Args:
        lat:float >> latitude, number between -90 and 90
        lon:float >> longitude, number between -180 and 180
    Returns:
        True:bool  >> book True, if check successfull
        error:dict >> object with error code, if check failed
    '''
    if not ((90>=lat>=-90) or (180>=lon>=-180)):
        return {"error":"lat must be between -90 and 90, lon must be between -180 and 180"}
    else:
        return True
