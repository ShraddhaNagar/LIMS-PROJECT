# models.py
from django.utils import timezone
from django.db import models

class IncomingMaterial(models.Model):
    date_of_indent = models.DateField()
    material = models.CharField(max_length=100)
    makes = models.CharField(max_length=100, default='Some default value')
    model_no = models.CharField(max_length=100, default='Default Model No.')  
    po_no = models.CharField(max_length=100,default='Default Model No.')
    date_of_order = models.DateField(default=timezone.now)
    description = models.TextField()
    grade = models.CharField(max_length=20)
    supplier_nameaddress = models.CharField(max_length=100)
    incoming_material_inspection = models.CharField(max_length=20)
    quantity = models.PositiveIntegerField()
    material_received_date = models.DateField()
    hsn_sac = models.CharField(max_length=20, default='None')
    invoice_no = models.CharField(max_length=20)
    received_by = models.CharField(max_length=50)
    remark = models.TextField()

    def __str__(self):
        return self.material
        


class RequisitionItem(models.Model):
    item = models.CharField(max_length=100)
    product_code = models.CharField(max_length=100)
    make_brand = models.CharField(max_length=100)
    grade = models.CharField(max_length=20)
    pack_size = models.CharField(max_length=100)
    quantity = models.CharField(max_length=100)
    coa_coc_required = models.BooleanField(default=False)
    discount = models.CharField(max_length=100,default='None')
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.item
    
class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=20,default='None')
    contact_number = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()

    def __str__(self):
        return self.name
    
class Grade(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


class PurchaseItem(models.Model):
    make_brand = models.CharField(max_length=100)
    product_code = models.CharField(max_length=50)
    item = models.CharField(max_length=100)
    quotation_no = models.CharField(max_length=100)
    grade = models.CharField(max_length=50)
    pack_size = models.CharField(max_length=50)
    quantity = models.CharField(max_length=100)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=20, decimal_places=2)
    coa_coc_required = models.BooleanField(default=False)
    pdf_file = models.FileField(upload_to='pdf_files/',blank=True, null=True)
    discount = models.CharField(max_length=10,default='None')
    status = models.CharField(max_length=50)
    
    def __str__(self):
        return self.item
    

class PurchaseOrder(models.Model):
    po_no = models.CharField(max_length=100)
    supplier_nameaddress = models.CharField(max_length=100)
    quotation_no = models.CharField(max_length=100)
    date_of_q = models.DateField()
    total_amount = models.DecimalField(max_digits=20, decimal_places=2)
    
    def __str__(self):
        return self.po_no 
    
class Stock(models.Model):
    
    material = models.CharField(max_length=100)
    makes = models.CharField(max_length=100, default='Default value')
    model_no = models.CharField(max_length=100, default='Default Model No.')  
    description = models.TextField()
    grade = models.CharField(max_length=20)
    quantity = models.PositiveIntegerField()
    hsn_sac = models.CharField(max_length=20, default='None')
    remark = models.TextField()

    def __str__(self):
        return self.material
    