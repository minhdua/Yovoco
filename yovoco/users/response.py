from rest_framework import status
from django.http import JsonResponse

class ResultResponse:
    def __init__(self, detail='', status_code=status.HTTP_200_OK, data=None):
        self.detail = detail
        self.status_code = status_code
        self.data = data
    
    @property
    def get_response(self):
        return {
            'detail': self.detail,
            'status_code': self.status_code,
            'data': self.data
       }