from django.urls import re_path as urls

from . import views
from .stok import *
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import TokenBlacklistView

urlpatterns = [
    urls('login/', views.CustomTokenPairView.as_view(), name="token_obtain_pair"),
    urls('logout/', TokenBlacklistView.as_view(), name="logout"),
    urls("kategori_material/", KategoriMaterialView.as_view(), name="get_kategori_material"),
    urls("kategori_material/", KategoriMaterialView.as_view(), name="get_kategori_material"),
    urls("material/", MaterialView.as_view(), name="get_material"),

    urls('user/', UserView.as_view(), name='get_user'),

    urls("stok/", StokAllView.as_view(), name="get_stok_all"),
    urls("stok_in/", StokInView.as_view(), name="stok_in"),

    urls("stok_out/", StokOutView.as_view(), name="get_stok_out"),

    urls("customer/", CustomerView.as_view(), name="get_customer"),

    urls("project/", ProjectView.as_view(), name="get_project"),

    urls("cost/", CostProjectView.as_view(), name="get_cost_project"),

    urls("progress_project/", ProgressProjectView.as_view(), name="get_progress_project"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
