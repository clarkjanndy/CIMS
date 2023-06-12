from django.http import HttpResponse,HttpResponseRedirect, JsonResponse,response,FileResponse
from django.template import loader
from django.urls import reverse
from .models import Editors,Users,Admin,Comments,Inventory,Posts,Order,PostImage,ProfilePics,Messages,CheckUpRecords,Search,RegCode, Notifications, Category
from .forms import RegCodeForm,SearchForm,MessageForm,ProfilePicForm,CommentForm,OrderForm, AdminRegForm, LoginForm, UsersForm,InventoryForm,PostForm,EditUsersForm,FacultyForm,AddStockForm,CheckupForm, UsersV2Form
import datetime
from django.contrib import messages
from sms import  Message
ID=None
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView
import io
from reportlab.pdfgen import canvas
import matplotlib.pyplot as plt
from django.db.models import Count
from .utils.pdf_generator import pdf_generator
from pathlib import Path
import base64
from django.shortcuts import render
from io import BytesIO
from matplotlib.lines import Line2D
from django.db.models import Sum
from django.db.models.functions import ExtractMonth, ExtractYear
from collections import defaultdict
from django.contrib import messages
# generating pdf file
def pdftest(request):
    d=Search.objects.all().filter(id=1)
    for c in d:
        s=c.search
    rec=Users.objects.all().filter(id=s)
    
    for r in rec:
        fname=r.firstname
        lname=r.lastname
        mname=r.middlename
        age=r.age
        address=r.address
        bithday=r.birthday
        department=r.department
        gender=r.gender
        yearlevel=r.year_level


    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)
    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawCentredString(200,800,'CIMS')
    p.drawString(50, 700, 'First Name:')
    p.drawString(50, 685, 'Middle Name:')
    p.drawString(50, 670, 'Last Name:')
    p.drawString(50, 655, 'Age:')
    p.drawString(50, 640, 'Birth Day:')
    p.drawString(50, 625, 'Address:')
    p.drawString(50, 610, 'Department:')
    p.drawString(50, 595, 'Gender:')
    p.drawString(50, 580, 'Year Level:')
    p.drawString(150, 700, fname)
    p.drawString(150, 685, mname)
    p.drawString(150, 670, lname)
    p.drawString(150, 655, age)
    # p.drawString(150, 740, bithday)
    p.drawString(150, 625, address)
    p.drawString(150, 610, department)
    p.drawString(150, 595, gender)
    p.drawString(150, 580, yearlevel)

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='hello.pdf')

def index(request):
    template=loader.get_template('layout.html') 
    return HttpResponse(template.render({'date':current_date},request))

def qualified_rotc(request):
    if request.session.get('email',default="")=="":
        return HttpResponseRedirect(reverse('user_login'))
    else:
        prof_pic=Admin.objects.filter(email=request.session.get('admin_email'))
        users=Users.objects.all().filter(medical_status='Physically Fit',status="confirmed",year_level="Freshmen")
        template=loader.get_template('admin_users_list.html') 
        data={'profile_pic':prof_pic,'users':users,'count':new_apply_count,'date':current_date,'table_title':'Students Qualified For ROTC'}
        return HttpResponse(template.render(data,request))
    
def qualified_rotc_list(request):
    list_of_users_only='false'
    prof_pic=Admin.objects.filter(email=request.session.get('admin_email'))
    users=Users.objects.all().filter(
        status="confirmed",
        user_type="Student", 
        is_active = True, 
        year_level='Freshmen',
        medical_status = 'Physically Fit'
    )    
    template=loader.get_template('admin_users_list.html') 
    data={'list_of_users_only':list_of_users_only, 'profile_pic':prof_pic,'users':users,'count':new_apply_count,'date':current_date,'table_title':'List of ROTC Qualified Students'}
    return HttpResponse(template.render(data,request))
    
def qualified_cwts(request):
    if request.session.get('email',default="")=="":
        return HttpResponseRedirect(reverse('user_login'))
    else:
        prof_pic=Admin.objects.filter(email=request.session.get('admin_email'))
        users=Users.objects.all().filter(medical_status='With Medical Condition',status="confirmed",year_level="Freshmen")
        template=loader.get_template('admin_users_list.html') 
        data={'profile_pic':prof_pic,'users':users,'count':new_apply_count,'date':current_date,'table_title':'Students Qualified For CWTS'}
        return HttpResponse(template.render(data,request))

def with_condition(request):
    if request.session.get('admin_email',default="")=="":
        return HttpResponseRedirect(reverse('admin_login'))
    else:
        bylevel=UsersForm()
        list_of_users_only='true'
        prof_pic=Admin.objects.filter(email=request.session.get('admin_email'))
        users=Users.objects.all().filter(medical_status='With Medical Condition',status="confirmed")
        template=loader.get_template('admin_users_list.html')
        
        selected_year_level = ''
        if 'year_level' in request.GET:
                users = users.filter(year_level = request.GET['year_level'])
                selected_year_level = request.GET['year_level']
         
        data={'list_of_users_only':list_of_users_only,'selected_year_level':selected_year_level,'profile_pic':prof_pic,'users':users,'count':new_apply_count,'date':current_date,'table_title':'Users with Medical Conditions','show':'Users Medical Condition'}
        return HttpResponse(template.render(data,request))

def physicaly_fit(request):
    if request.session.get('admin_email',default="")=="":
        return HttpResponseRedirect(reverse('admin_login'))
    else:
        bylevel=UsersForm()
        list_of_users_only='true'
        prof_pic=Admin.objects.filter(email=request.session.get('admin_email'))
        users=Users.objects.all().filter(medical_status='Physically Fit',status="confirmed")
        template=loader.get_template('admin_users_list.html') 
        
        selected_year_level = ''
        if 'year_level' in request.GET:
                users = users.filter(year_level = request.GET['year_level'])
                selected_year_level = request.GET['year_level']
            
        data={'list_of_users_only':list_of_users_only,'selected_year_level':selected_year_level,'profile_pic':prof_pic,'users':users,'count':new_apply_count,'date':current_date,'table_title':'Physically Fit Users','show':'With Medical Condition'}
        return HttpResponse(template.render(data,request))

