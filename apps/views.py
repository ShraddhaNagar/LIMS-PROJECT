from django.views.decorators.cache import cache_control, never_cache
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from limps import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth import authenticate, login, logout
from . tokens import generate_token

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas

from . form import IncomingMaterialForm,RequisitionItemForm,VendorForm,GradeForm,PurchaseOrderForm,PurchaseForm
from . models import IncomingMaterial,RequisitionItem,Vendor,Grade,PurchaseOrder,PurchaseItem,Stock

# from django.contrib.auth.tokens import default_token_generator
# from django.contrib.auth import get_user_model
# User = get_user_model()



def home(request):
    return render(request, 'apps/index.html')

def profile(request):
    user = request.user
    uname = user.username
    email = user.email
    date_of_join = user.date_joined.strftime('%Y-%m-%d')  # Example format
    return render(request, 'profile/profile.html', {'uname': uname, 'email': email, 'date_of_join': date_of_join})

def settings(request):
    if request.method == 'POST':
        current_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('cnf_password')

        # Your logic to validate and process the form data goes here
        # For example, you can check if the new password matches the confirm password
        if new_password != confirm_password:
            messages.error(request, 'New password and confirm password do not match.')
            # You can add more error handling and validation logic here
        else:
            # Save the new password or perform any other necessary actions
            messages.success(request, 'Password changed successfully.')
            # You can redirect the user to another page or render a different template here
            # Example: return redirect('home')

            # Redirect to the same page after form submission to prevent resubmission on page refresh
            return redirect('setting')

    return render(request, 'profile/setting.html')

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('pass')

        if User.objects.filter(username=username).exists():
            messages.warning(request, 'Username already exists!')
            return redirect('signup')
        
        if User.objects.filter(email=email).exists():
            messages.warning(request, 'Email is already in use!')
            return redirect('signup')
        
        if len(username)>10:
            messages.error(request,'Username should be less than 10 characters')
            return redirect('signup')
        
        if not  (8 <= len(password) <= 25):
            messages.error(request,"Password must be between 8 and 25 characters")
            return redirect("signup")
        
        if not username.isalnum():
            messages.error(request, "Username can only contain letters and numbers.")
            return redirect('signup')
        

        myuser = User.objects.create_user(username=username, email=email, password=password)
        myuser.is_active = False
        myuser.save()
        messages.success(request, "Your account has been successfully created. We have sent confirmation email on your mail to activate your account.")

        # welcome email
        subject = "Welcome to MySite!"
        message = "Hello "+ myuser.username +"\n\nThank you for joining us at MySite.Please feel free to browse around and start connecting with others."
        message = "Hello "+ myuser.username +"Please confirm your email address."
        message = "Hello "+ myuser.username +"\n\nThank you for seeing this mail !"
        from_email = settings.EMAIL_HOST_USER
        to_list=[myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        #confirmation mail link
        current_site = get_current_site(request)
        email_subject = "Confirm Your Email Address @ LIMPS - SVM Group, Inc."
        message2 = render_to_string('email_confirmation.html', {
            'name' : myuser.username,
            'uid':urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token':generate_token.make_token(myuser),
            'domain':current_site.domain
        })
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
            # reply_to=[settings.EMAIL_HOST_USER],
        )
        email.fail_silently = True
        email.send()

        return redirect('signin')
    

    return render(request, "apps/signup.html")


@never_cache
def signin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('pass')

        # Clear sensitive data from request object
        request.POST = {}

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            uname = user.username
            #Local Variable for home dashboard page for count data items
            requisition_data = RequisitionItem.objects.all().count()
            pos = PurchaseOrder.objects.all().count()
            purchase = PurchaseItem.objects.all().count()
            incomingItem = IncomingMaterial.objects.all().count()
            return render(request, "logined/home.html", {'un': uname,'req_count':requisition_data,'po_count':pos,'poIem_count':purchase,'incomingItem_count':incomingItem})
        else:
            messages.error(request, "Bad Credentials")
            return redirect('signin')

    return render(request, "apps/login.html")

@login_required(login_url='signin')
@never_cache
def homeDashboard(request):
    requisition_data = RequisitionItem.objects.all().count()
    pos = PurchaseOrder.objects.all().count()
    purchase = PurchaseItem.objects.all().count()
    incomingItem = IncomingMaterial.objects.all().count()
    return render(request, 'logined/home.html',{'req_count':requisition_data,'po_count':pos,'poIem_count':purchase,'incomingItem_count':incomingItem})

@login_required(login_url='signin')
@never_cache
def signout(request):
    logout(request)
    request.session['logged_out'] = True 
    messages.success(request, "You have logged out successfully!")
    return redirect('signin')

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None
    
    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        return redirect('signin')
    else:
        return render(request, 'activation_failed.html')
        #return HttpResponse("Thank you for your email confirmation.")
    
