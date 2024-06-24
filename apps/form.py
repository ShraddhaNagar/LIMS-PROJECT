# forms.py
from django import forms
from .models import IncomingMaterial, RequisitionItem,Vendor,Grade, PurchaseOrder,PurchaseItem,Stock

class IncomingMaterialForm(forms.ModelForm):
    class Meta:
        model = IncomingMaterial
        fields = '__all__'

class RequisitionItemForm(forms.ModelForm):
    class Meta:
        model = RequisitionItem
        fields = '__all__'  # or specify fields explicitly ['item', 'product_code', ...]

class VendorForm(forms.ModelForm): 
    class Meta:
        model = Vendor
        fields = '__all__'

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = '__all__'

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = PurchaseItem
        fields = '__all__'

class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'