def admin_users_list(request):
    bylevel=UsersForm()
    list_of_users_only='true'
    prof_pic=Admin.objects.filter(email=request.session.get('admin_email'))
    users=Users.objects.all().filter(status="confirmed",user_type="Student", is_active = True)
    template=loader.get_template('admin_users_list.html') 
    
    selected_year_level = ''
    if 'year_level' in request.GET:
            users = users.filter(year_level = request.GET['year_level'])
            selected_year_level = request.GET['year_level']
            
    data={'list_of_users_only':list_of_users_only,'selected_year_level':selected_year_level,'profile_pic':prof_pic,'users':users,'count':new_apply_count,'date':current_date,'table_title':'List of all Students'}
    return HttpResponse(template.render(data,request))
     
def view_by_level(request):
    bylevel=UsersForm()
    list_of_users_only='true'
    prof_pic=Admin.objects.filter(email=request.session.get('admin_email'))
    # if con == 'users_list':
    users=Users.objects.all().filter(status="confirmed",user_type="Student",year_level=request.GET['year_level'], is_active = True)
    # else:
        # users=Users.objects.all().filter(medical_status='With Medical Condition',status="confirmed",year_level=request.GET['year_level'])
    template=loader.get_template('admin_users_list.html') 
    data={'list_of_users_only':list_of_users_only,'bylevel':bylevel,'profile_pic':prof_pic,'users':users,'count':new_apply_count,'date':current_date,'table_title':'List of all Students'}
    return HttpResponse(template.render(data,request));



def faculty_list(request):
    if request.session.get('admin_email',default="")=="":
        return HttpResponseRedirect(reverse('admin_login'))
    else:
        list_of_users_only='false'
        prof_pic=Admin.objects.filter(email=request.session.get('admin_email'))
        users=Users.objects.all().filter(status="confirmed",list_filter="administrators")
        template=loader.get_template('admin_users_list.html') 
        if users:
            empty_rec="not empty"
        else:
            empty_rec=""
        data={'list_of_users_only':list_of_users_only,'profile_pic':prof_pic,'empty_rec':empty_rec,'users':users,'count':new_apply_count,'date':current_date,'table_title':'List of all Administrators', "list":"admin"}
        return HttpResponse(template.render(data,request))

def admin_for_confirmation(request):
    if request.session.get('admin_email',default="")=="":
        return HttpResponseRedirect(reverse('admin_login'))
    else:
        prof_pic=Admin.objects.filter(email=request.session.get('admin_email'))
        users=Users.objects.all().filter(status='')
        template=loader.get_template('admin_for_confirmation.html') 
        if users:
            empty_rec="not empty"
        else:
            empty_rec=""
        return HttpResponse(template.render({'profile_pic':prof_pic,'empty_rec':empty_rec,'count':new_apply_count,'users':users,'date':current_date},request))


def delete_user(request,pk):
    if request.session.get('admin_email',default="")=="":
        return HttpResponseRedirect(reverse('admin_login'))
    else:
        Users.objects.filter(id=pk).delete()
        return HttpResponseRedirect(reverse('admin_for_confirmation'))

def edit_user(request,pk):
    user=Users.objects.filter(id=pk)
    if request.session.get('email') == None:
        for x in user:
            k=x.medical_status
            l=x.medical_condition

        form = EditUsersForm(initial=
        {'medical_status':k,
        'medical_condition':l})
        template=loader.get_template('admin_edit_user.html')
        return HttpResponse(template.render({'form':form,'user':user,'date':current_date,'count':new_apply_count},request))
    else:
        for x in user:
            a=x.id
            b=x.firstname
            c=x.middlename
            d=x.lastname
            e=x.birthday
            f=x.age
            g=x.address
            h=x.gender
            i=x.department
            j=x.email
            k=x.medical_status
            l=x.medical_condition

        form = EditUsersForm(initial=
        {'id':a,
        'firstname':b,
        'middlename':c,
        'lastname':d,
        'birthday':e,
        'age':f,
        'address':g,
        'gender':h,
        'department':i,
        'email':j,
        'medical_status':k,
        'medical_condition':l})
        template=loader.get_template('admin_edit_user.html')
        return HttpResponse(template.render({'form':form,'user':user,'date':current_date,'count':new_apply_count},request))

def save_edit_user(request,pk):
    Users.objects.filter(id=pk).update(firstname=request.POST['firstname'],middlename=request.POST['middlename'],lastname=request.POST['lastname'],birthday=request.POST['birthday'],age=request.POST['age'],address=request.POST['address'],gender=request.POST['gender'],department=request.POST['department'],email=request.POST['email'],medical_status=request.POST['medical_status'])
    return HttpResponseRedirect(reverse('admin_users_list'))

def confirm_user(request,pk):
    # user = Users(status="confirmed")
    # user.save()
    if request.session.get('admin_email',default="")=="":
        return HttpResponseRedirect(reverse('admin_login'))
    else:
       # message=Message("You can login now to our CIMS website thank you",'09463897070',['09517134123'])
       # message.send()
        Users.objects.filter(id=pk).update(status="confirmed")
        return HttpResponseRedirect(reverse('admin_for_confirmation'))

def check_user(request,id):
    the_user=""
    who=Users.objects.all().filter(email=request.session.get('email'))
    template=loader.get_template('admin_check_user.html')
    user=Users.objects.filter(id=id)
    for f in who:
        the_user=f.user_type
    return HttpResponse(template.render({'usertype':the_user,'user':user,'date':current_date,'count':new_apply_count},request))
        
def admin_home_page(request):
    username=request.session.get('admin_email',default="")
    template=loader.get_template('admin_home_page.html')
    if username=='':
        return HttpResponseRedirect(reverse('admin_login'))
    else:
        online=Users.objects.all().filter(is_online='true')
        form=PostForm()
        posts=Posts.objects.all().order_by('-id')
        prof_pic=Admin.objects.filter(email=request.session.get('admin_email'))
        admin_post_pic=Admin.objects.all()
        user_post_pic=ProfilePics.objects.all()
        postImage=PostImage.objects.all()        
        data={'online':online,'admin_post_pic':admin_post_pic,'user_post_pic':user_post_pic,'postImage':postImage,'profile_pic':prof_pic,'name':username,'count':new_apply_count,'date':current_date,'form':form,'posts':posts}
        return HttpResponse(template.render(data,request))

