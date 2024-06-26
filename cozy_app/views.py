from django.shortcuts import render
from .serializers import *
from rest_framework.permissions import AllowAny
from django.contrib.auth.signals import user_logged_in
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
from rest_framework.views import APIView
from .etc import getuuid
from .etc.response_get import response

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        data['name'] = "%s %s" % (self.user.first_name, self.user.last_name)
        data['role'] = self.user.get_role_display()
        data['username'] = self.user.username
        data['id_user'] = self.user.id

        return data
    

class CustomTokenPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class MaterialView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        materials = Material.objects.all()
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
            material_save = Material(id_material=id_material, nama_material=nama_material, harga=harga, id_kategori_material_id=kategori_material)
            material_save.save()
            return response(code=201, data=None, detail_message="created request success")
        except Exception as e:
            return response(code=500, data=None, detail_message=str(e))
            

    def put(self, request):
        id = request.query_params.get("id")
        nama_material = request.data['nama_material']
        harga = request.data['harga']
        kategori_material = request.data['kategori_material']
        print("id",  id)
        try:
            try:
                data = Material.objects.get(id_material=id)
                data.nama_material = nama_material
                data.harga = harga
                data.id_kategori_material_id = kategori_material

                data.save()
                return response(code=201, data=None, detail_message="update request success")

            except Material.DoesNotExist:
                return response(code=404, data=None, detail_message="data not found")
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
                return response(code=404, data=None, detail_message="data not found")
        
        except Exception as e:
            return response(code=500, data=None, detail_message=str(e))
        

class KategoriMaterialView(APIView):
    permission_classes = (IsAuthenticated, )

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
            

class ChangeProfile(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        file_img = request.data.get('img', None)
        first_name = request.data['first_name']
        last_name = request.data['last_name']
        email = request.data['email']
        id_user = request.data['user']
        print("file_img", file_img)
        user = User.objects.get(id=id_user)
        try:
            if file_img == None or file_img == '' or file_img == 'undefined':
                try:
                    user.first_name = first_name
                    user.last_name = last_name
                    user.email = email
                    user.save()
                    return response(code=201, data=None, detail_message="update request success")
                except Exception as e:
                    return response(code=500, data=None, detail_message=str(e))
            else:
                try:
                    user.first_name = first_name
                    user.last_name = last_name
                    user.email = email
                    user.save()
                    try:
                        user_detail = User_Detail.objects.get(id_user_id=id_user)
                        try:
                            user_detail.img = file_img
                            user_detail.save()
                            return response(code=201, data=None, detail_message="update request success")
                        except Exception as e:
                            return response(code=500, data=None, detail_message=str(e))
                    except User_Detail.DoesNotExist:
                        try:
                            id_user_detail = getuuid.Ramdom_Id.get_id()
                            user_detail = User_Detail(id_user_detail=id_user_detail, img=file_img, id_user_id=id_user)
                            user_detail.save()
                            return response(code=201, data=None, detail_message="update request success")
                        except Exception as e:
                            return response(code=500, data=None, detail_message=str(e))
                except Exception as e:
                    return response(code=500, data=None, detail_message=str(e))
                
                    
        except User.DoesNotExist:
            return response(code=404, data=None, detail_message="user is not found")

