from rest_framework.renderers import JSONRenderer

class CustomRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context['response']
        status_code = response.status_code
        
        # Handle cases where data might be None
        if data is None:
            data = {}

        # Determine default message
        message = "Success"
        if status_code >= 400:
            message = "Error"

        # Check if a custom message or error was passed in the data
        if isinstance(data, dict):
            if 'message' in data:
                message = data.pop('message')
            elif 'error' in data:
                message = data.pop('error')
            elif 'detail' in data:
                message = data.pop('detail')
            
            # If it's a validation error (dict of lists), keep it in data
            # but maybe set a specific message
            if status_code == 400 and message == "Error":
                message = "Validation Error"

        formatted_data = {
            "status_code": status_code,
            "message": message,
            "data": data
        }

        return super().render(formatted_data, accepted_media_type, renderer_context)