def submit_post(request):
    form=PostForm(request.POST,request.FILES)
    if form.is_valid():
        form.save()
        q=Admin.objects.all().filter(email=request.session.get('admin_email'))
        z=Users.objects.all().filter(email=request.session.get('email'))
        postid=Posts.objects.all().filter(content=form.cleaned_data['content'])
        images=request.FILES.getlist('post_images')
        for image in images:
            for b in postid:
                PostImage.objects.create(post_pic=image,post_id=b.id)
        if q:
            for m in q:
                Posts.objects.all().filter(content=form.cleaned_data['content']).update(posted_by=m.email)
            return HttpResponseRedirect(reverse('announcements'))
        else:
            for  p in z:
                Posts.objects.all().filter(content=form.cleaned_data['content']).update(posted_by=p.email)
            return HttpResponseRedirect(reverse('user_home_page'))
            

def register(request):
    form = UsersForm()
    template= loader.get_template('user_reg.html')
    return HttpResponse(template.render({'form':form,'date':current_date,'usertype':'student','reg_title':'User Registration Form','url':'addRecord/'},request)) 

def faculty_reg(request):
    form = UsersV2Form()
    template = loader.get_template('faculty_user_reg.html')
    return HttpResponse(template.render({'form':form,'date':current_date,'usertype':'faculty','reg_title':'Faculty Registration Form','url':'faculty_addRecord/'},request)) 

def nstp_reg(request):
    form = UsersV2Form()
    template = loader.get_template('nstp_user_reg.html')
    return HttpResponse(template.render({'form':form,'date':current_date,'usertype':'nstp','reg_title':'NSTP Coordinator Registration Form','url':'nstp_addRecord/'},request)) 

def staff_reg(request):
    form = UsersV2Form()
    template = loader.get_template('user_reg.html')
    return HttpResponse(template.render({'form':form,'date':current_date,'usertype':'staff','reg_title':'Staff Registration Form','url':'staff_addRecord/'},request)) 

def admin_register(request):
    form=AdminRegForm()
    template= loader.get_template('admin_reg.html')
    return HttpResponse(template.render({'form':form,'date':current_date},request))

def user_login(request):
    email=request.session.get('email',default="")
    template=loader.get_template('user_login.html')
    if email=="":
        form=LoginForm()
        return HttpResponse(template.render({'form':form,'date':current_date},request))
    else:
         return HttpResponseRedirect(reverse('user_home_page'))

def usersubmitlogin(request):
    check_if_exist=Users.objects.all().filter(email=request.POST['email'], is_active = True)
    for x in check_if_exist:
        if x.email==request.POST['email'] and x.password==request.POST['password']:
            check_if_exist.update(is_online='true')
            request.session['email']=check_if_exist[0].email
            return HttpResponseRedirect(reverse('user_home_page'))
            # if x.status=="confirmed":
            #     check_if_exist.update(is_online='true')
            #     request.session['email']=check_if_exist[0].email
            #     return HttpResponseRedirect(reverse('user_home_page'))
            # else:
            #     messages.error(request,'Your account was being processed for admin confirmation')
            #     return HttpResponseRedirect(reverse('user_login'))
        else:
            messages.error(request,'Incorrect Email or Password')
            return HttpResponseRedirect(reverse('user_login'))
    messages.error(request,'Incorrect Email or Password')
    return HttpResponseRedirect(reverse('user_login'))

def admin_login(request):
    username=request.session.get('admin_email',default="")
    template=loader.get_template('admin_login.html')
    if username=="":
        form=LoginForm()
        return HttpResponse(template.render({'form':form,'date':current_date},request))
    else:
         return HttpResponseRedirect(reverse('admin_home_page'))

def adminsubmitlogin(request):
    m=Admin.objects.all().filter(email=request.POST['email'],password=request.POST['password'])
    if m:
        request.session['admin_email']=m[0].email
        return HttpResponseRedirect(reverse('admin_home_page'))   
    else:
        messages.error(request,'Incorrect Email or Password')
        return HttpResponseRedirect(reverse('admin_login'))

def admin_logout(request):
    del request.session['admin_email']
    return HttpResponseRedirect(reverse('admin_login'))

def user_logout(request):
    ol=Users.objects.all().filter(email=request.session.get('email'))
    ol.update(is_online="false")
    del request.session['email']
    return HttpResponseRedirect(reverse('user_login'))

def addRecord(request):
    form = UsersForm(request.POST, request.FILES)   
    if form.is_valid():
        check_email=Users.objects.all().filter(email=request.POST['email'])
        if check_email:
            messages.error(request,'!!!Email address already taken')
            return HttpResponseRedirect(reverse('register'))
        else:
            form.save()
            Users.objects.filter(email=request.POST['email']).update(user_type="Student")
            return HttpResponseRedirect(reverse('user_login'))
    else:
        return HttpResponseRedirect(reverse('register')) 

def faculty_addRecord(request):
    # regcode=RegCode.objects.all().filter(id=1)
    # for r in regcode:
    #     code=r.faculty
    form = FacultyForm(request.POST,request.FILES) 
    # if request.POST['code'] == code:
    if form.is_valid() and request.POST['code'] == 'BCC-FACULTY':
        check_email=Users.objects.all().filter(email=request.POST['email'])
        if check_email:
            messages.error(request,'!!!Email address already taken')
            return HttpResponseRedirect(reverse('faculty_reg'))
        else:
            form.save()
            Users.objects.filter(email=request.POST['email']).update(user_type="faculty",status="confirmed",list_filter="administrators")
            return HttpResponseRedirect(reverse('user_login'))
    else:
        return HttpResponseRedirect(reverse('faculty_reg')) 
    # else:
    #     messages.error(request,"!!!Error Faculty Code, you're not member of the faculty ")
    #     return HttpResponseRedirect(reverse('faculty_reg'))  

def nstp_addRecord(request):
    # regcode=RegCode.objects.all().filter(id=1)
    # for r in regcode:
    #     code=r.faculty
    form = FacultyForm(request.POST,request.FILES) 
    # if request.POST['code']== code:
    if form.is_valid() and request.POST['code'] == 'BCC-NSTP':
        check_email=Users.objects.all().filter(email=request.POST['email'])
        if check_email:
            messages.error(request,'!!!Email address already taken')
            return HttpResponseRedirect(reverse('nstp_reg'))
        else:
            form.save()
            Users.objects.filter(email=request.POST['email']).update(user_type="nstp",status="confirmed",list_filter="administrators")
            return HttpResponseRedirect(reverse('user_login'))
    else:
        return HttpResponseRedirect(reverse('nstp_reg')) 
    # else:
    #     messages.error(request,"!!!Error Code, you're not an NSTP Coordinator ")
    #     return HttpResponseRedirect(reverse('nstp_reg'))

