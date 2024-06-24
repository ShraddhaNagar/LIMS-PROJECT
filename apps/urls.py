from django.contrib import admin
from django.urls import path, include
from django.views.static import serve
from django.conf import settings

from . import views

urlpatterns = [
    # Media and static files for production mode
    path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
    path('static/<path:path>', serve, {'document_root': settings.STATIC_ROOT}),


    path('dashboard/', views.homeDashboard, name='home_dashboard'),  # Home page of the dashboard (logged in users)

    # Profile and Settings
    path('admin-profile/',views.profile,name='profile'), 
    path('admin-setting/',views.settings,name='setting'), 

    # App-specific URLs
    path('', views.home, name="home"),
    path('signup/', views.signup, name="signup"),
    path('signin/', views.signin, name="signin"),
    path('signout/', views.signout, name="signout"),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('incoming-material-form/', views.incoming_material_form, name='incoming_material_form'),
    path('requisition-form/', views.requisition_form, name='requisition_form'),
    path('submitted-data-list/', views.submitted_data_list, name='submitted_data_list'),
    path('requisition-list/', views.requisition_data_list, name='requisition_data_list'),

    #stock data
    path("stock-data",views.stock,name="stock"),
    path('stock-delete/<str:model_no>/', views.stock_delete, name='stockdelete'),
    
    # Operations for incoming material
    path('edit/<str:invoice_no>/', views.edit, name='edit'),
    path('update/<str:invoice_no>/', views.update, name='update'),
    path('delete/<str:invoice_no>/', views.delete, name='delete'),

    # Operations for requisition data list
    path('requisition-update/<str:product_code>/', views.requisition_list_update, name='requisition_list_update'),
    path('requisition-edit/<str:product_code>/', views.requisition_edit, name='requisition_edit'),
    path('generate-pdf/', views.generate_pdf, name='generate_pdf'),

    # Vendor data
    path('vendors/', views.vendor_list, name='vendor_list'),
    path('add-vendors/', views.add_vendor, name='add_vendor'),
    path('delete-vendors/<int:id>/', views.vendor_delete, name='vendor_delete'),

    # Grade data
    path('add-grades/', views.add_grade, name='add_grade'),
    path('delete-grade/<int:id>/', views.grade_delete, name='grade_delete'),
    path('grades/', views.grade_list, name='grade_list'),

    # Purchase list
    path('purchase-form/', views.purchase_form, name='purchase_form'),
    path('purchase-list/', views.purchase_list, name='purchase_list'),

    # Operations for purchase list form
    path('purchase-edit/<str:product_code>/', views.purchase_edit, name='purchase_edit'),
    path('purchase-update/<str:product_code>/', views.purchase_update, name='purchase_update'),

    path('po-details/', views.po_details, name='po_details'),
    path('po-add/', views.po_add, name='po_add'),
    path('product-details/', views.product_details, name='product_details'),
    path('purchase-order-detail/<str:quotation_no>/', views.show_detail, name='show_detail'),
    
    # Operations for purchase order form
    path('po-edit/<str:quotation_no>/', views.po_edit, name='po_edit'),
    path('po-update/<str:quotation_no>/', views.po_update, name='po_update'),
]
