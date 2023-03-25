from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ...models import *
from ...serializers import *
from rest_framework.views import APIView
from ...etc import getuuid
from ...etc.response_get import response
import datetime
from django.contrib.auth import authenticate

class UserView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        try:
            user = User.objects.get(username=request.query_params.get('username'))

            # self.data = {
            #     "user": user.data
            # }

            return response(code=200, data=None, detail_message=None)
        except User.DoesNotExist:
            return response(code=404, data=None, detail_message="data user not found")

class ChangePasswordView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        username = request.data['username']
        old_password = request.data['old_password']
        new_password = request.data['new_password']

        user = authenticate(username=username, password=old_password)
        if user is not None:
            user.set_password(new_password)
            user.save()

            return response(code=201, data=None, detail_message="update request success")

        else:
            return response(code=404, data=None, detail_message="old password is incorrect")