# Incoming Material Form Data
@login_required(login_url='signin')
@never_cache
def incoming_material_form(request):
    vendors = Vendor.objects.all()
    grades = Grade.objects.all()
    if request.method == 'POST':
        form = IncomingMaterialForm(request.POST)
        if form.is_valid():
            incoming_material_instance = form.save()  # Save incoming material data
            
            # Check if material already exists in stock table
            try:
                stock_instance = Stock.objects.get(model_no=incoming_material_instance.model_no,material=incoming_material_instance.material)
                
                # If material exists, update existing record in stock table
                stock_instance.quantity += incoming_material_instance.quantity
                stock_instance.save()
            except Stock.DoesNotExist:
                # If material doesn't exist, create a new record in stock table
                Stock.objects.create(
                    material=incoming_material_instance.material,
                    makes=incoming_material_instance.makes,
                    model_no= incoming_material_instance.model_no,
                    description=incoming_material_instance.description,
                    grade=incoming_material_instance.grade,
                    quantity=incoming_material_instance.quantity,
                    hsn_sac=incoming_material_instance.hsn_sac,
                    remark=incoming_material_instance.remark,
                    # Add other fields as needed
                )
                
            return redirect('submitted_data_list')  # Redirect to a success page
    else:
        form = IncomingMaterialForm()
        
    return render(request, 'logined/form.html', {'form': form, 'vendors': vendors, 'grades':grades})
# def incoming_material_form(request):
#     vendors = Vendor.objects.all()
#     grades = Grade.objects.all()
#     if request.method == 'POST':
#         form = IncomingMaterialForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('submitted_data_list')  # Redirect to a success page
#     else:
#         form = IncomingMaterialForm()
        
#     return render(request, 'logined/form.html', {'form': form, 'vendors': vendors, 'grades':grades})

# Stock Data
@login_required
@never_cache
def stock(request):
    stock_data = Stock.objects.all()
    return render(request, 'stock/stock_home.html', {'stock_data': stock_data})

@login_required
@never_cache
def stock_delete(request, model_no=None):
    item = Stock.objects.filter(model_no=model_no).first()
    item.delete()
    return redirect('stock')

@login_required
@never_cache
def submitted_data_list(request):
    submitted_data = IncomingMaterial.objects.all()
    return render(request, 'logined/submitted_data_list.html', {'submitted_data': submitted_data})

# requisition data 

@login_required
@never_cache
def requisition_form(request):
    grades = Grade.objects.all()
    if request.method == 'POST':
        form = RequisitionItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('requisition_data_list')  # Redirect to a success page
    else:
        form = RequisitionItemForm()
    return render(request, 'logined/req-form.html', {'form': form, 'grades':grades})

@login_required
@never_cache
def requisition_data_list(request):
    vendors = Vendor.objects.all()
    requisition_data = RequisitionItem.objects.all()
    return render(request, 'logined/requisition_list.html', {'vendors': vendors, 'requisition_data' : requisition_data})  # Create a success.html template

# Search data for incoming material

@login_required
@never_cache
def edit(request, invoice_no=None):
    vendors = Vendor.objects.all()
    grades = Grade.objects.all()
    item = IncomingMaterial.objects.filter(invoice_no=invoice_no).first()
    if not item:
        return render(request, '404.html')  # Handle the case when no item is found
    return render(request, 'logined/dashboard.html', {'item': item, 'vendors': vendors, 'grades': grades})

@login_required
@never_cache
def update(request, invoice_no=None):
    item = IncomingMaterial.objects.filter(invoice_no=invoice_no).first()
    form = IncomingMaterialForm(request.POST, instance=item)
    if form.is_valid():
            form.save()
            return redirect('submitted_data_list')
    return render(request, 'logined/dashboard.html', {'item': item})

@login_required
@never_cache
def delete(request, invoice_no=None):
    item = IncomingMaterial.objects.filter(invoice_no=invoice_no).first()
    item.delete()
    return redirect('submitted_data_list')

# requisition_data_list operations

@login_required
@never_cache
def requisition_edit(request, product_code=None):
    grades = Grade.objects.all()
    item = get_object_or_404(RequisitionItem, product_code=product_code)
    return render(request, 'logined/reqdashboard.html', {'item': item, 'grades': grades})

@login_required
@never_cache
def requisition_list_update(request, product_code=None):
    item = get_object_or_404(RequisitionItem, product_code=product_code)
    form = RequisitionItemForm(request.POST or None, instance=item)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('requisition_data_list')
    
    return render(request, 'logined/reqdashboard.html', {'form': form})

# vendore list view

@login_required
@never_cache
def vendor_list(request):
    vendors = Vendor.objects.all()
    return render(request, 'vendore/vendor_list.html', {'vendors': vendors})

@login_required
@never_cache
def add_vendor(request):
    if request.method == 'POST':
        form = VendorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vendor_list')
    else:
        form = VendorForm()
    return render(request, 'vendore/add_vendor.html', {'form': form})

