from rest_framework import status
from yovoco.constants import KEY_DETAIL, KEY_RESULTS, KEY_STATUS_CODE, VALUE_SUCCESS
class ResultResponse:
	def __init__(self, detail=VALUE_SUCCESS, status_code=status.HTTP_200_OK, data=None):
		self.detail=detail
		self.status_code=status_code
		self.data=data
	
	@property
	def get_response(self):
		return {
			KEY_DETAIL: self.detail,
			KEY_STATUS_CODE: self.status_code,
			KEY_RESULTS: self.data
		}