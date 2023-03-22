from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ...models import *
from ...serializers import *
from rest_framework.views import APIView
from ...etc import getuuid
from ...etc.response_get import response
import datetime

class UserView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        user = UserSerializer(User.objects.get(username=request.query_params.get('username')), many=True)

        self.data = {
            "user": user.data
        }

        return response(code=200, data=self.data, detail_message=None)

