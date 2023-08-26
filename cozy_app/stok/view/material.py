from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ...models import *
from ...serializers import *
from rest_framework.views import APIView
from ...etc import getuuid
from ...etc.response_get import response
from django.db.models import Sum

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

                # save to stok_gudang
                get_material = Material.objects.get(id_material=id_material)
                id_stok_gudang = getuuid.Ramdom_Id.get_id()
                stok_gudang = Stok_Gudang(id_stok_gudang=id_stok_gudang, id_material_id=get_material.id, stok=0, last_stok=0)

                stok_gudang.save()

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
                kategori = Kategori_Material.objects.get(id_kategori_material=kategori_material)
                data = Material.objects.get(id_material=id)
                data.nama_material = nama_material
                data.harga = harga
                data.id_kategori_material_id = kategori.id

                data.save()
                return response(code=201, data=None, detail_message="update request success")

            except Material.DoesNotExist or Kategori_Material.DoesNotExist:
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
        
class AlatView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        id_alat = request.query_params.get('id', 'all')

        if id_alat != 'all':
            try:
                get_alat = AlatSerializer(Alat.objects.get(id_alat=id_alat), many=False)

                self.data = {
                    "alat": get_alat.data
                }

                return response(code=200, data=self.data, detail_message=None)

            except Alat.DoesNotExist:
                return response(code=404, data=None, detail_message="data alat not found")
        
        else:
            alat = AlatSerializer(Alat.objects.all(), many=True)

            self.data = {
                "alat": alat.data
            }

            return response(code=200, data=self.data, detail_message=None)
        
    def post(self, request):
        id_alat = getuuid.Ramdom_Id.get_id()
        nama_alat = request.data['nama_alat']
        harga_alat = request.data['harga_alat']
        qty = request.data['qty']
        
        total_harga = int(harga_alat) * int(qty)

        try:
            alat = Alat(id_alat=id_alat, nama_alat=nama_alat, harga_alat=harga_alat, total_harga=total_harga, qty=qty)

            alat.save()

            return response(code=201, data=None, detail_message="created request success")
        
        except Exception as e:
            return response(code=500, data=None, detail_message=str(e))
        
    def put(self, request):
        id_alat = request.data['id']
        nama_alat = request.data['nama_alat']
        harga_alat = request.data['harga_alat']
        qty = request.data['qty']
                
        total_harga = int(harga_alat) * int(qty)

        try:
            try:
                alat = Alat.objects.get(id_alat=id_alat)

                alat.nama_alat = nama_alat
                alat.harga_alat = harga_alat
                alat.total_harga = total_harga

                alat.save()

                return response(code=201, data=None, detail_message="updated request success")
            
            except Alat.DoesNotExist:
                return response(code=404, data=None, detail_message="data alat not found")
        except Exception as e:
            return response(code=500, data=None, detail_message=str(e))
    
    def delete(self, request):
        id_alat = request.query_params.get('id')

        try:
            alat = Alat.objects.get(id_alat=id_alat)

            alat.delete()

            return response(code=201, data=None, detail_message="deleted request success")
            
        except Alat.DoesNotExist:
            return response(code=404, data=None, detail_message="data alat not found")
                
class CountAlat(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        total_harga = Alat.objects.aggregate(Sum('total_harga'))
        qty = Alat.objects.aggregate(Sum('qty'))

        self.data = {
            "total_harga": total_harga,
            "qty": qty
        }

        return response(code=200, data=self.data, detail_message=None)



        
