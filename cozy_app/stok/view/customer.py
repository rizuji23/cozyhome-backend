from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ...models import *
from ...serializers import *
from rest_framework.views import APIView
from ...etc import getuuid
from ...etc.response_get import response
import datetime

class CustomerView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        customer = CustomerSerializer(Customer.objects.all().order_by('-id'), many=True)

        self.data = {
            "customer": customer.data
        }

        return response(code=200, data=self.data, detail_message=None)
    

    def post(self, request):
        id_customer = getuuid.Ramdom_Id.get_id()
        nama_customer = request.data['nama_customer']
        no_telp = request.data['no_telp']
        email = request.data['email']
        alamat = request.data['alamat']
        nama_perusahaan = request.data['nama_perusahaan']
        id_user = request.data['id_user']

        try:
            customer = Customer(id_customer=id_customer, nama_customer=nama_customer, no_telp=no_telp, email=email, alamat=alamat, nama_perusahaan=nama_perusahaan, id_user_id=id_user)

            customer.save()
            return response(code=201, data=None, detail_message='created request success')
        
        except Exception as e:
            return response(code=500, data=None, detail_message=str(e))
        
    def put(self, request):
        id = request.query_params.get('id')
        nama_customer = request.data['nama_customer']
        no_telp = request.data['no_telp']
        email = request.data['email']
        alamat = request.data['alamat']
        nama_perusahaan = request.data['nama_perusahaan']
        id_user = request.data['id_user']

        try:
            try:
                data = Customer.objects.get(id_customer=id)
                data.nama_customer = nama_customer
                data.no_telp = no_telp
                data.email = email
                data.alamat = alamat
                data.nama_perusahaan = nama_perusahaan
                data.id_user_id = id_user

                data.save()
                return response(code=201, data=None, detail_message="update request success")

            except Customer.DoesNotExist:
                 return response(code=404, data=None, detail_message="data customer not found")
        except Exception as e:
            return response(code=500, data=None, detail_message=str(e))
        
    
    def delete(self, request):
        id = request.query_params.get("id")

        try:
            try:
                data = Customer.objects.get(id_customer=id)

                data.delete()

                return response(code=201, data=None, detail_message="delete request success")

            except Customer.DoesNotExist:
                return response(code=404, data=None, detail_message="data customer not found")
        
        except Exception as e:
            return response(code=500, data=None, detail_message=str(e))
        

class CustomerDetailView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        id = request.query_params.get('id_customer')

        try:
            customer = Customer.objects.get(id_customer=id)
            project = Project.objects.filter(id_customer_id=customer.id).select_related('id_customer')

            _customer = CustomerSerializer(customer, many=False)
            _project = ProjectSerializer(project, many=True)

            self.data = {
                "project": _project.data,
                "customer": _customer.data
            }

            
            return response(code=200, data=self.data, detail_message=None)
        except Customer.DoesNotExist:
            return response(code=404, data=None, detail_message="data customer not found")