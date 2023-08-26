from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ...models import *
from ...serializers import *
from rest_framework.views import APIView
from ...etc import getuuid
from ...etc.response_get import response
import datetime
from django.db.models import Sum


class StokAllView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        data = StokGudangSerializer(Stok_Gudang.objects.all().select_related('id_material'), many=True)
        self.data = {
            "stok": data.data
        }

        return response(code=200, data=self.data, detail_message=None)


class StokInView(APIView):
    permission_classes = (IsAuthenticated, ) 

    def get(self, request):
        get_now = datetime.date.today()
        stok_in = Stok_In.objects.all().order_by('-id')
        serializer = StokInSerializer(stok_in, many=True)
        self.data = {
            "stok_in": serializer.data
        }

        return response(code=200, data=self.data, detail_message=None)
    
    def post(self, request):
        id_stok_in = getuuid.Ramdom_Id.get_id()
        id_toko_material = getuuid.Ramdom_Id.get_id()
        id_material = request.data['id_material']
        stok_in = request.data['stok_in']
        keterangan = request.data['keterangan']
        id_user = request.data['id_user']
        nama_toko = request.data['nama_toko']
        
        try:
            material = Material.objects.get(id_material=id_material)    
            id_modified_stok = getuuid.Ramdom_Id.get_id()
            try:
                stok_gudang = Stok_Gudang.objects.get(id_material_id=material.id)
                calculate = stok_gudang.stok + stok_in
                stok_gudang.last_stok = stok_gudang.stok
                stok_gudang.stok = calculate

                try:
                    modified_stok = Modified_Stok(id_modified_stok=id_modified_stok, id_stok_gudang_id=stok_gudang.id, id_material_id=material.id, stok=stok_gudang.stok + stok_in, last_stok=stok_gudang.stok, stok_in=stok_in, stok_out=None, keterangan="Stok Masuk", id_user_id=id_user)
                    modified_stok.save()
                    stok_gudang.save()
                    _stok_in = Stok_In(id_stok_in=id_stok_in, id_stok_gudang_id=stok_gudang.id, id_material_id=material.id, stok_in=stok_in, katerangan=keterangan, id_user_id=id_user)

                    _stok_in.save()

                    get_stok_in = Stok_In.objects.get(id_stok_in=id_stok_in)
                    get_modif = Modified_Stok.objects.get(id_modified_stok=id_modified_stok)

                    try:
                        toko_get = Toko_Material.objects.get(id_toko_material=nama_toko)

                        get_modif.nama_toko = toko_get.nama_toko

                        get_modif.save()

                    except Toko_Material.DoesNotExist:
                        toko = Toko_Material(id_toko_material=id_toko_material, id_stok_in_id=get_stok_in.id, nama_toko=nama_toko, keterangan=None)
                        
                        get_modif.nama_toko = nama_toko

                        get_modif.save()
                        toko.save()

                    return response(code=201, data=None, detail_message="created request success")
                except Exception as e:
                    return response(code=500, data=None, detail_message=str(e))

            except Stok_Gudang.DoesNotExist:
                id_stok_gudang = getuuid.Ramdom_Id.get_id()

                try:
                    stok_gudang = Stok_Gudang(id_stok_gudang=id_stok_gudang, id_material_id=material.id, stok=stok_in, last_stok=0)
                    stok_gudang.save()

                    get_stok = Stok_Gudang.objects.get(id_stok_gudang=id_stok_gudang)

                    modified_stok = Modified_Stok(id_modified_stok=id_modified_stok, id_stok_gudang_id=get_stok.id, id_material_id=material.id, stok=stok_in, last_stok=0, stok_in=stok_in, stok_out=None, keterangan="Stok Masuk", id_user_id=id_user)
                    modified_stok.save()

                    get_gudang = Stok_Gudang.objects.get(id_stok_gudang=id_stok_gudang)

                    _stok_in = Stok_In(id_stok_in=id_stok_in, id_stok_gudang_id=get_gudang.id, id_material_id=material.id, stok_in=stok_in, katerangan=keterangan, id_user_id=id_user)

                    _stok_in.save()
                    return response(code=201, data=None, detail_message="created request success")
                except Exception as e:
                    return response(code=500, data=None, detail_message=str(e))

        except Material.DoesNotExist:
            return response(code=404, data=None, detail_message="data material not found")


