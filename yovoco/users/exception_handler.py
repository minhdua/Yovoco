from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    # Now add the HTTP status code to the response.
    if response is not None:
        if type(response.data) is not dict:
            response.data = {'detail': response.data}
        response.data['status_code'] = response.status_code
    return response