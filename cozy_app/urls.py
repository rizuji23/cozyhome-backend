from django.urls import re_path as urls

from . import views
from .stok import *
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import TokenBlacklistView

urlpatterns = [
    urls('login/', views.CustomTokenPairView.as_view(), name="token_obtain_pair"),
    urls('logout/', TokenBlacklistView.as_view(), name="logout"),
    urls('change_password/', ChangePasswordView.as_view(), name="change_password"),

    urls("kategori_material/", KategoriMaterialView.as_view(), name="get_kategori_material"),
    urls("material/", MaterialView.as_view(), name="get_material"),

    urls('user/', UserView.as_view(), name='get_user'),

    urls("stok/", StokAllView.as_view(), name="get_stok_all"),
    urls("stok_in/", StokInView.as_view(), name="stok_in"),

    urls("stok_out/", StokOutView.as_view(), name="get_stok_out"),

    urls("stok_count/", StokCountView.as_view(), name="get_stok_count"),

    urls("customer/", CustomerView.as_view(), name="get_customer"),

    urls("project/", ProjectView.as_view(), name="get_project"),
    urls("project_count/", ProjectCountView.as_view(), name="get_count_project"),
    urls("project_print/", ProjectPrintView.as_view(), name="get_count_project"),
    urls("cost/", CostProjectView.as_view(), name="get_cost_project"),
    urls('cost_sum/', CostProjectSumView.as_view(), name="get_cost_sum"),

    urls("progress/", ProgressProjectView.as_view(), name="get_progress_project"),
    urls("progress_detail/", ProgressDetailView.as_view(), name="get_progress_detail"),

    urls("customer_detail/", CustomerDetailView.as_view(), name="get_detail_customer"),

    urls("cost_produksi/", CostProduksiView.as_view(), name="cost_produksi"),
    urls("cost_design/", CostDesignView.as_view(), name="cost_design"),
    urls("cost_operasional/", CostOperasionalView.as_view(), name="cost_operasional"),

    urls("pekerjaan_lain/", PekerjaanLainView.as_view(), name="pekerjaan_lain"),
    urls("modified/", ModifiedStokView.as_view(), name="modified_stok_get"),
    urls("stok_sum/", StokCountSumView.as_view(), name="get_sum_stok"),
    urls('update_info/', views.ChangeProfile.as_view(), name="update_info_user"),
    urls('analisis/', AnalisisProjectView.as_view(), name="analisis_project"),
    urls('stok_detail/', DetailStok.as_view(), name="stok_detail"),
    urls('print/transaksi/', PrintTransaksi.as_view(), name="print_stok"),
    urls('print/all/', PrintAll.as_view(), name="print_stok")
]

urlpatterns = format_suffix_patterns(urlpatterns)
