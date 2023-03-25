from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ...models import *
from ...serializers import *
from rest_framework.views import APIView
from ...etc import getuuid
from ...etc.response_get import response
import datetime
from django.db.models import Count, Min
import json
from django.core.serializers import serialize
from re import search


class ProjectView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        if 'id_customer' in request.query_params:
            id_customer = request.query_params.get('id_customer')
            try:
                customer = Customer.objects.get(id_customer=id_customer)
                project = ProjectSerializer(Project.objects.filter(id_customer_id=customer.id).
                select_related('id_customer'), many=True)
                self.data = {
                    "project": project.data
                }

                return response(code=200, data=self.data, detail_message=None)
            except Customer.DoesNotExist:
                return response(code=404, data=None, detail_message="data customer not found")
            
        elif 'id_project' in request.query_params:
            id_project = request.query_params.get('id_project')
            try:
                project = ProjectSerializer(Project.objects.select_related('id_customer').get(id_project=id_project), many=False)
                self.data = {
                    "project": project.data
                }

                return response(code=200, data=self.data, detail_message=None)
            except Project.DoesNotExist:
                return response(code=404, data=None, detail_message="data projek not found")
        
        else:
            project = ProjectSerializer(Project.objects.all().select_related('id_customer'), many=True)
            self.data = {
                "project": project.data
            }

            return response(code=200, data=self.data, detail_message=None)

        
    
    def post(self, request):
        id_project = getuuid.Ramdom_Id.get_id()
        id_customer = request.data['id_customer']
        nama_project = request.data['nama_project']
        jumlah_volumn = request.data['jumlah_volumn']
        estimasi_pengerjaan = request.data['estimasi_pengerjaan']
        kategori_project = request.data['kategori_project']
        start_date = request.data['start_date']
        end_date = request.data['start_date']
        status = request.data['status']
        total_cost = request.data['total_cost']
        desc = request.data['desc']

        id_user = request.data['id_user']

        try:
            try:
                customer = Customer.objects.get(id_customer=id_customer)

                project = Project(id_project=id_project, id_customer_id=customer.id, nama_project=nama_project, jumlah_volumn=jumlah_volumn, estimasi_pengerjaan=estimasi_pengerjaan, kategori_project=kategori_project, total_cost=total_cost, start_date=start_date, end_date=end_date, status=status, desc=desc, id_user_id=id_user)
                id_cost_project = getuuid.Ramdom_Id.get_id()

                project.save()

                get_pro = Project.objects.get(id_project=id_project)

                cost = Cost_Project(id_cost_project=id_cost_project, id_project_id=get_pro.id, cost_design=0, cost_operasional=0, cost_produksi=0, cost_bahan=0, cost_lain=0, id_user_id=id_user)
                cost.save()
                return response(code=201, data=None, detail_message="created request success")

            except Customer.DoesNotExist:
                return response(code=404, data=None, detail_message="data customer not found")
            
        except Exception as e:
            return response(code=500, data=None, detail_message=str(e))
        
    def put(self, request):
        id = request.query_params.get('id')
        nama_project = request.data['nama_project']
        jumlah_volumn = request.data['jumlah_volumn']
        kategori_project = request.data['kategori_project']
        desc = request.data['desc']
        id_user = request.data['id_user']

        print(id)

        try:
            try:
                data = Project.objects.get(id_project=id)
                data.nama_project = nama_project
                data.jumlah_volumn = jumlah_volumn
                data.kategori_project = kategori_project
                data.desc = desc
                data.id_user_id = id_user

                data.save()

                return response(code=201, data=None, detail_message="update request success")
            
            except Project.DoesNotExist:
                return response(code=404, data=None, detail_message="data project not found")
        except Exception as e:
            return response(code=500, data=None, detail_message=str(e))
        
    def delete(self, request):
        id = request.query_params.get('id')

        try:
            try:
                data = Project.objects.get(id_project=id)
                data.delete()
                return response(code=201, data=None, detail_message="delete request success")
            except Project.DoesNotExist:
                return response(code=404, data=None, detail_message="data project not found")
        except Exception as e:
            return response(code=500, data=None, detail_message=str(e))
        

class ProjectCountView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        project = Project.objects.all()
        count_pending = 0
        count_progress = 0
        count_done = 0
        for p in list(project.values()):
            if search("On Progress", p['status']):
                count_progress += 1
            elif p['status'] == "Pending":
                count_pending += 1
            elif p['status'] == "Projek Selesai":
                count_done += 1
        
        self.data = {
            "project_count": {
                "count_pending": count_pending,
                "count_progress": count_progress,
                "count_done": count_done,
                "count_all": len(list(project.values()))
            }
        }

        return response(code=200, data=self.data, detail_message=None)
    
# class ProjectDeadlineView(APIView):
#     permission_classes = (IsAuthenticated, )

#     def get(self, request):
#         project = Project.objects.all().values_list('id_project','nama_project', 'id_customer_id').annotate(Min('estimasi_pengerjaan')).order_by('estimasi_pengerjaan')

#         print(list(project))

class ProjectPrintView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        id = request.query_params.get('id')

        # get project
        try:
            project = Project.objects.select_related('id_customer').get(id_project=id)

            # get cost
            cost_project = CostProjectSerializer(Cost_Project.objects.select_related('id_project').get(id_project_id=project.id), many=False)
            # get stok out
            stok_out = StokOutSerializer(Stok_Out.objects.filter(id_project_id=project.id).select_related('id_material', 'id_user', 'id_project', 'id_stok_gudang'), many=True)
            # get pekerjaan lain
            pekerjaan = PekerjaanLainSerializer(Pekerjaan_Lain.objects.filter(id_project_id=project.id), many=True)
            # get progress
            progress = ProgressProjectSerializer(Progress_Project.objects.filter(id_project_id=project.id), many=True)

            project_2 = ProjectSerializer(project, many=False)

            self.data = {
                "project": project_2.data,
                "cost_project": cost_project.data,
                "stok_out": stok_out.data,
                "pekerjaan_lain": pekerjaan.data,
                "progress": progress.data
            }

            return response(code=200, data=self.data, detail_message=None)
        
        except Project.DoesNotExist:
            return response(code=404, data=None, detail_message="data project not found")