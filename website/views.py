from django.shortcuts import render
from django.http import HttpResponse

from django.shortcuts import render,render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
# Create your views here.
from . import models
import time




def index(request):
    return render_to_response('../html/index.html',locals())
    #return HttpResponse('Hello World!') #用来向浏览器返回内容

def staff_login(request):
    return render_to_response('../html/staff_login.html',locals())

def user_login(request):
    return render_to_response('../html/user_login.html',locals())

def user_register(request):
    return render_to_response('../html/user_register.html',locals())

def staff_register(request):
    return render_to_response('../html/staff_register.html',locals())

@csrf_exempt
def user_query(request):
    return render_to_response('../html/user_query.html')

def query(request):
    return render_to_response('../html/query.html')

@csrf_exempt
def result(request):
    try:
        package = request.POST['package']
        name = request.POST['name']
        info = models.Package.objects.get(package_id=package)
        
        company = models.Company.objects.get(company_id=info.company_id)
        send = models.Address.objects.get(address_id=info.send_id)
        receive = models.Address.objects.get(address_id=info.receive_id)


        if (name != send.name) and (name != receive.name):
            return render_to_response('../html/notfound.html', locals())

        delivery = models.Delivery.objects.filter(package_id=package)   #很多
        delivery = sorted(delivery,key=lambda x: x.time,reverse=True)
        status = []
        for i in delivery:
            status.append([i,
                i.status,
                i.station,
                i.next_station,
                models.Staff.objects.get(staff_id=i.staff_id)
                ])
        
        
        
        
        return render_to_response('../html/result.html', locals())

    except:
        return render_to_response('../html/notfound.html', locals())

@csrf_exempt
def user_resu(request):
    try:
        package = request.POST['package']

        info = models.Package.objects.get(package_id=package)
        

        company = models.Company.objects.get(company_id=info.company_id)
        send = models.User.objects.get(user_id=info.send_id)
        receive = models.User.objects.get(user_id=info.receive_id)

        id = int(request.session['id'])
        if (int(id) != send.user_id) and (int(id) != receive.user_id):

            return render_to_response('../html/notfound.html', locals())

        delivery = models.Delivery.objects.filter(package_id=package)   #很多
        delivery = sorted(delivery,key=lambda x: x.time,reverse=True)
        status = []
        for i in delivery:
            status.append([i,
                models.Status.objects.get(status_id=i.status_id),
                models.Station.objects.get(station_id=i.station_id),
                models.Station.objects.get(station_id=i.next_station_id),
                models.Staff.objects.get(staff_id=i.staff_id)
                ])
        
        
        
        
        return render_to_response('../html/result.html', locals())

    except:
        return render_to_response('../html/notfound.html', locals())

@csrf_exempt
def staff_login_resu(request):
    try:
        id = request.POST['id']
        password = request.POST['password']
        request.session['id'] = id
        request.session['password'] = password

        staff = models.Staff.objects.get(staff_id=id)
        #user = models.User.objects.all()
        
        if staff.password != password:
            
            return render_to_response('../html/login_error.html')
        
        if staff.duty == '收货':
            return render_to_response('../html/staff_login_ok.html', locals())
        elif staff.duty == '扫描':
            return render_to_response('../html/staff_saomiao.html', locals())
        elif staff.duty == '派送':
            return render_to_response('../html/staff_paisong.html', locals())
        elif staff.duty == '运输':
            return HttpResponse('你好!'+staff.staff_name+'<br>员工编号：'+str(staff.staff_id)+'<br>联系方式：'+staff.staff_tel+'<br>')

        else:
            return HttpResponse('功能待完善...')
    except:
        return render_to_response('../html/login_error.html')

@csrf_exempt
def staff_input(request):
    id = request.session['id']
    password = request.session['password']
    c_id = models.Staff.objects.get(staff_id=id).company_id

    sender = request.POST['sender']
    receiver = request.POST['receiver']
    var = request.POST['varity']
    s_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(type(s_time),s_time)
    new = models.Package.objects.create(company_id=int(c_id), send_id=int(sender), receive_id=int(receiver), varity=var, send_time=s_time)
    
    info = models.Package.objects.get(send_time=s_time)
    
    company = models.Company.objects.get(company_id=info.company_id)
    send = models.Address.objects.get(address_id=info.send_id)
    receive = models.Address.objects.get(address_id=info.receive_id)
    staff = models.Staff.objects.get(staff_id=id)
    new_delivery = models.Delivery.objects.create(package_id=int(info.package_id),time=s_time,station=send.address,next_station=staff.station,status='待揽件',staff_id=int(id))


    return render_to_response('../html/staff_input.html', locals())