def staff_addRecord(request):
    # regcode=RegCode.objects.all().filter(id=1)
    # for r in regcode:
    #     code=r.staff
    form = FacultyForm(request.POST,request.FILES) 
    # if request.POST['code']== code:
    if form.is_valid() and request.POST['code'] == 'BCC-STAFF':
        check_email=Users.objects.all().filter(email=request.POST['email'])
        if check_email:
            messages.error(request,'!!!Email address already taken')
            return HttpResponseRedirect(reverse('staff_reg'))
        else:
            form.save()
            Users.objects.filter(email=request.POST['email']).update(user_type="staff",status="confirmed",list_filter="administrators")
            return HttpResponseRedirect(reverse('user_login'))
    else:
        return HttpResponseRedirect(reverse('staff_reg')) 
    # else:
    #     messages.error(request,"!!!Error Code, you're not a Staff ")
    #     return HttpResponseRedirect(reverse('staff_reg'))  


    
def adminSubmitReg(request):
    form=AdminRegForm(request.POST,request.FILES)
    if form.is_valid() and request.POST['admin_code']=='qawsedrf':
        check_email=Admin.objects.all().filter(email=request.POST['email'])
        if check_email:
            messages.error(request,'!!!Email address already taken')
            return HttpResponseRedirect(reverse('admin_register'))
        else:
            form.save()
            return HttpResponseRedirect(reverse('admin_login'))
    else:
        return HttpResponseRedirect(reverse('admin_register')) 

def new_apply_count():
    users=Users.objects.all().filter(status='')
    c=0
    for x in users:
            c+=1
    if c==0:
        c=""
        return c
    else:
        return c

def current_date():
    date=datetime.date.today()
    return date

def admin_inventory(request):
    if request.session.get('admin_email', default="") == "":
        return HttpResponseRedirect(reverse('admin_login'))
    else:
        all_orders = Order.objects.filter(order_status='')
        for a in all_orders:
            b = Inventory.objects.filter(serial=a.serial)
            for c in b:
                d = a.quantity
                Order.objects.filter(serial=a.serial).update(item_name=c.item_name, unit=c.unit, total=d)

    all_items = Inventory.objects.all()
    all_orders = Order.objects.filter(order_status='')  # Filter orders with order_status = 'A'

    form = InventoryForm()

    order = OrderForm()
    template = loader.get_template('admin_inventory.html')

    notifs = Notifications.objects.filter(is_read=False).aggregate(count=Count('id')).get('count', None)
    return HttpResponse(template.render({'all_orders': all_orders, 'order': order, 'table_title': 'all types of illness', 'count': new_apply_count, 'form': form, 'date': current_date, 'items': all_items, "notifs": notifs}, request))

def list_by(request):
    form=InventoryForm()
    order=OrderForm()
    all_items=Inventory.objects.all().filter(category=request.GET['category'])
    template=loader.get_template('admin_inventory.html')
    if all_items:
        empty_rec="not empty"
    else:
        empty_rec=""
    return HttpResponse(template.render({'order':order,'table_title':request.GET['category'],'empty_rec':empty_rec,'form':form,'count':new_apply_count,'date':current_date,'items':all_items},request))

def expired(request):
    if request.session.get('admin_email',default="")=="":
        return HttpResponseRedirect(reverse('admin_login'))
    else:
        all_items=Inventory.objects.all()
        for x in all_items:
          if x.expiration.year<current_date().year:
            Inventory.objects.filter(id=x.id).update(status='expired')
        items=Inventory.objects.all().filter(status='expired')
        form=InventoryForm()
        template=loader.get_template('admin_inventory.html')
        return HttpResponse(template.render({'count':new_apply_count,'form':form,'date':current_date,'items':items},request))

def save_item(request):
    form=InventoryForm(request.POST,request.FILES)
    a=Inventory.objects.filter(serial=request.POST['serial'])

    if form.is_valid():
        form.save()
        # for x in a:
        #     b=x.remaining+int(request.POST['quantity'])
        #     Inventory.objects.filter(serial=request.POST['serial']).update(remaining=b)     
        messages.success(request, 'Item successfully added.')   
        return HttpResponseRedirect(reverse('admin_inventory'))
    else:
        if form.errors.get('serial'):
             messages.warning(request, 'Item must be unique')

        if form.errors.get('expiration'):
            messages.warning(request, 'Expiration date cannot be in the past.')
            
        return HttpResponseRedirect(reverse('admin_inventory'))

def add_stock(request,pk):
    item=Inventory.objects.filter(id=pk)
    form=AddStockForm()
    template=loader.get_template('add_stock.html')
    return HttpResponse(template.render({'form':form,'item':item},request))

def save_added_stock(request,pk):
    a=Inventory.objects.filter(id=pk)
    for x in a:
        b=x.remaining+int(request.POST['quantity'])
    a.update(quantity=b,remaining=b)
    return add_stock(request,pk)

def delete_stock(request,pk):
    Inventory.objects.all().filter(id=pk).delete()
    return HttpResponseRedirect(reverse('admin_inventory'))

def add_order(request):
    order_form = OrderForm(request.POST)
    if order_form.is_valid():
        check_order = Order.objects.filter(serial=request.POST['serial'])
        if check_order:
            check_item = Inventory.objects.filter(serial=request.POST['serial'])
            if check_item:
                for item in check_item:
                    if int(request.POST['quantity']) > item.remaining:
                        messages.error(request, 'You ordered ' + request.POST['quantity'] + '. Not enough stock... ' + str(item.remaining) + ' remaining ' + item.item_name)
                    else:
                        order = order_form.save(commit=False)
                        order.student_name = request.POST['student_name']
                        order.save()
            else:
                messages.error(request, 'Wrong item number. Medicine is not in the inventory')
        else:
            check_item = Inventory.objects.filter(serial=request.POST['serial'])
            if check_item:
                for item in check_item:
                    if int(request.POST['quantity']) > item.remaining:
                        messages.error(request, 'You ordered ' + request.POST['quantity'] + '. Not enough stock... ' + str(item.remaining) + ' remaining ' + item.item_name)
                    else:
                        order = order_form.save(commit=False)
                        order.student_name = request.POST['student_name']
                        order.save()
            else:
                messages.error(request, 'Wrong item number. Medicine is not in the inventory')
    return HttpResponseRedirect(reverse('admin_inventory'))     
    
