# checker.py

from http.client import HTTPConnection
from urllib.parse import urlparse
import asyncio
import time
import functools
import aiohttp

def response_time(func):
    """Timer function, @response_time to wrap a function and output
    the functions run time.
    """
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        time_before = time.perf_counter()
        result = func(*args, **kwargs)
        time_after = time.perf_counter()
        response_time = time_after - time_before
        print(f"Response time: {response_time:0.4f} seconds")
        return result
    return wrapper_timer

@response_time
def site_is_online(url, timeout=2):
    """Return True if the target URL is online.
    
    Raise an exception otherwise.
    """
    error = Exception("Unknown error")
    parser = urlparse(url)
    # uses the netloc url or grabs the base url
    host = parser.netloc or parser.path.split("/")[0]
    # tests http and https
    for port in (80, 443):
        connection = HTTPConnection(host=host, port=port, timeout=timeout)
        try:
            connection.request("HEAD", "/")
            return True
        except Exception as e:
            error = e
        finally:
            connection.close()
    raise error

async def site_is_online_async(url, timeout=2):
    """Return True if the target URL is online.
    
    Raise an exception otherwise.
    """
    error = Exception("Unknown error")
    parser = urlparse(url)
    # uses the netloc url or grabs the base url
    host = parser.netloc or parser.path.split("/")[0]
    # tests http and https
    for scheme in ("http", "https"):
        target_url = scheme + "://" + host
        async with aiohttp.ClientSession() as session:
            try:
                await session.head(target_url, timeout=timeout)
                return True
            except asyncio.exceptions.TimeoutError:
                error = Exception("timed out")
            except Exception as e:
                error = e
    raise error