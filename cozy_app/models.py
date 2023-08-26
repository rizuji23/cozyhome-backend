from django.db import models
from django.contrib.auth.models import AbstractUser
from simple_history.models import HistoricalRecords
# Create your models here.

class User(AbstractUser):
    STOK = 1
    PROJECT = 2
    ADMIN = 3

    ROLE_CHOICES = (
        (STOK, 'Stok Management'),
        (PROJECT, 'Project Management'),
        (ADMIN, 'Admin'),
    )

    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)


class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    id_customer = models.CharField(max_length=100)
    nama_customer = models.CharField(max_length=100)
    no_telp = models.CharField(max_length=15, null=True)
    email = models.CharField(max_length=100, null=True)
    alamat = models.TextField(null=True)
    nama_perusahaan = models.CharField(max_length=100)
    id_user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.nama_customer


class Project(models.Model):
    id = models.AutoField(primary_key=True)
    id_project = models.CharField(max_length=100)
    id_customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    nama_project = models.CharField(max_length=100)
    jumlah_volumn = models.CharField(max_length=100)
    estimasi_pengerjaan = models.CharField(max_length=100)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    kategori_project = models.CharField(max_length=50)
    total_cost = models.BigIntegerField()
    desc = models.TextField(null=True)
    status = models.CharField(max_length=100, null=True)
    id_user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.nama_project

class Cost_Project(models.Model):
    id = models.AutoField(primary_key=True)
    id_cost_project = models.CharField(max_length=100)
    id_project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
    cost_design = models.BigIntegerField(null=True)
    cost_operasional = models.BigIntegerField(null=True)
    cost_produksi = models.BigIntegerField(null=True)
    cost_bahan = models.BigIntegerField(null=True)
    cost_lain = models.BigIntegerField(null=True)
    id_user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.id_project.nama_project

class Progress_Project(models.Model):
    id = models.AutoField(primary_key=True)
    id_progress_project = models.CharField(max_length=100)
    id_project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
    nama_progress = models.CharField(max_length=100)
    desc = models.TextField(null=True)
    percentage = models.IntegerField(null=True)
    status = models.CharField(max_length=100)
    foto = models.FileField(upload_to='progress/', default='')
    id_user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
       return self.nama_progress

class Kategori_Material(models.Model):
    id = models.AutoField(primary_key=True)
    id_kategori_material = models.CharField(max_length=100)
    nama_kategori = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
       return self.nama_kategori

class Material(models.Model):
    id = models.AutoField(primary_key=True)
    id_material = models.CharField(max_length=100)
    id_kategori_material = models.ForeignKey(Kategori_Material, on_delete=models.DO_NOTHING)
    nama_material = models.CharField(max_length=100)
    harga = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
       return self.nama_material

class Stok_Gudang(models.Model):
    id = models.AutoField(primary_key=True)
    id_stok_gudang = models.CharField(max_length=100)
    id_material = models.ForeignKey(Material, on_delete=models.CASCADE, null=True)
    stok = models.BigIntegerField()
    last_stok = models.BigIntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
       return self.id_material.nama_material
    



class Stok_In(models.Model):
    id = models.AutoField(primary_key=True)
    id_stok_in = models.CharField(max_length=100)
    id_stok_gudang = models.ForeignKey(Stok_Gudang, on_delete=models.CASCADE)
    id_material = models.ForeignKey(Material, on_delete=models.CASCADE)
    stok_in = models.BigIntegerField()
    katerangan = models.TextField(null=True)
    id_user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
       return self.id_material.nama_material

class Stok_Out(models.Model):
    id = models.AutoField(primary_key=True)
    id_stok_out = models.CharField(max_length=100)
    id_stok_gudang = models.ForeignKey(Stok_Gudang, on_delete=models.CASCADE)
    id_material = models.ForeignKey(Material, on_delete=models.CASCADE)
    id_project = models.ForeignKey(Project, on_delete=models.CASCADE)
    stok_out = models.BigIntegerField()
    katerangan = models.TextField(null=True)
    id_user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
       return self.id_material.nama_material
    
class Modified_Stok(models.Model):
    id = models.AutoField(primary_key=True)
    id_modified_stok = models.CharField(max_length=100)
    id_stok_gudang = models.ForeignKey(Stok_Gudang, on_delete=models.DO_NOTHING)
    id_material = models.ForeignKey(Material, on_delete=models.DO_NOTHING)
    stok = models.BigIntegerField()
    last_stok = models.BigIntegerField(null=True)
    stok_in = models.BigIntegerField(null=True)
    stok_out = models.BigIntegerField(null=True)
    keterangan = models.CharField(max_length=50)
    id_project = models.ForeignKey(Project, on_delete=models.DO_NOTHING, null=True)
    id_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
       return self.id_material.nama_material
    
class Pekerjaan_Lain(models.Model):
    id = models.AutoField(primary_key=True)
    id_pekerjaan_lain = models.CharField(max_length=100)
    id_project = models.ForeignKey(Project, on_delete=models.DO_NOTHING)
    nama_pekerjaan = models.CharField(max_length=100)
    desc = models.TextField()
    harga = models.BigIntegerField(null=True)
    id_user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
       return self.nama_pekerjaan

class User_Detail(models.Model):
    id = models.AutoField(primary_key=True)
    id_user_detail = models.CharField(max_length=100)
    img = models.FileField(upload_to='img_user/', default='profile.png')
    id_user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.id_user_detail
    

class Activity_User(models.Model):
    id = models.AutoField(primary_key=True)
    id_activity_user = models.CharField(max_length=100)
    desc = models.TextField()
    id_user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.id_activity_user
