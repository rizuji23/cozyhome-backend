from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ...models import *
from ...serializers import *
from rest_framework.views import APIView
from ...etc import getuuid
from ...etc.response_get import response
import datetime
from django.db.models import Sum

class KategoriUnit(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        id_kategori_unit = request.query_params.get('id', None)

        if id_kategori_unit != 'all':
            try:
                get_kategori = KategoriUnitSerializer(Kategori_Unit.objects.get(id_kategori_unit=id_kategori_unit), many=False)

                self.data = {
                    "kategori_unit": get_kategori.data
                }

                return response(code=200, data=self.data, detail_message=None)
            except Kategori_Unit.DoesNotExist:
                return response(code=404, data=None, detail_message="data kategori unit not found")
        else:
            get_kategori = KategoriUnitSerializer(Kategori_Unit.objects.all(), many=True)

            self.data = {
                    "kategori_unit": get_kategori.data
                }

            return response(code=200, data=self.data, detail_message=None)
        
    def post(self, request):
        id_kategori_unit = getuuid.Ramdom_Id.get_id()
        nama_kategori = request.data['nama_kategori']

        try:
            kategori_unit = Kategori_Unit(id_kategori_unit=id_kategori_unit, nama_kategori=nama_kategori)

            kategori_unit.save()

            return response(code=201, data=None, detail_message="created request success")

        except Exception as e:
            return response(code=500, data=None, detail_message=str(e))
        
    def put(self, request):
        id_kategori_unit = request.data['id']
        nama_kategori = request.data['nama_kategori']

        try:
            try:
                kategori_unit = Kategori_Unit.objects.get(id_kategori_unit=id_kategori_unit)

                kategori_unit.nama_kategori = nama_kategori

                kategori_unit.save()

                return response(code=201, data=None, detail_message="update request success")
            except Kategori_Unit.DoesNotExist:
                return response(code=404, data=None, detail_message="data kategori unit not found")
        except Exception as e:
            return response(code=500, data=None, detail_message=str(e))
    
    def delete(self, request):
        id_kategori_unit = request.query_params.get('id')

        try:
            kategori_unit = Kategori_Unit.objects.get(id_kategori_unit=id_kategori_unit)

            kategori_unit.delete()

            return response(code=201, data=None, detail_message="delete request success")
        except Kategori_Unit.DoesNotExist:
            return response(code=404, data=None, detail_message="data kategori unit not found")
        

class RincianUnit(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        id_rincian_unit = request.query_params.get('id', None)

        if id_rincian_unit != 'all':
            try:
                get_rincian = RincianUnitSerializer(Rincian_Unit.objects.get(id_rincian_unit=id_rincian_unit), many=False)
                
                self.data = {
                    "rincian_unit": get_rincian.data
                }

                return response(code=200, data=self.data, detail_message=None)
            except Rincian_Unit.DoesNotExist:
                return response(code=404, data=None, detail_message="data rincian unit not found")
        
        else:
            get_rincian = RincianUnitSerializer(Rincian_Unit.objects.all(), many=True)
                
            self.data = {
                "rincian_unit": get_rincian.data
            }

            return response(code=200, data=self.data, detail_message=None)
        
    def post(self, request):
        id_rincian_unit = getuuid.Ramdom_Id.get_id()
        nama_unit = request.data['nama_unit']
        id_kategori_unit = request.data['id_kategori_unit']
        dimensi = request.data['dimensi']
        desc = request.data['desc']
        id_project = request.data['id_project']

        try:
            try:
                try:
                    kategori = Kategori_Unit.objects.get(id_kategori_unit=id_kategori_unit)

                    project = Project.objects.get(id_project=id_project)

                    rincian = Rincian_Unit(id_rincian_unit=id_rincian_unit, id_kategori_unit_id=kategori.id, nama_unit=nama_unit, dimensi=dimensi, desc=desc, id_project_id=project.id)

                    rincian.save()

                    return response(code=201, data=None, detail_message="created request success")
                except Project.DoesNotExist:
                    return response(code=404, data=None, detail_message="data project not found")
            except Kategori_Unit.DoesNotExist:
                return response(code=404, data=None, detail_message="data kategori unit not found")

        except Exception as e:
            return response(code=500, data=None, detail_message=str(e))
    
    def put(self, request):
        id_rincian_unit = request.data['id']
        type_edit = request.data['type_edit']
          

        try:
            try:
                rincian = Rincian_Unit.objects.get(id_rincian_unit=id_rincian_unit)

                if type_edit == 'cost_produksi':
                    cost_produksi = request.data['cost_produksi']
                    rincian.cost_produksi = cost_produksi
                elif type_edit == 'cost_operasional':
                    print(type_edit)  
                    cost_operasional = request.data['cost_operasional']
                    rincian.cost_operasional = cost_operasional
                else:
                    nama_unit = request.data['nama_unit']
                    id_kategori_unit = request.data['id_kategori_unit']
                    dimensi = request.data['dimensi']
                    desc = request.data['desc']
                    id_project = request.data['id_project']
                    try:
                        try:
                            kategori = Kategori_Unit.objects.get(id_kategori_unit=id_kategori_unit)

                            project = Project.objects.get(id_project=id_project)

                            rincian.nama_unit = nama_unit
                            rincian.id_kategori_unit_id = kategori.id
                            rincian.dimensi = dimensi
                            rincian.desc = desc
                            rincian.id_project_id = project.id

                        except Project.DoesNotExist:
                            return response(code=404, data=None, detail_message="data project not found")
                    except Kategori_Unit.DoesNotExist:
                        return response(code=404, data=None, detail_message="data kategori unit not found")
                    
                rincian.save()
                return response(code=201, data=None, detail_message="updated request success")
            
            except Rincian_Unit.DoesNotExist:
                return response(code=404, data=None, detail_message="data rincian unit not found")
        except Exception as e:
            return response(code=500, data=None, detail_message=str(e))
        
    def delete(self, request):
        id_rincian_unit = request.data['id']

        try:
            rincian = Rincian_Unit.objects.get(id_rincian_unit=id_rincian_unit)

            rincian.delete()

            return response(code=201, data=None, detail_message="delete request success")
        except Rincian_Unit.DoesNotExist:
            return response(code=404, data=None, detail_message="data rincian unit not found")


class KebutuhanMaterialUnit(APIView):
    permission_classes = (IsAuthenticated, )
    
    def get(self, request):
        type_get = request.query_params.get('type_get', None)
        id_kebutuhan_material_unit = request.query_params.get('id', None)

        if type_get != 'all':
            try:
                kebutuhan = KebutuhanMaterialSerializer(Kebutuhan_Material_Unit.objects.get(id_kebutuhan_material_unit=id_kebutuhan_material_unit), many=False)

                self.data = {
                    "kebutuhan_unit": kebutuhan.data
                }

                return response(code=200, data=self.data, detail_message=None)

            except Kebutuhan_Material_Unit.DoesNotExist:
                return response(code=404, data=None, detail_message="data kebutuhan unit not found")
        else:
            try:
                rincian = Rincian_Unit.objects.get(id_rincian_unit=id_kebutuhan_material_unit)

                kebutuhan = KebutuhanMaterialSerializer(Kebutuhan_Material_Unit.objects.filter(id_rincian_unit_id=rincian.id), many=True)

                self.data = {
                    "kebutuhan_unit": kebutuhan.data
                }

                return response(code=200, data=self.data, detail_message=None)

            except Rincian_Unit.DoesNotExist:
                return response(code=404, data=None, detail_message="data rincian unit not found")
            
    def post(self, request):
        id_rincian_unit = request.data['id']
        id_kebutuhan_material_unit = getuuid.Ramdom_Id.get_id()
        nama_bahan = request.data['nama_bahan']
        harga = request.data['harga']
        qty = request.data['qty']
        total = request.data['total']

        try:
            try:
                rincian = Rincian_Unit.objects.get(id_rincian_unit=id_rincian_unit)

                kebutuhan = Kebutuhan_Material_Unit(id_kebutuhan_material_unit=id_kebutuhan_material_unit, id_rincian_unit_id=rincian.id, nama_bahan=nama_bahan, harga=harga, qty=qty, total=total)

                kebutuhan.save()
                return response(code=201, data=None, detail_message="created request success")
            except Rincian_Unit.DoesNotExist:
                return response(code=404, data=None, detail_message="data rincian unit not found")
        except Exception as e:
            return response(code=500, data=None, detail_message=str(e))
        
    def put(self, request):
        id_rincian_unit = request.data['id_rincian_unit']
        id_kebutuhan_material_unit = request.data['id']
        nama_bahan = request.data['nama_bahan']
        harga = request.data['harga']
        qty = request.data['qty']
        total = request.data['total']

        try:
            try:
                try:
                    rincian = Rincian_Unit.objects.get(id_rincian_unit=id_rincian_unit)

                    kebutuhan = Kebutuhan_Material_Unit.objects.get(id_kebutuhan_material_unit=id_kebutuhan_material_unit)

                    kebutuhan.nama_bahan = nama_bahan
                    kebutuhan.harga = harga
                    kebutuhan.qty = qty
                    kebutuhan.total = total
                    kebutuhan.id_rincian_unit_id = rincian.id

                    return response(code=201, data=None, detail_message="update request success")

                except Rincian_Unit.DoesNotExist:
                    return response(code=404, data=None, detail_message="data rincian unit not found")
            except Kebutuhan_Material_Unit.DoesNotExist:
                return response(code=404, data=None, detail_message="data kebutuhan unit not found")
        except Exception as e:
            return response(code=500, data=None, detail_message=str(e))
        
    def delete(self, request):
        id_kebutuhan_material_unit = request.query_params.get('id')

        try:
            kebutuhan = Kebutuhan_Material_Unit.objects.get(id_kebutuhan_material_unit=id_kebutuhan_material_unit)

            kebutuhan.delete()
            
            return response(code=201, data=None, detail_message="delete request success")
        
        except Kebutuhan_Material_Unit.DoesNotExist:
            return response(code=404, data=None, detail_message="data kebutuhan unit not found")
        
class PekerjaanLainUnit(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        type_get = request.query_params.get('type_get', None)
        id_pekerjaan_lain_unit = request.query_params.get('id', None)

        if type_get != 'all':
            try:
                pekerjaan_lain = PekerjaanLainUnitSerializer(Pekerjaan_Lain_Unit.objects.get(id_pekerjaan_lain_unit=id_pekerjaan_lain_unit), many=False)

                self.data = {
                    "pekerjaan_lain": pekerjaan_lain.data
                }

                return response(code=200, data=self.data, detail_message=None)

            except Pekerjaan_Lain_Unit.DoesNotExist:
                return response(code=404, data=None, detail_message="data pekerjaan lain unit not found")
        else:
            try:
                rincian = Rincian_Unit.objects.get(id_rincian_unit=id_pekerjaan_lain_unit)

                pekerjaan_lain = PekerjaanLainUnitSerializer(Pekerjaan_Lain_Unit.objects.filter(id_rincian_unit_id=rincian.id), many=True)

                self.data = {
                    "pekerjaan_lain": pekerjaan_lain.data
                }

                return response(code=200, data=self.data, detail_message=None)

            except Rincian_Unit.DoesNotExist:
                return response(code=404, data=None, detail_message="data rincian unit not found")

    def post(self, request):
        id_pekerjaan_lain_unit = getuuid.Ramdom_Id.get_id()
        id_rincian_unit = request.data['id']
        judul_pekerjaan = request.data['judul_pekerjaan']
        harga = request.data['harga']
        desc = request.data['desc']

        try:
            try:
                rincian = Rincian_Unit.objects.get(id_rincian_unit=id_rincian_unit)

                pekerjaan_lain = Pekerjaan_Lain_Unit(id_pekerjaan_lain_unit=id_pekerjaan_lain_unit, id_rincian_unit_id=rincian.id, judul_pekerjaan=judul_pekerjaan, harga=harga, desc=desc)

                pekerjaan_lain.save()

                return response(code=201, data=None, detail_message="created request success")

            except Rincian_Unit.DoesNotExist:
                return response(code=404, data=None, detail_message="data rincian unit not found")
        except Exception as e:
            return response(code=500, data=None, detail_message=str(e))
        
class ImageUnit(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        id_rincian_unit = request.query_params.get('id')

        try:
            rincian = Rincian_Unit.objects.get(id_rincian_unit=id_rincian_unit)

            image = ImageUnitSerializer(Image_Unit.objects.filter(id_rincian_unit_id=rincian.id), many=True)

            self.data = {
                "image_unit": image.data
            }

            return response(code=200, data=self.data, detail_message=None)
            
        except Rincian_Unit.DoesNotExist:
            return response(code=404, data=None, detail_message="data rincian unit not found")
        
    def post(self, request):
        id_image_unit = getuuid.Ramdom_Id.get_id()
        id_rincian_unit = request.data['id']
        url_image = request.data['image']

        try:
            try:
                rincian = Rincian_Unit.objects.get(id_rincian_unit=id_rincian_unit)

                image = Image_Unit(id_image_unit=id_image_unit, url_image=url_image, id_rincian_unit_id=rincian.id)

                image.save()

                return response(code=201, data=None, detail_message="created request success")

            except Rincian_Unit.DoesNotExist:
                return response(code=404, data=None, detail_message="data rincian unit not found")
        except Exception as e:
                return response(code=500, data=None, detail_message=str(e))

    def put(self, request):
        id_image_unit = request.data['id']
        id_rincian_unit = request.data['id_rincian_unit']
        url_image = request.data['image']

        try:
            try:
                rincian = Rincian_Unit.objects.get(id_rincian_unit=id_rincian_unit)

                image = Image_Unit.objects.get(id_image_unit=id_image_unit, id_rincian_unit_id=rincian.id)

                image.url_image = url_image

                image.save()

                return response(code=201, data=None, detail_message="updated request success")

            except Rincian_Unit.DoesNotExist:
                return response(code=404, data=None, detail_message="data rincian unit not found")
        except Exception as e:
                return response(code=500, data=None, detail_message=str(e))
        
    def delete(self, request):
        id_image_unit = request.query_params.get('id')
        id_rincian_unit = request.query_params.get('id_rincian_unit')

        try:
            try:
                rincian = Rincian_Unit.objects.get(id_rincian_unit=id_rincian_unit)

                image = Image_Unit.objects.get(id_image_unit=id_image_unit, id_rincian_unit_id=rincian.id)
                image.delete()

                return response(code=201, data=None, detail_message="deleted request success")

            except Rincian_Unit.DoesNotExist:
                return response(code=404, data=None, detail_message="data rincian unit not found")
        except Exception as e:
                return response(code=500, data=None, detail_message=str(e))