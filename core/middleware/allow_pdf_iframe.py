from django.utils.deprecation import MiddlewareMixin

class AllowPDFIframeMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # Only allow iframe embedding for .pdf files in /media/
        if request.path.startswith('/media/') and request.path.endswith('.pdf'):
            response['X-Frame-Options'] = 'ALLOWALL'
        return response
