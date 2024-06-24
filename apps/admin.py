from django.contrib import admin
from .models import Vendor,Grade,IncomingMaterial,RequisitionItem,PurchaseItem,PurchaseOrder,Stock


admin.site.register(Vendor)
admin.site.register(Grade)
admin.site.register(IncomingMaterial)
admin.site.register(RequisitionItem)
admin.site.register(PurchaseItem)
admin.site.register(PurchaseOrder)
admin.site.register(Stock)
