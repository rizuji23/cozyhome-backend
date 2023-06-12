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
    id_kategori = serializers.CharField(source="id_kategori_material.id_kategori_material")
    class Meta(object):
        model = Material
        fields = ('id_material', 'id_kategori','nama_kategori', 'nama_material', 'harga', 'created_at', 'updated_at')

class StokGudangSerializer(serializers.ModelSerializer):
    nama_material = serializers.CharField(source="id_material.nama_material", read_only=True)

    harga_material = serializers.CharField(source="id_material.harga", read_only=True)

    id_material_2 = serializers.CharField(source="id_material.id_material", read_only=True)

    kategori_material = serializers.CharField(source="id_material.id_kategori_material.nama_kategori", read_only=True)

    class Meta(object):
        model = Stok_Gudang
        fields = ('id_stok_gudang', 'id_material', 'id_material_2', 'nama_material', 'harga_material', 'kategori_material', 'stok', 'last_stok', 'created_at', 'updated_at')

class StokInSerializer(serializers.ModelSerializer):
    nama_material = serializers.CharField(source="id_material.nama_material", read_only=True)
    kategori_material = serializers.CharField(source="id_material.id_kategori_material.nama_kategori", read_only=True)
    username = serializers.CharField(source="id_user.username", read_only=True)

    class Meta(object):
        model = Stok_In
        fields = ('id_stok_in', 'id_stok_gudang', 'nama_material', 'kategori_material', 'stok_in', 'katerangan', 'username', 'created_at', 'updated_at')

class ModifiedStokSerializer(serializers.ModelSerializer):
    nama_material = serializers.CharField(source="id_material.nama_material", read_only=True)

    kategori_material = serializers.CharField(source="id_material.id_kategori_material.nama_kategori", read_only=True)

    project = serializers.CharField(source="id_project.nama_project", read_only=True)

    class Meta(object):
        model = Modified_Stok
        fields = ('id_modified_stok', 'stok', 'last_stok', 'stok_in', 'stok_out', 'keterangan', 'id_user', 'created_at', 'updated_at', 'nama_material', 'kategori_material', 'project')

class StokOutSerializer(serializers.ModelSerializer):
    nama_material = serializers.CharField(source="id_material.nama_material", read_only=True)
    kategori_material = serializers.CharField(source="id_material.id_kategori_material.nama_kategori", read_only=True)
    username = serializers.CharField(source="id_user.username", read_only=True)

    nama_project = serializers.CharField(source="id_project.nama_project", read_only=True)

    id_stok_gudang = serializers.CharField(source="id_stok_gudang.id_stok_gudang", read_only=True)

    harga = serializers.CharField(source="id_material.harga", read_only=True)

    id_material_2 = serializers.CharField(source="id_material.id_material", read_only=True)

    class Meta(object):
        model = Stok_Out
        fields = ('id_stok_out', 'id_stok_gudang', 'nama_project', 'nama_material', 'id_material_2', 'harga', 'kategori_material', 'stok_out', 'katerangan', 'username', 'created_at', 'updated_at')

class CustomerSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Customer
        fields = ('id_customer', 'nama_customer', 'no_telp', 'email', 'alamat', 'nama_perusahaan', 'created_at', 'updated_at')


class ProjectSerializer(serializers.ModelSerializer):
    nama_customer = serializers.CharField(source="id_customer.nama_customer", read_only=True)

    class Meta(object):
        model = Project
        fields = ('id_project', 'nama_project', 'nama_customer', 'jumlah_volumn', 'estimasi_pengerjaan', 'kategori_project', 'total_cost', 'desc', 'status', 'start_date', 'end_date','created_at', 'updated_at')


class CostProjectSerializer(serializers.ModelSerializer):
    nama_project = serializers.CharField(source="id_project.nama_project", read_only=True)

    class Meta(object):
        model = Cost_Project
        fields = ('id_cost_project', 'nama_project', 'cost_design', 'cost_operasional', 'cost_produksi', 'cost_bahan', 'cost_lain', 'id_user', 'created_at', 'updated_at')

class ProgressProjectSerializer(serializers.ModelSerializer):
    nama_project = serializers.CharField(source="id_project.nama_project", read_only=True)

    class Meta(object):
        model = Progress_Project
        fields = ('id_progress_project', 'nama_project', 'nama_progress', 'desc', 'percentage', 'status', 'foto', 'id_user', 'created_at', 'updated_at')


class PekerjaanLainSerializer(serializers.ModelSerializer):
    nama_project = serializers.CharField(source="id_project.nama_project", read_only=True)

    class Meta(object):
        model = Pekerjaan_Lain
        fields = ('id_pekerjaan_lain', 'nama_project', 'nama_pekerjaan', 'desc','harga', 'id_user', 'created_at', 'updated_at')

class ProgressDetailSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Progress_Project
        fields = ('id_progress_project', 'nama_progress', 'desc', 'created_at', 'status', 'id_project_id')

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User_Detail
        fields = ('id_user_detail', 'img', 'id_user_id', 'created_at', 'updated_at')