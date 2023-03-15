from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.ReadOnlyField()

    class Meta(object):
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'date_joined', 'password')
        
        extra_kwargs = {'password': {'write_only': True}}

class KategoriMaterialSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Kategori_Material
        fields = ('id', 'id_kategori_material', 'nama_kategori', 'created_at', 'updated_at')


class MaterialSerializer(serializers.ModelSerializer):
    nama_kategori = serializers.CharField(source="id_kategori_material.nama_kategori", read_only=True)
    class Meta(object):
        model = Material
        fields = ('id_material', 'id_kategori_material_id','nama_kategori', 'nama_material', 'harga', 'created_at', 'updated_at')

class StokGudangSerializer(serializers.ModelSerializer):
    nama_material = serializers.CharField(source="id_material.nama_material", read_only=True)

    kategori_material = serializers.CharField(source="id_material.id_kategori_material.nama_kategori", read_only=True)

    class Meta(object):
        model = Stok_Gudang
        fields = ('id_stok_gudang', 'id_material', 'nama_material', 'kategori_material', 'stok', 'last_stok', 'created_at', 'updated_at')

class StokInSerializer(serializers.ModelSerializer):
    nama_material = serializers.CharField(source="id_material.nama_material", read_only=True)
    kategori_material = serializers.CharField(source="id_material.id_kategori_material.nama_kategori", read_only=True)
    username = serializers.CharField(source="id_user.username", read_only=True)

    class Meta(object):
        model = Stok_In
        fields = ('id_stok_in', 'id_stok_gudang', 'nama_material', 'kategori_material', 'stok_in', 'katerangan', 'username', 'created_at', 'updated_at')



