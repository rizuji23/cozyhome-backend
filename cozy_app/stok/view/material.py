from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ...models import *
from ...serializers import *
from rest_framework.views import APIView
from ...etc import getuuid
from ...etc.response_get import response

class MaterialView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        if 'id_material' in request.query_params:
            materials = Material.objects.select_related('id_kategori_material').get(id_material=request.query_params.get('id_material'))
            serializer = MaterialSerializer(materials, many=False)
            self.data = {
                "material": serializer.data,
            }
            return response(code=200, data=self.data, detail_message=None) 
        else:
            materials = Material.objects.all().select_related('id_kategori_material').order_by('-id')
            seriliazer = MaterialSerializer(materials, many=True)
            self.data = {
                "material": seriliazer.data
            }
            return response(code=200, data=self.data, detail_message=None)
    
    def post(self, request):
        id_material = getuuid.Ramdom_Id.get_id()
        nama_material = request.data['nama_material']
        harga = request.data['harga']
        kategori_material = request.data['kategori_material']

        try:
            kategori_ma = Kategori_Material.objects.get(id_kategori_material=kategori_material)
            try:
                material_save = Material(id_material=id_material, nama_material=nama_material, harga=harga, id_kategori_material_id=kategori_ma.id)
                material_save.save()
                return response(code=201, data=None, detail_message="created request success")
            except Exception as e:
                return response(code=500, data=None, detail_message=str(e))
        except Kategori_Material.DoesNotExist:
            return response(code=404, data=None, detail_message="data kategori material not found")
            

    def put(self, request):
        id = request.query_params.get("id")
        nama_material = request.data['nama_material']
        harga = request.data['harga']
        kategori_material = request.data['kategori_material']
        try:
            try:
                data = Material.objects.get(id_material=id)
                data.nama_material = nama_material
                data.harga = harga
                data.id_kategori_material_id = kategori_material

                data.save()
                return response(code=201, data=None, detail_message="update request success")

            except Material.DoesNotExist:
                return response(code=404, data=None, detail_message="data material not found")
        except Exception as e:
            return response(code=500, data=None, detail_message=str(e))
        
    def delete(self, request):
        id = request.query_params.get("id")

        try:
            try:
                data = Material.objects.get(id_material=id)

                data.delete()
                return response(code=201, data=None, detail_message="delete request success")
            
            except Material.DoesNotExist:
                return response(code=404, data=None, detail_message="data material not found")
        
        except Exception as e:
            return response(code=500, data=None, detail_message=str(e))
        


        



        