def check_out_order(request):
    a=Order.objects.all()
    if a:
        for b in a:
            c=Inventory.objects.all().filter(serial=b.serial)
            for d in c:
                c.update(remaining=d.remaining-b.quantity)
                # Order.objects.filter(serial=b.serial).delete()
                Order.objects.filter(serial=b.serial).update(order_status='B')  # Update the order_status column
    else:
        messages.error(request,'Medicine Table is Empty')    
    return HttpResponseRedirect(reverse('admin_inventory'))

def remove_order(request,pk):
    Order.objects.all().filter(id=pk).delete()
    return HttpResponseRedirect(reverse('admin_inventory'))

def edit_user_profile(request):
    user=Users.objects.filter(email=request.session.get('email'))
    # for x in user:
    #     a=x.id
    #     b=x.firstname
    #     c=x.middlename
    #     d=x.lastname
    #     e=x.birthday
    #     f=x.age
    #     g=x.address
    #     h=x.gender
    #     i=x.department
    #     j=x.email
    #     k=x.medical_status
    #      l=x.medical_condition
    #     prof_pic=ProfilePics.objects.all().filter(prof_pic_of=x.id)

    # form = EditUsersForm(initial=
    # {'id':a,
    # 'firstname':b,
    # 'middlename':c,
    # 'lastname':d,
    # 'birthday':e,
    # 'age':f,
    # 'address':g,
    # 'gender':h,
    # 'department':i,
    # 'email':j,
    # 'medical_status':k,
    # 'medical_condition':l})
    profilePicForm= ProfilePicForm(request.FILES)
    template=loader.get_template('user_update_profile.html')
    prof_pic=ProfilePics.objects.all().filter(prof_pic_of=request.session.get('email'))
    return HttpResponse(template.render({'prof_pic':prof_pic,'profilePicForm':profilePicForm,'user':user,'date':current_date,'count':new_apply_count},request))

def add_profile_pic(request):
    profilePicForm= ProfilePicForm(request.FILES)
    template=loader.get_template('add_profile_pic.html')
    return HttpResponse(template.render({'profilePicForm':profilePicForm,'date':current_date,},request))

def upload_prof_pic(request):
    form=ProfilePicForm(request.POST,request.FILES)
    if form.is_valid():
        q1=ProfilePics.objects.all().filter(prof_pic_of=request.session.get('email'))
        q1.delete()
        q1.create(prof_pic_of=request.session.get('email'),profile_pic=form.cleaned_data['profile_pic'])
    return HttpResponseRedirect(reverse('edit_user_profile'))

def med_inquiry(request):
    template=loader.get_template('medicine_inquiry.html')
    if request.session.get('email',default="")=="":
        return HttpResponseRedirect(reverse('user_login'))
    else:        
        prof_pic=ProfilePics.objects.all().filter(prof_pic_of=request.session.get('email'))
        all_items=Inventory.objects.all()
        return HttpResponse(template.render({'count':new_apply_count,'date':current_date,'items':all_items,'profile_pic':prof_pic},request))

def delete_post(request,pk):
    Posts.objects.all().filter(id=pk).delete()
    PostImage.objects.all().filter(id=pk).delete()
    return HttpResponseRedirect(reverse('admin_home_page'))

def user_view_post(request,pk):
    template=loader.get_template('post_view.html')
    user_sess=request.session.get('email',default="")
    if user_sess=='':
        return HttpResponseRedirect(reverse('user_login'))
    else:
        com=Comments.objects.all().filter(post_id=pk)
        form=CommentForm()
        prof_pic=Admin.objects.filter(email=request.session.get('admin_email'))
        admin_post_pic=Admin.objects.all()
        user_post_pic=ProfilePics.objects.all()
        postImage=PostImage.objects.all()      
        post=Posts.objects.all().filter(id=pk)  
        data={'com':com,'form':form,'admin_post_pic':admin_post_pic,'user_post_pic':user_post_pic,'postImage':postImage,'profile_pic':prof_pic,'name':username,'count':new_apply_count,'date':current_date,'post':post}
        return HttpResponse(template.render(data,request))

def view_post(request,pk):
    template=loader.get_template('post_view.html')
    username=request.session.get('admin_email',default="")
    
    com=Comments.objects.all().filter(post_id=pk)
    form=CommentForm()
    prof_pic=Admin.objects.filter(email=request.session.get('admin_email'))
    admin_post_pic=Admin.objects.all()
    user_post_pic=ProfilePics.objects.all()
    postImage=PostImage.objects.all()      
    post=Posts.objects.all().filter(id=pk)
    data={'com':com,'form':form,'admin_post_pic':admin_post_pic,'user_post_pic':user_post_pic,'postImage':postImage,'profile_pic':prof_pic,'name':username,'count':new_apply_count,'date':current_date,'post':post}
    return HttpResponse(template.render(data,request))

def comment(request,pk):
    form=CommentForm(request.POST)
    if form.is_valid():

        form.save()
        q=Admin.objects.all().filter(email=request.session.get('admin_email'))
        z=Users.objects.all().filter(email=request.session.get('email'))
        if q:
            for m in q:
                Comments.objects.all().filter(comment=form.cleaned_data['comment']).update(post_id=pk,commented_by=m.email)
        else:
            for p in z:
                Comments.objects.all().filter(comment=form.cleaned_data['comment']).update(post_id=pk,commented_by=p.email)
        if q:
            return HttpResponse(view_post(request,pk))
        else:
            return HttpResponse(view_post(request,pk))

def features(request):
    user=""
    template=loader.get_template('features.html')
    if request.session.get('admin_email') != None :
        prof_pic=Admin.objects.all().filter(email=request.session.get('admin_email'))
    else :
        prof_pic=ProfilePics.objects.all().filter(prof_pic_of=request.session.get('email'))
        user_type=Users.objects.all().filter(email=request.session.get('email'))
        for u in user_type:
            user=u.user_type
    if prof_pic.count() == 0:
        default_pic='true'
    else:
        default_pic='false'
    
    notifs = Notifications.objects.filter(is_read=False).aggregate(count = Count('id')).get('count', None)
    data={'default_pic':default_pic,'profile_pic':prof_pic,'count':new_apply_count,'user_type':user, "notifs": notifs}
    return HttpResponse(template.render(data,request))

