from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *

class CustomUser(UserAdmin):
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'role'
        )
     
    fieldsets = (
        (("Personal Info"), {"fields": ("first_name", "last_name")}),
        (("Account Info"), {"fields": ("username", "email", "password", "role")}),
    )

    add_fieldsets = (
            (
                None,
                {
                    'classes': ('wide',),
                    'fields': ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'role'),
                },
            ),
        )

class CustomerCustom(admin.ModelAdmin):
    list_display = ('nama_customer', 'no_telp', 'email', 'alamat', 'nama_perusahaan')

class ProjectCustom(admin.ModelAdmin):
    list_display = ('nama_project', 'id_customer', 'jumlah_volumn', 'kategori_project', 'total_cost')

class CostProjectCustom(admin.ModelAdmin):
    list_display = ('id_project', 'cost_design', 'cost_operasional', 'cost_produksi', 'cost_bahan', 'cost_lain')

class ProgressProjectCustom(admin.ModelAdmin):
    list_display = ('nama_progress', 'id_project', 'desc', 'status')

class MaterialCustom(admin.ModelAdmin):
    list_display = ('nama_material', 'id_kategori_material', 'harga')

class KategoriMaterialCustom(admin.ModelAdmin):
    list_display = ('nama_kategori')

class StokGudangCustom(admin.ModelAdmin):
    list_display = ('id_material', 'stok', 'last_stok', 'created_at', 'updated_at')

class StokInCustom(admin.ModelAdmin):
    list_display = ('id_material', 'stok_in', 'katerangan', 'created_at', 'updated_at')

class StokOutCustom(admin.ModelAdmin):
    list_display = ('id_material', 'id_project', 'stok_out', 'katerangan', 'created_at', 'updated_at')

class ModifiedStokCustom(admin.ModelAdmin):
    list_display = ('id_material', 'id_stok_gudang', 'stok', 'stok_in', 'stok_out', 'last_stok', 'keterangan', 'id_project', 'created_at', 'updated_at')

class User_DetailCustom(admin.ModelAdmin):
    list_display = ('id_user_detail', 'img', 'id_user')

class Pekerjaan_LainCustom(admin.ModelAdmin):
    list_display = ('id_pekerjaan_lain', 'id_project', 'nama_pekerjaan', 'desc', 'harga', 'id_user', 'created_at', 'updated_at')

admin.site.register(User, CustomUser)
admin.site.register(Customer, CustomerCustom)
admin.site.register(Project, ProjectCustom)
admin.site.register(Cost_Project, CostProjectCustom)
admin.site.register(Progress_Project, ProgressProjectCustom)
admin.site.register(Material, MaterialCustom)
admin.site.register(Kategori_Material)
admin.site.register(Stok_Gudang, StokGudangCustom)
admin.site.register(Stok_In, StokInCustom)
admin.site.register(Stok_Out, StokOutCustom)
admin.site.register(Modified_Stok, ModifiedStokCustom)
admin.site.register(User_Detail, User_DetailCustom)
admin.site.register(Pekerjaan_Lain, Pekerjaan_LainCustom)
# Register your models here.
