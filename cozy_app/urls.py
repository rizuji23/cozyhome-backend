from django.urls import re_path as urls

from . import views
from .stok import MaterialView, KategoriMaterialView, StokAllView, StokInView
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    urls('login/', views.CustomTokenPairView.as_view(), name="token_obtain_pair"),
    urls("kategori_material/", KategoriMaterialView.as_view(), name="get_kategori_material"),
    urls("kategori_material/", KategoriMaterialView.as_view(), name="get_kategori_material"),
    urls("material/", MaterialView.as_view(), name="get_material"),

    urls("stok/", StokAllView.as_view(), name="get_stok_all"),
    urls("stok_in/", StokInView.as_view(), name="stok_in"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
