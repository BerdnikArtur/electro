# myapp/middleware.py
from django.core.cache import cache
from django.http import HttpResponse, FileResponse
from django.utils.deprecation import MiddlewareMixin

from django.middleware.csrf import get_token

class MainCacheMiddleware(MiddlewareMixin):
    """
    Middleware for caching querysets based on request URL and query parameters.
    """

    def process_request(self, request):
        # Generate cache key based on URL and query parameters
        cache_key = self.get_cache_key(request)
        if cache_key:
            cached_response = cache.get(cache_key)
            if cached_response:
                return HttpResponse(cached_response)

    def process_response(self, request, response):
        # Cache the response if the status is OK and cache_key was set
        if isinstance(response, FileResponse) or hasattr(response, 'streaming_content'):
            return response
        
        cache_key = self.get_cache_key(request)
        if cache_key and response.status_code == 200:
            cache.set(cache_key, response, timeout=60 * 15)  # Cache for 15 minutes
        
        return response

    def get_cache_key(self, request):
        """
        Generate a cache key based on the request path and query parameters.
        """
        if request.method != 'GET' or self.is_admin_request(request) or self.is_api_request(request):
            return None

        # Create a cache key from the URL path and query parameters
        cache_key = f"queryset_cache_{request.get_full_path()}"
        return cache_key
    
    def is_admin_request(self, request):
        """
        Check if the request is for the admin panel.
        """
        return request.path.startswith('/admin/')
    
    def is_api_request(self, request):
        """
        Check if the request is for the api requests.
        """
        return request.path.startswith('/api/')
    
    def update_cache_after_post(self, request):
        """
        Update the cache after a POST request if needed.
        This method can be used to clear or refresh cache entries related to modified data.
        """
        cache_key = self.get_cache_key(request)
        if cache_key:
            # Optionally clear or update the cache here
            cache.delete(cache_key)




from django.http import JsonResponse
import hashlib
from django.utils.encoding import force_bytes

def get_cache_key(request):
    url = request.build_absolute_uri()
    return hashlib.md5(force_bytes(url)).hexdigest()

class FullPageCacheMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        cache_key = get_cache_key(request)
        if not cache_key:
            return self.get_response(request)

        cached_response = cache.get(cache_key)
        if cached_response:
            # Ensure that JSON responses are returned with correct headers
            if isinstance(cached_response, JsonResponse):
                cached_response["Content-Type"] = "application/json"
            return cached_response

        response = self.get_response(request)

        # Check if the response is JSON and cache it properly
        if isinstance(response, JsonResponse):
            cache.set(cache_key, response, timeout=60*15)  # Cache JSON responses
        else:
            cache.set(cache_key, response, timeout=60*15)  # Cache HTML responses

        return response 
    

class CacheMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path.startswith('/admin/') or request.path.startswith('/api/'):
            return None
        
        if request.method != 'GET':
            self.clear_cache(request)

        if request.method == 'GET':
            cache_key = self.get_cache_key(request)
            cached_response = cache.get(cache_key)
            if cached_response:
                return cached_response

        return None

    def process_response(self, request, response):
        if request.path.startswith('/admin/') or request.path.startswith('/api/'):
            return response


        if request.method == 'GET':
            # Check if the response contains a CSRF token and avoid caching
            csrf_token = get_token(request)
            if csrf_token in response.cookies:
                # CSRF token found, don't cache this response
                return response
            else:
                # Cache JSON and other responses for 15 minutes
                cache_key = self.get_cache_key(request)
                #cache.set(cache_key, response, timeout=60 * 15)
        

        # if request.method == 'GET':
        #     if isinstance(response, JsonResponse):
        #         cache_key = self.get_cache_key(request)
        #         cache.set(cache_key, response, timeout=60*15)
        #     else:
        #         cache_key = self.get_cache_key(request)
        #         cache.set(cache_key, response, timeout=60*15)  

        return response
    
    def get_cache_key(self, request):
        # Generate a unique key based on the request URL and query parameters
        url = request.build_absolute_uri()  # Get the full URL including query parameters
        return hashlib.md5(force_bytes(url)).hexdigest()
    
    def clear_cache(self, request):
        """Clear cache related to the current URL."""
        cache_key = self.get_cache_key(request)
        cache.delete(cache_key)

