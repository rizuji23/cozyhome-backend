from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ...models import *
from ...serializers import *
from rest_framework.views import APIView
from ...etc import getuuid
from ...etc.response_get import response
import datetime
import pandas as pd
from django.db.models import Sum
from django.db.models import Q


class CostProjectView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        id = request.query_params.get('id')
        try:
            project = Project.objects.get(id_project=id)
            try:
                cost = CostProjectSerializer(Cost_Project.objects.select_related('id_project').get(id_project_id=project.id), many=False)

                sum_asset_out = 0
                stok_out_count = Stok_Out.objects.filter(id_project_id=project.id)

                for i in stok_out_count:
                    sum_asset_out += i.id_material.harga * i.stok_out
                print("cost.data", cost.data)
                self.data = {
                    "cost_project": {
                        "cost_produksi": cost.data['cost_produksi'],
                        "cost_operasional": cost.data['cost_operasional'],
                        "cost_lain": cost.data['cost_lain'],
                        "cost_bahan": sum_asset_out,
                        "id_cost_project": cost.data['id_cost_project']
                    }
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
        cost_produksi = request.data['cost']
        try:
            cost_all = Cost_Project.objects.get(id_cost_project=id)
            cost_all.cost_produksi = cost_produksi
            cost_all.save()

            cost_sum = cost_all.cost_produksi + cost_all.cost_bahan + cost_all.cost_design + cost_all.cost_operasional + cost_all.cost_lain

            _project = Project.objects.get(id=cost_all.id_project_id)
            _project.total_cost = cost_sum
            _project.save()

            return response(code=201, data=None, detail_message="update request success")
        except Cost_Project.DoesNotExist:
            return response(code=404, data=None, detail_message="data cost project not found")
        
class CostDesignView(APIView):
    permission_classes = (IsAuthenticated, )

    def put(self, request):
        id = request.query_params.get('id')
        cost_design = request.data['cost']

        try:
            cost_all = Cost_Project.objects.get(id_cost_project=id)
            cost_all.cost_design = cost_design
            cost_all.save()

            cost_sum = cost_all.cost_produksi + cost_all.cost_bahan + cost_all.cost_design + cost_all.cost_operasional + cost_all.cost_lain

            _project = Project.objects.get(id=cost_all.id_project_id)
            _project.total_cost = cost_sum
            _project.save()

            return response(code=201, data=None, detail_message="update request success")
        except Cost_Project.DoesNotExist:
            return response(code=404, data=None, detail_message="data cost project not found")

class CostOperasionalView(APIView):
    permission_classes = (IsAuthenticated, )

    def put(self, request):
        id = request.query_params.get('id')
        cost_operasional = request.data['cost']

        try:
            cost_all = Cost_Project.objects.get(id_cost_project=id)
            cost_all.cost_operasional = cost_operasional
            cost_all.save()

            cost_sum = cost_all.cost_produksi + cost_all.cost_bahan + cost_all.cost_design + cost_all.cost_operasional + cost_all.cost_lain

            _project = Project.objects.get(id=cost_all.id_project_id)
            _project.total_cost = cost_sum
            _project.save()

            return response(code=201, data=None, detail_message="update request success")
        except Cost_Project.DoesNotExist:
            return response(code=404, data=None, detail_message="data cost project not found")
        
class CostProjectSumView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        cost = Cost_Project.objects.filter(~Q(id_project_id=None)).aggregate(total_bahan=Sum('cost_bahan'), total_design=Sum('cost_design'), total_operasional=Sum('cost_operasional'), total_produksi=Sum('cost_produksi'), total_lain=Sum('cost_lain'))

        total_all = 0

        if cost['total_bahan'] != None:
            for k, v in cost.items():
                print(v)
                total_all += v

        cost['total_all'] = total_all

        self.data = {
            "sum": cost,
        }

        return response(code=200, data=self.data, detail_message=None)
        