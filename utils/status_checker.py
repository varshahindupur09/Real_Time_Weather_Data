import requests

def getStatuscode(url):
    try:
        r = requests.head(url, timeout=10) # it is faster to only request the header
        return (r.status_code)
    except:
        return -1