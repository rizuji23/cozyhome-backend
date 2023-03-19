from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ...models import *
from ...serializers import *
from rest_framework.views import APIView
from ...etc import getuuid
from ...etc.response_get import response

class KategoriMaterialView(APIView):
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        id = self.kwargs['id']
        return Kategori_Material.objects.filter(id_kategori_material=id)

    def get(self, request):
        kategori = KategoriMaterialSerializer(Kategori_Material.objects.all(), many=True)
        self.data = {
            "kategori_material": kategori.data
        }
        return response(code=200, data=self.data, detail_message=None)
    
    def post(self, request):
        id_kategori_material = getuuid.Ramdom_Id.get_id()
        nama_kategori = request.data['nama_kategori']

        try:
            kategori = Kategori_Material(id_kategori_material=id_kategori_material, nama_kategori=nama_kategori)
            kategori.save()
            return response(code=201, data=None, detail_message='created request success')
        except Exception as e:
            return response(code=500, data=None, detail_message=str(e))
        
    def put(self, request, format=None):
        id = request.query_params.get("id")
        nama_kategori = request.data['nama_kategori']

        try:
            try:
                data = Kategori_Material.objects.get(id_kategori_material=id)
                data.nama_kategori = nama_kategori
                data.save()

                return response(code=201, data=None, detail_message="update request success")
            
            except Kategori_Material.DoesNotExist:
                return response(code=404, data=None, detail_message="data kategori material not found")
        except Exception as e:
            return response(code=500, data=None, detail_message=str(e))

    def delete(self, request):
        id = request.query_params.get("id")

        try:
            try:
                data = Kategori_Material.objects.get(id_kategori_material=id)
                data.delete()

                return response(code=201, data=None, detail_message="delete request success")
            except Kategori_Material.DoesNotExist:
                return response(code=404, data=None, detail_message="data kategori material not found")

        except Exception as e:
            return response(code=500, data=None, detail_message=str(e))

        
    