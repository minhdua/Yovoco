from rest_framework.views import exception_handler

from yovoco.constants import KEY_DETAIL, KEY_STATUS_CODE

def custom_exception_handler(exc, context):
	# Call REST framework's default exception handler first,
	# to get the standard error response.
	response=exception_handler(exc, context)
	# Now add the HTTP status code to the response.
	if response:
		if type(response.data) is not dict:
			response.data={KEY_DETAIL: response.data}
		response.data[KEY_STATUS_CODE]=response.status_code
	return response