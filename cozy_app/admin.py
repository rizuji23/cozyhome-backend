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
        

admin.site.register(User, CustomUser)
admin.site.register(Customer)
admin.site.register(Project)
admin.site.register(Cost_Project)
admin.site.register(Progress_Project)
admin.site.register(Material)
admin.site.register(Kategori_Material)
admin.site.register(Stok_Gudang)
admin.site.register(Stok_In)
admin.site.register(Stok_Out)
admin.site.register(Modified_Stok)

# Register your models here.
