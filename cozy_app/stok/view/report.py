from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ...models import *
from ...serializers import *
from rest_framework.views import APIView
from ...etc import getuuid
from ...etc.response_get import response
import datetime
from django.db.models import Sum

class PrintTransaksi(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        print("request", request.data)
        filter_type = request.query_params.get('tipe_filter')
        id = request.query_params.get('id')

        try:
            get_stok = Stok_Gudang.objects.get(id_stok_gudang=id)
            try:
                get_material = Material.objects.get(id=get_stok.id_material_id)
                if filter_type == "Semua":
                    # format 2021-08-12 YYYY-MM-DD
                    modified = Modified_Stok.objects.filter(id_stok_gudang_id=get_stok.id)
                    
                    seriali_stok = StokGudangSerializer(get_stok, many=False)
                    seriali_modified = ModifiedStokSerializer(modified, many=True)
                    seriali_material = MaterialSerializer(get_material, many=False)

                    get_stok_in = Stok_In.objects.filter(id_stok_gudang_id=get_stok.id)
                    get_stok_out = Stok_Out.objects.filter(id_stok_gudang_id=get_stok.id)
                elif filter_type == "Tanggal":
                    # format 2021-08-12 YYYY-MM-DD
                    start_date = request.query_params.get('start_date')
                    end_date = request.query_params.get('end_date')
                    modified = Modified_Stok.objects.filter(created_at__gte=start_date, created_at__lte=end_date, id_stok_gudang_id=get_stok.id)
                    
                    seriali_stok = StokGudangSerializer(get_stok, many=False)
                    seriali_modified = ModifiedStokSerializer(modified, many=True)
                    seriali_material = MaterialSerializer(get_material, many=False)

                    get_stok_in = Stok_In.objects.filter(id_stok_gudang_id=get_stok.id, created_at__gte=start_date, created_at__lte=end_date)
                    get_stok_out = Stok_Out.objects.filter(id_stok_gudang_id=get_stok.id, created_at__gte=start_date, created_at__lte=end_date)
                elif filter_type == "Bulan":
                    # format 2021-08-12 YYYY-MM
                    month = request.query_params.get('month')
                    year = request.query_params.get('year')
                    modified = Modified_Stok.objects.filter(created_at__month=month, created_at__year=year, id_stok_gudang_id=get_stok.id)
                    
                    seriali_stok = StokGudangSerializer(get_stok, many=False)
                    seriali_modified = ModifiedStokSerializer(modified, many=True)
                    seriali_material = MaterialSerializer(get_material, many=False)

                    get_stok_in = Stok_In.objects.filter(id_stok_gudang_id=get_stok.id, created_at__month=month, created_at__year=year)
                    get_stok_out = Stok_Out.objects.filter(id_stok_gudang_id=get_stok.id, created_at__month=month, created_at__year=year)
                elif filter_type == "Tahun":
                    # format 2021-08-12 YYYY-MM
                    year = request.query_params.get('year')
                    modified = Modified_Stok.objects.filter(created_at__year=year, id_stok_gudang_id=get_stok.id)
                    
                    seriali_stok = StokGudangSerializer(get_stok, many=False)
                    seriali_modified = ModifiedStokSerializer(modified, many=True)
                    seriali_material = MaterialSerializer(get_material, many=False)

                    get_stok_in = Stok_In.objects.filter(id_stok_gudang_id=get_stok.id, created_at__year=year)
                    get_stok_out = Stok_Out.objects.filter(id_stok_gudang_id=get_stok.id, created_at__year=year)

                sum_asset_all = int(get_material.harga) * int(get_stok.stok)
                sum_stok_in = 0
                sum_stok_out = 0
                sum_asset_in = 0
                sum_asset_out = 0

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
            except Modified_Stok.DoesNotExist:
               return response(code=404, data=None, detail_message="data modified not found")
        except Stok_Gudang.DoesNotExist:
            return response(code=404, data=None, detail_message="data stok gudang not found")