class StokOutView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        if 'id_project' in request.query_params:
            id_project = request.query_params.get('id_project')
            try:
                project = Project.objects.get(id_project=id_project)

                with_id = StokOutSerializer(Stok_Out.objects.filter(id_project_id=project.id).select_related('id_material', 'id_user', 'id_project', 'id_stok_gudang').order_by('-id'), many=True)

                self.data = {
                    "stok_out": with_id.data
                }

                return response(code=200, data=self.data, detail_message={'id_project': id_project, 'nama_project': project.nama_project})
            
            except Project.DoesNotExist:
                return response(code=404, data=None, detail_message="data project not found")
        
        else:
            with_id = StokOutSerializer(Stok_Out.objects.all().select_related('id_material', 'id_user', 'id_project', 'id_stok_gudang').order_by('-id'), many=True)
            self.data = {
                "stok_out": with_id.data
            }

            return response(code=200, data=self.data, detail_message=None)


    def post(self, request):
        id_stok_out = getuuid.Ramdom_Id.get_id()
        id_modified_stok = getuuid.Ramdom_Id.get_id()
        id_stok_gudang = request.data['id_stok_gudang']
        id_material = request.data['id_material']
        id_project = request.data['id_project']
        stok_out = request.data['stok_out']
        keterangan = request.data['keterangan']
        id_user = request.data['id_user']

        try:
            project = Project.objects.get(id_project=id_project)
            try:
                material = Material.objects.get(id_material=id_material)
                try:
                    stok_gudang = Stok_Gudang.objects.get(id_stok_gudang=id_stok_gudang)

                    sum_out = int(stok_gudang.stok) - int(stok_out)

                    try:
                        modified_stok = Modified_Stok(id_modified_stok=id_modified_stok, id_stok_gudang_id=stok_gudang.id, id_material_id=material.id, stok=sum_out, last_stok=sum_out, stok_in=None, stok_out=stok_out, keterangan="Stok Keluar", id_user_id=id_user, id_project_id=project.id)
                        stok_gudang.last_stok = stok_gudang.stok
                        stok_gudang.stok = sum_out
                        stok_gudang.save()
                        modified_stok.save()

                        _stok_out = Stok_Out(id_stok_out=id_stok_out, id_stok_gudang_id=stok_gudang.id, id_material_id=material.id, id_project_id=project.id, stok_out=stok_out, katerangan=keterangan, id_user_id=id_user)

                        _stok_out.save()
                        total_bahan = int(material.harga) * int(stok_out)
                        cost_all = Cost_Project.objects.get(id_project_id=project.id)
                        total_all = int(total_bahan) + int(cost_all.cost_bahan)
                        cost_all.cost_bahan = total_all
                        cost_all.save()

                        cost_sum = cost_all.cost_produksi + cost_all.cost_bahan + cost_all.cost_design + cost_all.cost_operasional + cost_all.cost_lain

                        project.total_cost = cost_sum
                        project.save()

                        return response(code=201, data=None, detail_message="created request success")

                    except Exception as e:
                        return response(code=500, data=None, detail_message=str(e))
                    
                except Stok_Gudang.DoesNotExist:
                    return response(code=404, data=None, detail_message="data stok gudang not found")
            except Material.DoesNotExist:
                return response(code=404, data=None, detail_message="data material not found")
        except Project.DoesNotExist:
            return response(code=404, data=None, detail_message="data project not found")
        

class ModifiedStokView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        if 'sort' in request.query_params:
            if request.query_params.get('sort') != 'all':
                modified = Modified_Stok.objects.filter(keterangan=request.query_params.get('sort')).select_related('id_material')
                serializers = ModifiedStokSerializer(modified, many=True)
                self.data = {
                    "modified_stok": serializers.data
                }

                return response(code=200, data=self.data, detail_message=None)
            else:
                modified = Modified_Stok.objects.all().select_related('id_material')
                serializers = ModifiedStokSerializer(modified, many=True)
                self.data = {
                    "modified_stok": serializers.data
                }

                return response(code=200, data=self.data, detail_message=None)  
            

class StokCountView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        stok_gudang = Stok_Gudang.objects.aggregate(Sum('stok')).get('stok__sum')
        stok_in = Stok_In.objects.aggregate(Sum('stok_in')).get('stok_in__sum')
        stok_out = Stok_Out.objects.aggregate(Sum('stok_out')).get('stok_out__sum')

        self.data = {
            "count": {
                "stok_gudang": stok_gudang,
                "stok_in": stok_in,
                "stok_out": stok_out
            }
        }

        return response(code=200, data=self.data, detail_message=None)
    
