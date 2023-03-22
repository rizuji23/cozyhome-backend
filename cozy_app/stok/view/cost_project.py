from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ...models import *
from ...serializers import *
from rest_framework.views import APIView
from ...etc import getuuid
from ...etc.response_get import response
import datetime

class CostProjectView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        id = request.query_params.get('id')
        try:
            project = Project.objects.get(id_project=id)
            try:
                cost = CostProjectSerializer(Cost_Project.objects.select_related('id_project').get(id_project_id=project.id), many=False)

                self.data = {
                    "cost_project": cost.data
                }

                return response(code=200, data=self.data, detail_message=None)
            except Cost_Project.DoesNotExist:
                return response(code=404, data=None, detail_message="data cost project not found")
        except Project.DoesNotExist:
            return response(code=404, data=None, detail_message="data project not found")
    
    def delete(self, request):
        id = request.query_params.get('id')

        try:
            try:
                data = Cost_Project.objects.get(id_cost_project=id)

                data.delete()
                return response(code=201, data=None, detail_message="delete request success")
            except Cost_Project.DoesNotExist:
                return response(code=404, data=None, detail_message="data cost project not found")
        except Exception as e:
            return response(code=500, data=None, detail_message=str(e))
        

class CostProduksiView(APIView):
    permission_classes = (IsAuthenticated, )

    def put(self, request):
        id = request.query_params.get('id')
        cost_produksi = request.data['cost_produksi']
        try:
            cost_all = Cost_Project.objects.get(id_cost_project=id)
            cost_all.cost_produksi = cost_produksi
            cost_all.save()
            return response(code=201, data=None, detail_message="update request success")
        except Cost_Project.DoesNotExist:
            return response(code=404, data=None, detail_message="data cost project not found")

