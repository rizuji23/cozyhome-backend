from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ...models import *
from ...serializers import *
from rest_framework.views import APIView
from ...etc import getuuid
from ...etc.response_get import response
import datetime

class PekerjaanLainView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        id = request.query_params.get('id_project')
        
        try:
            project = Project.objects.get(id_project=id)

            pekerjaan = PekerjaanLainSerializer(Pekerjaan_Lain.objects.filter(), read_only=True)

            self.data = {
                "pekerjaan_lain": pekerjaan.data
            }

            return response(code=200, data=self.data, detail_message=None)

        except Project.DoesNotExist:
            return response(code=404, data=None, detail_message="data project not found")
        

    def post(self, request):
        id_pekerjaan_lain = getuuid.Ramdom_Id.get_id()
        id_project = request.data['id_project']
        nama_pekerjaan = request.data['nama_pekerjaan']
        desc = request.data['desc']
        id_user = request.data['id_user']

        