class StokCountSumView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        stok_gudang = Stok_Gudang.objects.all().select_related('id_material')
        stok_in = Stok_In.objects.all().select_related('id_material')
        stok_out = Stok_Out.objects.all().select_related('id_material')

        sum_total_asset = 0
        sum_stok_all = 0

        sum_stok_in = 0
        sum_stok_out = 0
        sum_asset_in = 0
        sum_asset_out = 0

        for i in stok_gudang:
            sum_total_asset += i.id_material.harga * i.stok
            sum_stok_all += i.stok

        for i in stok_in:
            sum_stok_in += i.stok_in
            sum_asset_in += i.id_material.harga * i.stok_in
        
        for i in stok_out:
            sum_stok_out += i.stok_out
            sum_asset_out += i.id_material.harga * i.stok_out

        print("sum_total_asset", sum_total_asset)
        print("sum_stok_all", sum_stok_all)

        self.data = {
            "sum": {
                "sum_total_asset": sum_total_asset,
                "sum_stok_all": sum_stok_all,
                "sum_stok_in": sum_stok_in,
                "sum_asset_in": sum_asset_in,
                "sum_stok_out": sum_stok_out,
                "sum_asset_out": sum_asset_out
            }
        }

        return response(code=200, data=self.data, detail_message=None) 

class DetailStok(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        id = request.query_params.get('id')

        # get data detail stok
        try:
            get_stok = Stok_Gudang.objects.get(id_stok_gudang=id)
            # get data modified stok
            print("DD", get_stok.id_material)
            try:
                get_material = Material.objects.get(id=get_stok.id_material_id)
                get_modified = Modified_Stok.objects.filter(id_stok_gudang_id=get_stok.id)
                
                seriali_stok = StokGudangSerializer(get_stok, many=False)
                seriali_modified = ModifiedStokSerializer(get_modified, many=True)
                seriali_material = MaterialSerializer(get_material, many=False)

                sum_asset_all = int(get_material.harga) * int(get_stok.stok)
                sum_stok_in = 0
                sum_stok_out = 0
                sum_asset_in = 0
                sum_asset_out = 0

                get_stok_in = Stok_In.objects.filter(id_stok_gudang_id=get_stok.id)
                get_stok_out = Stok_Out.objects.filter(id_stok_gudang_id=get_stok.id)

                for i in get_stok_in:
                    sum_stok_in += i.stok_in
                    sum_asset_in += i.id_material.harga * i.stok_in
                
                for i in get_stok_out:
                    sum_stok_out += i.stok_out
                    sum_asset_out += i.id_material.harga * i.stok_out

                self.data = {
                    "stok_info": seriali_stok.data,
                    "material": seriali_material.data,
                    "modified": seriali_modified.data,
                    "asset": {
                        "all": sum_asset_all,
                        "in": sum_asset_in,
                        "out": sum_asset_out
                    },
                    "stok": {
                        "in": sum_stok_in,
                        "out": sum_stok_out
                    }
                }

                return response(code=200, data=self.data, detail_message=None)
            except Material.DoesNotExist:
                return response(code=404, data=None, detail_message="data material not found")
        except Stok_Gudang.DoesNotExist:
            return response(code=404, data=None, detail_message="data stok gudang not found")
        
    def delete(self, request):
        id = request.query_params.get('id')

        try:
            try:
                data = Stok_Gudang.objects.get(id_stok_gudang=id)
                data_in = Stok_In.objects.filter(id_stok_gudang_id=data.id)
                data_out = Stok_Out.objects.filter(id_stok_gudang_id=data.id)
                modified = Modified_Stok.objects.filter(id_stok_gudang_id=data.id)
                data.stok = 0
                data.save()
                data_in.delete()
                data_out.delete()
                modified.delete()
                return response(code=201, data=None, detail_message="delete request success")
            except Stok_Gudang.DoesNotExist:
                return response(code=404, data=None, detail_message="data stok gudang not found")
        except Exception as e:
            return response(code=500, data=None, detail_message=str(e))
        
class NamaToko(APIView):
    permission_classes = (IsAuthenticated, )
    
    def get(self, request):
        id_material = request.query_params.get('id', 'all')

        if id_material != 'all':
            try:
                get_material = Material.objects.get(id_material=id_material)

                toko = NamaTokoSerializer(Toko_Material.objects.filter(id_material_id=get_material.id), many=True)

                self.data = {
                    "toko": toko.data
                }

                return response(code=200, data=self.data, detail_message=None)
            except Material.DoesNotExist:
                return response(code=404, data=None, detail_message="data Material not found")
        
        else:
            toko = NamaTokoSerializer(Toko_Material.objects.all(), many=True)

            self.data = {
                "toko": toko.data
            }

            return response(code=200, data=self.data, detail_message=None)

        