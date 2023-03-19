from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ...models import *
from ...serializers import *
from rest_framework.views import APIView
from ...etc import getuuid
from ...etc.response_get import response
import datetime

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
        stok_in = Stok_In.objects.filter(created_at__date=get_now)
        serializer = StokInSerializer(stok_in, many=True)
        self.data = {
            "stok_in": serializer.data
        }

        return response(code=200, data=self.data, detail_message=None)
    
    def post(self, request):
        id_stok_in = getuuid.Ramdom_Id.get_id()
        id_material = request.data['id_material']
        stok_in = request.data['stok_in']
        keterangan = request.data['keterangan']
        id_user = request.data['id_user']
        
        try:
            material = Material.objects.get(id_material=id_material)
            try:
                stok_gudang = Stok_Gudang.objects.get(id_material_id=material.id)
                calculate = stok_gudang.stok + stok_in
                stok_gudang.last_stok = stok_gudang.stok
                stok_gudang.stok = calculate

                try:
                    stok_gudang.save()
                    _stok_in = Stok_In(id_stok_in=id_stok_in, id_stok_gudang_id=stok_gudang.id, id_material_id=material.id, stok_in=stok_in, katerangan=keterangan, id_user_id=id_user)

                    _stok_in.save()

                    return response(code=201, data=None, detail_message="created request success")
                except Exception as e:
                    return response(code=500, data=None, detail_message=str(e))

            except Stok_Gudang.DoesNotExist:
                id_stok_gudang = getuuid.Ramdom_Id.get_id()

                try:
                    stok_gudang = Stok_Gudang(id_stok_gudang=id_stok_gudang, id_material_id=material.id, stok=stok_in, last_stok=0)
                    stok_gudang.save()

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

                with_id = StokOutSerializer(Stok_Out.objects.filter(id_project_id=project.id).select_related('id_material', 'id_user', 'id_project', 'id_stok_gudang'), many=True)

                self.data = {
                    "stok_out": with_id.data
                }

                return response(code=200, data=self.data, detail_message={'id_project': id_project, 'nama_project': project.nama_project})
            
            except Project.DoesNotExist:
                return response(code=404, data=None, detail_message="data project not found")
        
        else:
            with_id = StokOutSerializer(Stok_Out.objects.all().select_related('id_material', 'id_user', 'id_project', 'id_stok_gudang'), many=True)
            self.data = {
                "stok_out": with_id.data
            }

            return response(code=200, data=self.data, detail_message=None)


    def post(self, request):
        id_stok_out = getuuid.Ramdom_Id.get_id()
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
                        stok_gudang.last_stok = stok_gudang.stok
                        stok_gudang.stok = sum_out
                        stok_gudang.save()

                        _stok_out = Stok_Out(id_stok_out=id_stok_out, id_stok_gudang_id=stok_gudang.id, id_material_id=material.id, id_project_id=project.id, stok_out=stok_out, katerangan=keterangan, id_user_id=id_user)

                        _stok_out.save()

                        return response(code=201, data=None, detail_message="created request success")

                    except Exception as e:
                        return response(code=500, data=None, detail_message=str(e))
                    
                except Stok_Gudang.DoesNotExist:
                    return response(code=404, data=None, detail_message="data stok gudang not found")
            except Material.DoesNotExist:
                return response(code=404, data=None, detail_message="data material not found")
        except Project.DoesNotExist:
            return response(code=404, data=None, detail_message="data project not found")
        


    