@csrf_exempt
def user_login_resu(request):
    #try:
        id = request.POST['id']
        password = request.POST['password']
        request.session['id'] = id
        request.session['password'] = password
        user = models.User.objects.get(user_id=id)
        address = models.Address.objects.filter(user_id=id)
        if user.password != password:
            return render_to_response('../html/login_error.html')

        send_infos = models.Package.objects.filter(send_id=id)
        receive_infos = models.Package.objects.filter(receive_id=id)


        send_packages = []
        for i in send_infos:
            company = models.Company.objects.get(company_id=i.company_id)
            send = models.Address.objects.get(address_id=i.send_id)
            receive = models.Address.objects.get(address_id=i.receive_id)

            delivery = models.Delivery.objects.filter(package_id=i.package_id)   #很多
            delivery = sorted(delivery,key=lambda x: x.time,reverse=True)
            
        
            
            send_package = {
                        'id':i.package_id,
                        'send_time':i.send_time,
                        'company':company.company_name,
                        'sender':send.name,
                        'receiver':receive.name,
                        'send_address':send.address,
                        'receive_address':receive.address,
                        'status':delivery[0].status
                        }

            send_packages.append(send_package)


        receive_packages = []
        for i in receive_infos:
            company = models.Company.objects.get(company_id=i.company_id)
            send = models.Address.objects.get(address_id=i.send_id)
            receive = models.Address.objects.get(address_id=i.receive_id)

            delivery = models.Delivery.objects.filter(package_id=i.package_id)   #很多
            delivery = sorted(delivery,key=lambda x: x.time,reverse=True)
        
            
            receive_package = {
                        'id':i.package_id,
                        'send_time':i.send_time,
                        'company':company.company_name,
                        'sender':send.name,
                        'receiver':receive.name,
                        'send_address':send.address,
                        'receive_address':receive.address,
                        'status':delivery[0].status
                        }

            receive_packages.append(receive_package)

        address = models.Address.objects.filter(user_id=id)
        
        
        return render_to_response('../html/user_query.html', locals())
    #except:
        return render_to_response('../html/login_error.html')

@csrf_exempt
def user_registe_resu(request):
    id = request.POST['id']
    password1 = request.POST['password1']
    password2 = request.POST['password2']

    all = models.User.objects.all()
    for i in all:
        if i.user_id == int(id):
            return HttpResponse('id:' + id + ' 已经被注册！')
    if password1 != password2:
        return HttpResponse('两次输入的密码不一致！')
    if password1 == '':
        return HttpResponse('密码不能为空！')
    new = models.User.objects.create(user_id=id,password=password1)
    return render_to_response('../html/user_register_ok.html')

@csrf_exempt
def staff_registe_resu(request):

    id = request.POST['id']
    password1 = request.POST['password1']
    password2 = request.POST['password2']
    name = request.POST['name']
    tel = request.POST['tel']
    station = request.POST['station']
    duty = request.POST['duty']

    all = models.Staff.objects.all()
    print(all)
    for i in all:
        if i.staff_id == int(id):
            return HttpResponse('id:' + id + ' 已经被注册！')
    if password1 != password2:
        return HttpResponse('两次输入的密码不一致！')
    if password1 == '':
        return HttpResponse('密码不能为空！')
    new = models.Staff.objects.create(staff_id=int(id),password=password1, staff_name=name,staff_tel=tel,station=station,duty=duty,company_id=1)
    return render_to_response('../html/staff_register_ok.html')


@csrf_exempt
def saomiao(request):
    id = request.session['id']
    p_id = request.POST['package_id']
    staff = models.Staff.objects.get(staff_id=id)
    n_sta = request.POST['next_station']
    stat = request.POST['status']
    s_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    
    new_delivery = models.Delivery.objects.create(package_id=int(p_id),time=s_time,station=staff.station,next_station=n_sta,status=stat,staff_id=int(id))
    return render_to_response('../html/success.html')

@csrf_exempt
def paisong(request):
    id = request.session['id']
    p_id = request.POST['package_id']
    success = request.POST['success']
    s_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    staff = models.Staff.objects.get(staff_id=id)
    if success == 'yes':
        new_delivery = models.Delivery.objects.create(package_id=int(p_id),time=s_time,station=staff.station,status='已签收',staff_id=int(id))
        package = models.Package.objects.get(package_id=int(p_id))
        package.receive_time = s_time
        package.save()
    return render_to_response('../html/success.html')

@csrf_exempt
def address_add(request):
    try:
        id = request.session['id']
        name = request.POST['name']
        tel = request.POST['tel']
        address = request.POST['address']

        new_add = models.Address.objects.create(user_id=id, name=name, tel=tel, address=address)

        return render_to_response('../html/success.html')
    except:
        return render_to_response('../html/error.html')

@csrf_exempt
def address_change(request):
    try:
        id = request.session['id']
        address_id = request.POST['address_id']
        name = request.POST['name']
        tel = request.POST['tel']
        address = request.POST['address']

        target = models.Address.objects.get(address_id=address_id)
        target.name = name
        target.tel = tel
        target.address = address
        target.save()
        return render_to_response('../html/success.html')
    except:
        return render_to_response('../html/error.html')

@csrf_exempt
def address_delete(request):
    try:
        id = request.session['id']
        address_id = request.POST['address_id']
        target = models.Address.objects.get(address_id=address_id)
        target.delete()
        return render_to_response('../html/success.html')
    except:
        return render_to_response('../html/error.html')