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
            cost = CostProjectSerializer(Cost_Project.objects.get(id_project_id=id).select_related('id_project'), many=True)

            self.data = {
                "cost_project": cost.data
            }

            return response(code=200, data=self.data, detail_message=None)
        except Cost_Project.DoesNotExist:
            return response(code=404, data=None, detail_message="data cost project not found")
    
    def post(self, request):
        id_cost_project = getuuid.Ramdom_Id.get_id()
        id_project = request.data['id_project']
        cost_design = request.data['cost_design']
        cost_oprasional = request.data['cost_oprasional']
        cost_produksi = request.data['cost_produksi']
        cost_bahan = request.data['cost_bahan']
        id_user = request.data['id_user']

        try:
            project = Project.objects.get(id_project=id_project)
            try:
                _cost = Cost_Project(id_cost_project=id_cost_project, id_project_id=project.id, cost_design=cost_design, cost_oprasional=cost_oprasional, cost_produksi=cost_produksi, cost_bahan=cost_bahan, id_user_id=id_user)

                _cost.save()

                return response(code=201, data=None, detail_message="created request success")
            
            except Exception as e:
                return response(code=500, data=None, detail_message=str(e))
            
        except Project.DoesNotExist:
            return response(code=404, data=None, detail_message="data project not found")
    
    def put(self, request):
        id = request.query_params.get('id')
        id_project = request.data['id_project']
        cost_design = request.data['cost_design']
        cost_oprasional = request.data['cost_oprasional']
        cost_produksi = request.data['cost_produksi']
        cost_bahan = request.data['cost_bahan']
        id_user = request.data['id_user']

        try:
            cost = Cost_Project.objects.get(id_cost_project=id)
            try:
                project = Project.objects.get(id_project=id_project)

                try:
                    cost.id_project_id = project.id
                    cost.cost_design = cost_design
                    cost.cost_operasional = cost_oprasional
                    cost.cost_produksi = cost_produksi
                    cost.cost_bahan = cost_bahan
                    cost.id_user_id = id_user

                    cost.save()
                
                    return response(code=201, data=None, detail_message="update request success")
            
                except Cost_Project.DoesNotExist:
                    return response(code=404, data=None, detail_message="data cost project not found")
            except Project.DoesNotExist:
                return response(code=404, data=None, detail_message="data project not found")
        except Exception as e:
            return response(code=500, data=None, detail_message=str(e))
    
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