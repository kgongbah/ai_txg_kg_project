from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
import time
import logging

#Log the time and info of any HTTP request
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

#Configure custom middleware class
class CustomMiddleware(BaseHTTPMiddleware):

    #core function that intercepts HTTP request, allows you ot process response/add extra
    #code before passing to next middleware or route handler
    async def dispatch(self, request: Request, call_next):

        #define the start of request
        start_time = time.time() 

        #log request url and method
        logging.info(f"Request URL: {request.url} - Method: {request.method}")

        #call_next passes request to the next "layer", which generates a response, assign to response
        response = await call_next(request)

        #define the process time
        process_time = time.time() - start_time()

        #log response status and time
        logging.info(f"Response Status: {response.status_code} - Process Time: {process_time:.2f}s")

        return response
