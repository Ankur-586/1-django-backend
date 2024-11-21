from django.utils.deprecation import MiddlewareMixin

class ImageUrlMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if response.status_code == 200 and hasattr(response, 'data'):
            self.add_full_image_urls(response.data, request)
        return response

    def add_full_image_urls(self, data, request):
        if isinstance(data, list):
            for item in data:
                self._update_image_urls(item, request)
        elif isinstance(data, dict):
            self._update_image_urls(data, request)

    def _update_image_urls(self, item, request):
        for key, value in item.items():
            if isinstance(value, str) and (key == 'image' or key.endswith('_image')):
                item[key] = request.build_absolute_uri(value)