from django.db import models
from django.contrib.auth.models import AbstractUser
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
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nama_customer

class Project(models.Model):
    id = models.AutoField(primary_key=True)
    id_project = models.CharField(max_length=100)
    id_customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    nama_project = models.CharField(max_length=100)
    jumlah_volumn = models.CharField(max_length=100)
    estimasi_pengerjaan = models.CharField(max_length=100)
    kategori_project = models.CharField(max_length=50)
    total_cost = models.BigIntegerField()
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nama_project

class Cost_Project(models.Model):
    id = models.AutoField(primary_key=True)
    id_cost_project = models.CharField(max_length=100)
    id_project = models.ForeignKey(Project, on_delete=models.CASCADE)
    cost_design = models.BigIntegerField()
    cost_operasional = models.BigIntegerField()
    cost_produksi = models.BigIntegerField()
    cost_bahan = models.BigIntegerField()
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id_project

class Progress_Project(models.Model):
    id = models.AutoField(primary_key=True)
    id_progress_project = models.CharField(max_length=100)
    id_project = models.ForeignKey(Project, on_delete=models.CASCADE)
    nama_progress = models.CharField(max_length=100)
    desc = models.TextField(null=True)
    percentage = models.IntegerField()
    status = models.CharField(max_length=100)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
       return self.nama_progress

class Kategori_Material(models.Model):
    id = models.AutoField(primary_key=True)
    id_kategori_material = models.CharField(max_length=100)
    nama_kategori = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
       return self.nama_kategori

class Material(models.Model):
    id = models.AutoField(primary_key=True)
    id_material = models.CharField(max_length=100)
    id_kategori_material = models.ForeignKey(Kategori_Material, on_delete=models.CASCADE)
    nama_material = models.CharField(max_length=100)
    harga = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
       return self.nama_material

class Stok_Gudang(models.Model):
    id = models.AutoField(primary_key=True)
    id_stok_gudang = models.CharField(max_length=100)
    id_material = models.ForeignKey(Material, on_delete=models.CASCADE)
    stok = models.BigIntegerField()
    last_stok = models.BigIntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
       return self.id_stok_gudang


class Stok_In(models.Model):
    id = models.AutoField(primary_key=True)
    id_stok_in = models.CharField(max_length=100)
    id_stok_gudang = models.ForeignKey(Stok_Gudang, on_delete=models.CASCADE)
    id_material = models.ForeignKey(Material, on_delete=models.CASCADE)
    stok_in = models.BigIntegerField()
    katerangan = models.TextField(null=True)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
       return self.id_material

class Stok_Out(models.Model):
    id = models.AutoField(primary_key=True)
    id_stok_out = models.CharField(max_length=100)
    id_stok_gudang = models.ForeignKey(Stok_Gudang, on_delete=models.CASCADE)
    id_material = models.ForeignKey(Material, on_delete=models.CASCADE)
    id_project = models.ForeignKey(Project, on_delete=models.CASCADE)
    stok_out = models.BigIntegerField()
    katerangan = models.TextField(null=True)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
       return self.id_material
    
class Modified_Stok(models.Model):
    id = models.AutoField(primary_key=True)
    id_modified_stok = models.CharField(max_length=100)
    id_stok_gudang = models.ForeignKey(Stok_Gudang, on_delete=models.CASCADE)
    id_material = models.ForeignKey(Material, on_delete=models.CASCADE)
    stok = models.BigIntegerField()
    keterangan = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
       return self.id_modified_stok