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
        id = request.query_params.get('id')
        
        try:
            project = Project.objects.get(id_project=id)

            pekerjaan = PekerjaanLainSerializer(Pekerjaan_Lain.objects.filter(id_project_id=project.id), many=True)

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
        harga = request.data['harga']
        id_user = request.data['id_user']

        try:
            project = Project.objects.get(id_project=id_project)

            try:
                lain = Pekerjaan_Lain(id_pekerjaan_lain=id_pekerjaan_lain, id_project_id=project.id, nama_pekerjaan=nama_pekerjaan, desc=desc, harga=harga, id_user_id=id_user)
                
                cost_all = Cost_Project.objects.get(id_project_id=project.id)
                total_lain = int(cost_all.cost_lain) + int(harga)

                cost_all.cost_lain = total_lain
                cost_all.save()

                cost_sum = cost_all.cost_produksi + cost_all.cost_bahan + cost_all.cost_design + cost_all.cost_operasional + cost_all.cost_lain

                project.total_cost = cost_sum
                project.save()
                lain.save()
                return response(code=201, data=None, detail_message="created request success")
            except Exception as e:
                return response(code=500, data=None, detail_message=str(e))

        except Project.DoesNotExist:
            return response(code=404, data=None, detail_message="data project not found")
        