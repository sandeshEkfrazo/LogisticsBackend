from django.core.cache import cache

class ClearCacheMiddleware:
    def process_request(self, request):
        # Clear the cache here
        cache.clear()   