@login_required
@never_cache
def vendor_delete(request, id=None):
    item = Vendor.objects.filter(id=id).first()
    item.delete()
    return redirect('vendor_list')

# grade list

@login_required
@never_cache
def add_grade(request):
    grades = Grade.objects.all()
    
    if request.method == 'POST':
        form = GradeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('grade_list')  # Redirect to the same page after adding a grade
    else:
        form = GradeForm()
    
    return render(request, 'grade/add_grade.html', {'form': form, 'grades': grades})

@login_required
@never_cache
def grade_delete(request, id=None):
    item = Grade.objects.filter(id=id).first()
    item.delete()
    return redirect('grade_list')

@login_required
@never_cache
def grade_list(request):
    grades = Grade.objects.all()
    return render(request, 'grade/grade_list.html', {'grades': grades})

# Purchase
@login_required
@never_cache
def purchase_form(request):
    purchases = PurchaseItem.objects.all()
    grades = Grade.objects.all()
    vendors = Vendor.objects.all()
    
    if request.method == 'POST':
        form = PurchaseForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('purchase_list')  
    else:
        form = PurchaseForm()
    
    return render(request, 'purchase/purchase_form.html', {'form': form, 'purchases': purchases,'grades': grades, 'vendors': vendors})

@login_required
@never_cache
def purchase_list(request):
    pos = PurchaseOrder.objects.all()
    purchases = PurchaseItem.objects.all()
    return render(request, 'purchase/purchase_list.html', {'pos': pos, 'purchases': purchases})

# Purchase List Operations
@login_required
@never_cache
def purchase_edit(request, product_code=None):
    item = PurchaseItem.objects.filter(product_code=product_code).first()
    if not item:
        return render(request, '404.html')  # Handle the case when no item is found
    return render(request, 'purchase/purchase_update.html', {'item': item})

@login_required
@never_cache
def purchase_update(request, product_code=None):
    item = PurchaseItem.objects.filter(product_code=product_code).first()
    form = PurchaseForm(request.POST, instance=item)
    if form.is_valid():
            form.save()
            return redirect('purchase_list')
    return render(request, 'purchase/purchase_update.html', {'item': item, 'form': form})

# Purchase Order Form
@login_required
@never_cache
def po_add(request):
    vendors = Vendor.objects.all() 
    pos = PurchaseOrder.objects.all()  
    if request.method == 'POST':
        form = PurchaseOrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('po_details')  
    else:
        form = PurchaseOrderForm()
    return render(request, 'purchase/po_add.html', {'form': form, 'vendors': vendors, 'pos': pos})
@login_required
@never_cache
def po_details(request):
    pos = PurchaseOrder.objects.all()
    vendors = Vendor.objects.all()
    return render(request, 'purchase/po_details.html', {'pos': pos, 'vendors': vendors})

# Purchase Order Form Operations
@login_required
@never_cache
def po_edit(request, quotation_no=None):
    vendors = Vendor.objects.all()
    pos = PurchaseOrder.objects.filter(quotation_no=quotation_no).first()
    if not pos:
        return render(request, '404.html')  # Handle the case when no item is found
    return render(request, 'purchase/po_update.html', {'pos': pos, 'vendors': vendors})

@login_required
@never_cache
def po_update(request, quotation_no=None):
    pos = PurchaseOrder.objects.filter(quotation_no=quotation_no).first()
    form = PurchaseOrderForm(request.POST, instance=pos)
    if form.is_valid():
            form.save()
            return redirect('po_details')
    return render(request, 'purchase/po_update.html', {'pos': pos, 'form': form})

@login_required
@never_cache
def show_detail(request, quotation_no=None):
    purchases = PurchaseItem.objects.filter(quotation_no=quotation_no)
    return render(request, 'purchase/purchase_list.html', {'purchases': purchases})

@login_required
@never_cache
def product_details(request):
    # Fetch data from the models
    purchases = PurchaseItem.objects.all()
    return render(request, 'purchase/product_details.html', {'purchases': purchases})



# for print pdf for requisition list
@login_required
@never_cache
def generate_pdf(request):
    selected_product_codes = request.POST.get('selected_rows').split(',')
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="selected_rows.pdf"'

    # Prepare data for each selected row
    all_selected_rows_data = []
    for product_code in selected_product_codes:
        requisition = RequisitionItem.objects.get(product_code=product_code)
        row_data = [
            requisition.item,
            requisition.product_code,
            requisition.make_brand,
            requisition.grade,
            requisition.pack_size,
            requisition.quantity,
            requisition.coa_coc_required,
            requisition.discount,
            requisition.status
        ]
        all_selected_rows_data.append(row_data)

    # Generate PDF
    pdf = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    # Add a table for each row of data
    for row_data in all_selected_rows_data:
        table = Table([row_data])
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])
        table.setStyle(style)
        elements.append(table)

    pdf.build(elements)

    return response
