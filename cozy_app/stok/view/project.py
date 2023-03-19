from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ...models import *
from ...serializers import *
from rest_framework.views import APIView
from ...etc import getuuid
from ...etc.response_get import response
import datetime


class ProjectView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
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
        total_cost = request.data['total_cost']
        id_user = request.data['id_user']

        try:
            try:
                customer = Customer.objects.get(id_customer=id_customer)

                _customer = Project(id_project=id_project, id_customer_id=customer.id, nama_project=nama_project, jumlah_volumn=jumlah_volumn, estimasi_pengerjaan=estimasi_pengerjaan, kategori_project=kategori_project, total_cost=total_cost, id_user_id=id_user)

                _customer.save()
                return response(code=201, data=None, detail_message="created request success")

            except Customer.DoesNotExist:
                return response(code=404, data=None, detail_message="data customer not found")
            
        except Exception as e:
            return response(code=500, data=None, detail_message=str(e))
        
    def put(self, request):
        id = request.query_params.get('id')
        id_customer = request.data['id_customer']
        nama_project = request.data['nama_project']
        jumlah_volumn = request.data['jumlah_volumn']
        estimasi_pengerjaan = request.data['estimasi_pengerjaan']
        kategori_project = request.data['kategori_project']
        total_cost = request.data['total_cost']
        id_user = request.data['id_user']

        try:
            try:
                customer = Customer.objects.get(id_customer=id_customer)
                try:
                    data = Project.objects.get(id_project=id)
                    data.id_customer_id = customer.id
                    data.nama_project = nama_project
                    data.jumlah_volumn = jumlah_volumn
                    data.estimasi_pengerjaan = estimasi_pengerjaan
                    data.kategori_project = kategori_project
                    data.total_cost = total_cost
                    data.id_user_id = id_user

                    data.save()

                    return response(code=201, data=None, detail_message="update request success")
                
                except Project.DoesNotExist:
                    return response(code=404, data=None, detail_message="data project not found")
            except Customer.DoesNotExist:
                return response(code=404, data=None, detail_message="data customer not found")
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