def message(request):
    template=loader.get_template('message.html')
    msgform=MessageForm(request.POST)
    a=Messages.objects.all().order_by('-id')
    users=Users.objects.all()
    if request.session.get('admin_email') != None :
        prof_pic=Admin.objects.all().filter(email=request.session.get('admin_email'))
    else :
        prof_pic=ProfilePics.objects.all().filter(prof_pic_of=request.session.get('email'))
    if prof_pic.count() == 0:
        default_pic='true'
    else:
        default_pic='false'
    data={'default_pic':default_pic,'profile_pic':prof_pic,'form':msgform,'message':a,'contacts':users}
    return HttpResponse(template.render(data,request))

def send(request):
    msgform=MessageForm(request.POST)
    if msgform.is_valid():
        msgform.save()
        Messages.objects.all().filter(message=msgform.cleaned_data['message']).update(message_from=request.session.get('email'),message_to=msgform.cleaned_data['message_to'])

        return HttpResponse(message(request))

def announcements(request):
    username=request.session.get('admin_email',default="")
    template=loader.get_template('post.html')
    
    online=Users.objects.all().filter(is_online='true')
    form=PostForm()
    posts=Posts.objects.all().order_by('-id')
    prof_pic=Admin.objects.filter(email=request.session.get('admin_email'))
    admin_post_pic=Admin.objects.all()
    user_post_pic=ProfilePics.objects.all()
    postImage=PostImage.objects.all()        
    data={'online':online,'admin_post_pic':admin_post_pic,'user_post_pic':user_post_pic,'postImage':postImage,'profile_pic':prof_pic,'name':username,'count':new_apply_count,'date':current_date,'form':form,'posts':posts}
    return HttpResponse(template.render(data,request))

def visit_history(request):
    form=SearchForm(request.POST)
    template=loader.get_template('visit_history.html')
    messages.error(request,'Please search record to display...')
    history=CheckUpRecords.objects.all()
    
    actual_history = []
    for h in history:
        users = Users.objects.filter(id = h.rec_id) 
        if users.exists(): 
           if users.exists():
            h.name = f"{users.first().firstname} {users.first().middlename} {users.first().lastname}"
            h.email = users.first().email
        else:
            h.name = 'Unknown User'
            h.email = "Uknown Email"
          
            
        actual_history.append(h)
    
    return HttpResponse(template.render({'form':form,'history':actual_history},request))

def myhistory(request):
    rec=Users.objects.all().filter(email=request.session.get('email'))
    for r in rec:
            prof_pic=ProfilePics.objects.all().filter(prof_pic_of=r.email)
            history=CheckUpRecords.objects.all().filter(rec_email=r.email)
    if prof_pic.count() == 0:
        default_pic='true'
    else:
        default_pic='false'
    template=loader.get_template('visit_history_record.html')
    return HttpResponse(template.render({'rec':rec,'history':history,'profile_pic':prof_pic,'default_pic':default_pic},request))


def search_history(request):
    form = SearchForm(request.POST)
    rec = Users.objects.all().filter(student_id=request.POST['search'])
    graph_file = generate_visit_graph()
    try:
        if not rec:
            rec = Users.objects.all().filter(id=int(request.POST['search']))
    except:
        incorrectID = '!!! No record for this ID...'
    
    id = None
    
    d = Search.objects.all().filter(id=1)
    prof_pic = ProfilePics.objects.all()
    if rec.count() == 0:
        incorrectID = '!!! No record for this ID...'
        Search.objects.all().filter(id=1).update(search=request.POST['search'])
    else:
        incorrectID = ""
        if d.count() == 0:
            form.save()
        else:
            Search.objects.all().filter(id=1).update(search=request.POST['search'])
        id = rec.first().id
        prof_pic = ProfilePics.objects.all().filter(prof_pic_of=rec.first().email)
    checkupform = CheckupForm()

    if prof_pic.count() == 0:
        default_pic = 'true'
    else:
        default_pic = 'false'

    template = loader.get_template('visit_history_record.html')
    history = CheckUpRecords.objects.all().filter(rec_id=id).order_by('-id')
    context = {
        'history': history,
        'profile_pic': prof_pic,
        'default_pic': default_pic,
        'checkupform': checkupform,
        'incorrectID': incorrectID,
        'form': form,
        'rec': rec,
        'graph_file': 'data:image/png;base64,' + graph_file  # Prepend the necessary prefix to the graph file
    }
    return HttpResponse(template.render(context, request))

def generate_visit_graph():
    # Switch the backend to 'Agg'
    plt.switch_backend('Agg')

    # Retrieve the records from the CheckUpRecords model
    history = CheckUpRecords.objects.all().order_by('checkup_date')

    # Initialize variables to store the date and count of visits
    dates = []
    visit_counts = []

    # Iterate over the history records
    for record in history:
        # Get the checkup_date as a string representation
        checkup_date = record.checkup_date.strftime('%Y-%m-%d')

        # Check if the date is already in the dates list
        if checkup_date not in dates:
            # If it is not, add the date to the dates list and set the visit count to 1
            dates.append(checkup_date)
            visit_counts.append(1)
        else:
            # If it is already in the dates list, increment the visit count for that date
            index = dates.index(checkup_date)
            visit_counts[index] += 1

    # Plot the graph
    fig, ax = plt.subplots()
    ax.bar(dates, visit_counts)
    ax.set_xlabel('Date')
    ax.set_ylabel('Number of Visits')
    ax.set_title('Number of Students Visiting Clinic')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the graph plot to an in-memory buffer
    buffer = io.BytesIO()
    fig.savefig(buffer, format='png')
    buffer.seek(0)

    # Convert the buffer to a base64-encoded string
    visit_graph = base64.b64encode(buffer.getvalue()).decode('utf-8')

    # Close the plot to free up resources
    plt.close(fig)

    return visit_graph

def save_current_checkup_rec(request):
    checkupform=CheckupForm(request.POST)
    if checkupform.is_valid():
        checkupform.save()
        r=Search.objects.all().filter(id=1)
        
        for w in r:
            if isinstance(w.search, int):
                rec=Users.objects.all().filter(id=w.search)
            else:
                rec=Users.objects.all().filter(student_id=w.search)
                
            for g in rec:
                temp=g.email
                
        tbu = CheckUpRecords.objects.all().last()   
        tbu.rec_id = request.POST['id']
        tbu.email = request.POST['email']
        tbu.save()
        
        messages.error(request,'Checkup Record Saved...')
        return HttpResponse(visit_history(request))

def medical_notes(request):
    template=loader.get_template('medical_notes.html')
    history=CheckUpRecords.objects.all()
        
    actual_history = []
    for h in history:
        users = Users.objects.filter(id = h.rec_id)  
        if users.exists():
            h.firstname = users.first().firstname
            h.middlename = users.first().middlename
            h.lastname = users.first().lastname
        else:
            h.firstname = 'Unknown User'
            h.middlename = 'Unknown User'
            h.lastname = 'Unknown User'
        actual_history.append(h)
            
    return HttpResponse(template.render({'history':actual_history},request))

def user_home_page(request):
    email=request.session.get('email',default="")
    template=loader.get_template('user_home_page.html')
    if email=="":
        return HttpResponseRedirect(reverse('user_login'))
    else:
        online=Users.objects.all().filter(is_online='true')
        form=PostForm()
        posts=Posts.objects.all().order_by('-id')
        postImage=PostImage.objects.all()
        prof_pic=ProfilePics.objects.all().filter(prof_pic_of=request.session.get('email'))
        admin_post_pic=Admin.objects.all()
        user_post_pic=ProfilePics.objects.all()
        if prof_pic.count() == 0:
            default_pic='true'
        else:
            default_pic='false'
        data={'default_pic':default_pic,'online':online,'admin_post_pic':admin_post_pic,'user_post_pic':user_post_pic,'postImage':postImage,'profile_pic':prof_pic,'name':email,'date':current_date,'form':form,'posts':posts}
        return HttpResponse(template.render(data,request))

def reports(request):
    qs = Editors.objects.all()
    graph_file = generate_visit_graph()
    second_graph_data = generate_user_graph()  # Replace with your actual data for the second graph
    dispensing_graph = generate_dispensing_graph()
    purchase_graph = generate_purchase_graph()
    context = {
        'qs': qs,
        'graph_file': 'data:image/png;base64,' + str(graph_file),  # Prepend the necessary prefix to the first graph file
        'second_graph_data': 'data:image/png;base64,' + str(second_graph_data),
        'dispensing_grap': 'data:image/png;base64,' + str(dispensing_graph),
        'purchase_graph': 'data:image/png;base64,' + str(purchase_graph)
    }

    return render(request, 'reports.html', context)

def generate_purchase_graph():
    # Get the purchase data
    purchase_data = (
        Inventory.objects
        .annotate(purchase_month=ExtractMonth('purchase_date'), purchase_year=ExtractYear('purchase_date'))
        .values('purchase_month', 'purchase_year', 'category')
        .annotate(total_quantity=Sum('quantity'))
        .order_by('purchase_year', 'purchase_month', 'category')
    )
    if not purchase_data:
        return None
    
    # Extract the unique months and categories
    months = sorted(list(set((data['purchase_month'], data['purchase_year']) for data in purchase_data)))
    categories = sorted(list(set(data['category'] for data in purchase_data)))
    
    # Prepare the data for plotting
    category_quantities = {month: {category: 0 for category in categories} for month in months}
    for data in purchase_data:
        month = (data['purchase_month'], data['purchase_year'])
        category_quantities[month][data['category']] = data['total_quantity']
    
    # Plotting the graph
    x = range(len(months))  # x-axis values (0, 1, 2, ...)
    
    colors = plt.cm.tab10.colors  # Get a list of colors from the tab10 colormap
    markers = ['o', 's', 'v', '^', 'D', 'p', '*', 'h', 'x', '+']  # List of marker styles
    legend_handles = []  # Store legend handles
    
    for i, category in enumerate(categories):
        y = [category_quantities[month][category] for month in months]
        marker_style = markers[i % len(markers)]  # Use different marker styles for each category
        line = Line2D([], [], marker=marker_style, linestyle='-', linewidth=1, color=colors[i % len(colors)], label=category)
        plt.plot(x, y, marker=marker_style, linestyle='-', linewidth=1, color=colors[i % len(colors)])
        legend_handles.append(line)
    
    plt.xticks(x, [f'{month[0]} {month[1]}' for month in months], rotation=45)  # Set the x-axis labels to the formatted month strings and rotate them by 45 degrees
    plt.xlabel('Purchase Month')
    plt.ylabel('Total Quantity of Medicines Purchased')
    plt.title('Medicine Purchase Graph')
    plt.legend(handles=legend_handles)  # Show the legend
    
    # Add the total category quantity for each month at the top of the bar
    for i, month in enumerate(months):
        total_quantity = sum(category_quantities[month].values())
        plt.text(i, total_quantity + 1, f'Total: {total_quantity}', ha='center')
    
    # Saving the graph to a BytesIO object
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    
    # Encoding the image to base64
    graph_file = base64.b64encode(buffer.getvalue()).decode()
    
    plt.close()  # Close the plot to free up memory
    
    return graph_file

def generate_dispensing_graph():
    # Get the dispensing count and dates for each category
    dispensing_data = Order.objects.filter(order_status='B', serial__in=Inventory.objects.values_list('serial', flat=True)).values('order_date', 'serial').annotate(count=Count('id')).order_by('order_date', 'serial')
    if not dispensing_data:
        return None
    
    # Extract the unique dates and categories
    dates = sorted(list(set(data['order_date'].date() for data in dispensing_data if data['order_date'] is not None)))  # Exclude None values
    categories = sorted(list(set(Inventory.objects.filter(serial__in=[data['serial'] for data in dispensing_data]).values_list('category', flat=True))))
    
    # Prepare the data for plotting
    category_counts = {date: {category: 0 for category in categories} for date in dates}
    for data in dispensing_data:
        if data['order_date'] is not None:
            item_category = Inventory.objects.filter(serial=data['serial']).values_list('category', flat=True).first()
            if item_category is not None:
                category_counts[data['order_date'].date()][item_category] += data['count']
    
    # Plotting the graph
    x = range(len(dates))  # x-axis values (0, 1, 2, ...)
    
    colors = plt.cm.tab10.colors  # Get a list of colors from the tab10 colormap
    markers = ['o', 's', 'v', '^', 'D', 'p', '*', 'h', 'x', '+']  # List of marker styles
    legend_handles = []  # Store legend handles
    
    for i, category in enumerate(categories):
        y = [category_counts[date][category] for date in dates]
        marker_style = markers[i % len(markers)]  # Use different marker styles for each category
        line = Line2D([], [], marker=marker_style, linestyle='-', linewidth=1, color=colors[i % len(colors)], label=category)
        plt.plot(x, y, marker=marker_style, linestyle='-', linewidth=1, color=colors[i % len(colors)])
        legend_handles.append(line)
    
    plt.xticks(x, dates, rotation=45)  # Set the x-axis labels to the dates and rotate them by 45 degrees
    plt.xlabel('Date')
    plt.ylabel('Number of Cases')
    plt.title('Illness Report')
    plt.legend(handles=legend_handles)  # Show the legend
    
    # Add the total category count for each date at the bottom of the graph
    for i, date in enumerate(dates):
        total_count = sum(category_counts[date].values())
        plt.text(i, -10, f'Total: {total_count}', ha='center')
    
    # Saving the graph to a BytesIO object
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    
    # Encoding the image to base64
    graph_file = base64.b64encode(buffer.getvalue()).decode()
    
    plt.close()  # Close the plot to free up memory
    
    return graph_file

def generate_user_graph():
    # Get the user count for each user type and date
    user_data = Users.objects.values('date_added', 'user_type').annotate(count=Count('student_id')).order_by('date_added', 'user_type')
    if not user_data:
        return None
    
    # Prepare the data for plotting
    user_counts = {}
    user_types = set()
    
    for data in user_data:
        date = data['date_added'].strftime('%Y-%m-%d')
        user_type = data['user_type']
        count = data['count']
        
        if date not in user_counts:
            user_counts[date] = {}
        
        user_counts[date][user_type] = count
        user_types.add(user_type)
    
    # Sort the dates in ascending order
    dates = sorted(user_counts.keys())
    
    # Plotting the graph
    x = range(len(dates))  # x-axis values (0, 1, 2, ...)
    
    colors = plt.cm.tab10.colors  # Get a list of colors from the tab10 colormap
    markers = ['o', 's', 'v', '^', 'D', 'p', '*', 'h', 'x', '+']  # List of marker styles
    
    for i, user_type in enumerate(user_types):
        marker = markers[i % len(markers)]
        color = colors[i % len(colors)]
        
        y = [user_counts[date].get(user_type, 0) for date in dates]
        plt.scatter(x, y, marker=marker, color=color, s=100, label=user_type)
    
    plt.xticks(x, dates, rotation=45)  # Set the x-axis labels to dates and rotate them by 45 degrees
    plt.xlabel('Date')
    plt.ylabel('Number of Registered Users')
    plt.title('Registered Users by User Type')
    plt.legend(title='User Types', loc='upper left')
    
    # Saving the graph to a BytesIO object
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    
    # Encoding the image to base64
    graph_file = base64.b64encode(buffer.getvalue()).decode()
    
    plt.close()  # Close the plot to free up memory
    
    return graph_file



class LineChartJSONView(BaseLineChartView):
    def get_labels(self):
        """Return 7 labels for the x-axis."""
        return ["January", "February", "March", "April", "May", "June", "July"]

    def get_providers(self):
        """Return names of datasets."""
        return ["Central", "Eastside", "Westside"]

    def get_data(self):
        """Return 3 datasets to plot."""

        return [[75, 44, 92, 11, 44, 95, 35],
                [41, 92, 18, 3, 73, 87, 92],
                [87, 21, 94, 3, 90, 13, 65]]


line_chart = TemplateView.as_view(template_name='reports.html')
line_chart_json = LineChartJSONView.as_view()


def settings(request):
    
    codes=RegCode.objects.filter(id=1)
    a=''
    b=''
    c=''
    d=''
    e=''
    for t in codes:
        a = t.faculty
        b=t.staff
        c=t.nstp_coordinator
        d=t.admin
        e=t.rotc_coordinator
    form = RegCodeForm(initial = {'faculty': a,'staff':b,'nstp_coordinator':c,'admin':d,'rotc_coordinator':e})
    template=loader.get_template('settings.html')
    return HttpResponse(template.render({'codes':codes,'form':form},request))

def save_code(request):
    form = RegCodeForm(request.POST)
    codes=RegCode.objects.all()
    if codes.count()==0:
        if form.is_valid():
            form.save()
    else:  
        codes.filter(id=1).update(faculty=request.POST['faculty'],staff=request.POST['staff'],nstp_coordinator=request.POST['nstp_coordinator'],admin=request.POST['admin'],rotc_coordinator=request.POST['rotc_coordinator'])
    
    
    return settings(request)

def bulk_delete(request):
    Users.objects.filter(
        year_level = 'Senior'        
    ).update(is_active = False)
    
    return HttpResponseRedirect('/admin/users_list')

def privacy_policy(request):
    template=loader.get_template('privacy_policy.html')
    return HttpResponse(template.render(request=request))

def notifications(request):
    template=loader.get_template('notifications.html')
    
    notifs = Notifications.objects.all().order_by('-datetime')
    return HttpResponse(template.render(context={"notifs": notifs},request=request))

def view_notif(request, id):    
    notif = Notifications.objects.get(id=id)
    notif.is_read = True
    notif.medicine.delete()
    notif.delete()
    
    return HttpResponseRedirect('/notifications')


#reports
def reports_inventory(request):
    template=loader.get_template('reports/inventory.html')
    
    medicines = Inventory.objects.all()
    BASE_DIR = Path(__file__).resolve().parent.parent
    today=datetime.date.today()
    context = {
        "medicines": medicines,
        "dir": f"{BASE_DIR}/my_app/",
        "date": today
    }
    
    generator = pdf_generator(template, context) 
    pdf = generator.generate()
    
    response = HttpResponse(pdf.read(),content_type='application/pdf;')
    response['Content-Disposition'] = 'filename="reports_inventory.pdf"'
  
    return response

def reports_user_visit_history(request, id):
    template=loader.get_template('reports/user_visit_history.html')
    
    user = Users.objects.get(id=id)
    visits = CheckUpRecords.objects.filter(rec_id = user.id)
    
    BASE_DIR = Path(__file__).resolve().parent.parent
    today=datetime.date.today()
    context = {
        "user": user,
        "visits": visits,
        "dir": f"{BASE_DIR}/my_app/",
        "date": today
    }
    
    generator = pdf_generator(template, context) 
    pdf = generator.generate()
    
    response = HttpResponse(pdf.read(),content_type='application/pdf;')
    response['Content-Disposition'] = 'filename="reports_user_visit_history.pdf"'
  
    return response

def add_category(request):
    Category.objects.create(name=request.POST['name'].title())
    return HttpResponseRedirect('/admin/inventory')