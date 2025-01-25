from statistics import quantiles

from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from bank.forms import ExtendedUserCreationForm
from bank.models import BloodDonor, BloodInventory, DonationList, UserBloodRequest


def user_registration(request):

    if request.method == 'POST':
        form = ExtendedUserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the user
            messages.success(request, "Registration successful! You can now log in.")
            return redirect('/')  # Redirect to the login page
        else:
            messages.error(request, "Registration failed. Please check the errors below.")
    else:
        form = ExtendedUserCreationForm()

    return render(request, 'registration.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pswd']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('/adminhome')
            else:
                return redirect('/userhome')
        else:
            return render(request, 'login.html', {
                'error_message': 'Invalid username or password..'
            })

    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('/')

@login_required
def admin_dashboard(request):
    return render(request,'admin_dashboard.html')

@login_required
def user_dashboard(request):
    return render(request,'user_dashboard.html')

def register_donor(request):
    if request.method == 'POST':
        name = request.POST['fname']
        age = request.POST['age']
        email = request.POST['email']
        phone = request.POST['phone']
        gender = request.POST.get('gender', None)
        address = request.POST['addrs']
        health = request.POST['health']
        health_issue = request.POST['other-condition']
        group = request.POST['group']
        status = 'PENDING'

        # if health_issue is not None and health != 'none':
        #     status = 'Rejected'
        #
        if health == 'other':
            health = health_issue

        donor = BloodDonor(fullname=name,age=age,email=email,mobile_number=phone,address=address,
                               gender=gender,health_issue=health,blood_type=group,status=status)
        donor.save()
        return redirect('/viewdonor')
    return render(request,'add_donor.html')


def view_donor(request,status=None):
    search_data = request.GET.get('search', '').strip()
    if search_data:
        donors = BloodDonor.objects.filter(
            Q(fullname__icontains=search_data) |
            Q(blood_type__icontains=search_data) |
            Q(status__icontains=search_data)
        )

    elif status and status.upper() in ["APPROVED", "REJECTED", "PENDING"]:
        donors = BloodDonor.objects.filter(status=status.upper())
    else:
        donors = BloodDonor.objects.all()

    return render(request, 'view_donor.html', {'donors': donors})

def detailed_view_donor(request,id):
    donor= BloodDonor.objects.get(id=id)
    return render(request,'detailed_view.html',{'donor':donor})


def update_donor(request, id):
    donor = BloodDonor.objects.get(id=id)

    if request.method == 'POST':

        donor.fullname = request.POST['fname']
        donor.age = request.POST['age']
        donor.email = request.POST['email']
        donor.mobile_number = request.POST['phone']
        donor.gender = request.POST.get('gender', None)
        donor.address = request.POST['addrs']
        donor.health_issue = request.POST['health']

        donor.blood_type = request.POST['group']
        donor.status = request.POST['status']

        donor.save()
        return redirect('/viewdonor')

    return render(request, 'detailed_view.html', {'donor': donor})


def delete_donor(request, id):
    donor = BloodDonor.objects.get(id=id)
    donor.delete()
    return redirect('/viewdonor')

def get_inventory(request):
    inventory = BloodInventory.objects.all()
    return render(request,'view_inventory.html',{'inventory':inventory})

def collect_inventory(request,id):
    inventory = get_object_or_404(BloodInventory, id=id)

    if request.method == 'POST':
        quantity = float(request.POST['qunty'])
        inventory.available_qnty += quantity
        inventory.save()

        # Update donor collection status
        donor = get_object_or_404(BloodDonor, id=request.POST['donor'])
        data_list = DonationList(donor_id =donor.id ,name =donor.fullname ,blood_type = donor.blood_type,quantity = quantity ,status=True)
        data_list.save()
        return redirect('/inventorylist')

    donors = BloodDonor.objects.filter(status='APPROVED')
    return render(request,'collect.html',{'donors': donors})


def supply_inventory(request, id):
    inventory = get_object_or_404(BloodInventory, id=id)

    if request.method == 'POST':
        quantity = float(request.POST['qunty'])

        if quantity > inventory.available_qnty:
            # Return an error message if the entered quantity exceeds available quantity
            reqt = UserBloodRequest.objects.filter(status='APPROVED')
            return render(request, 'supply.html', {
                'reqt': reqt,
                'error_message': 'Entered quantity exceeds available inventory.'
            })

        inventory.available_qnty -= quantity
        inventory.save()

        # Update donor collection status
        data = get_object_or_404(UserBloodRequest, id=request.POST['requst'])
        data.status = 'RECEIVED'
        data.save()
        return redirect('/inventorylist')

    reqt = UserBloodRequest.objects.filter(status='APPROVED')
    return render(request, 'supply.html', {'reqt': reqt})

def view_blood_request(request):
    datas = UserBloodRequest.objects.all()
    return render(request, 'view_request.html', {'datas': datas})


def register_request(request):
    user_id = request.user.id

    if request.method == 'POST':
        name = request.POST['fname']
        age = request.POST['age']
        email = request.POST['email']
        phone = request.POST['phone']
        gender = request.POST.get('gender', None)
        address = request.POST['addrs']
        health = request.POST['reason']
        group = request.POST['group']
        quantity = request.POST['qunty']
        status = 'PENDING'

        datas = UserBloodRequest(name=name,age=age,email=email,mobile_number=phone,address=address,gender=gender,
                        health_issue=health,blood_type=group,quantity= quantity,status=status,request_id=user_id)
        datas.save()
        return redirect('/requestlist')
    return render(request,'request_form.html')

def user_request_list(request,status=None):
    search_data = request.GET.get('search', '').strip()
    if search_data:
        reqt = UserBloodRequest.objects.filter(
            Q(name__icontains=search_data) |
            Q(blood_type__icontains=search_data) |
            Q(status__icontains=search_data)
        )

    elif status and status.upper() in ["APPROVED", "REJECTED", "PENDING"]:
        reqt = UserBloodRequest.objects.filter(status=status.upper())
    else:
        reqt = UserBloodRequest.objects.all()

    return render(request, 'req_verification.html', {'reqt': reqt})

def approve_reject_request(request,id,status=None):
    reqt = get_object_or_404(UserBloodRequest, id=id)
    if status and status.upper() in ["APPROVED", "REJECTED"]:
        reqt.status = status
        reqt.save()
        return redirect('/viewrequest')
    return render(request, 'approve_reject.html',{'data':reqt})

def update_request(request, id):
    reqt = get_object_or_404(UserBloodRequest, id=id)

    if request.method == 'POST':
        reqt.name = request.POST['fname']
        reqt.age = request.POST['age']
        reqt.email = request.POST['email']
        reqt.mobile_number = request.POST['phone']
        reqt.gender = request.POST.get('gender', None)
        reqt.address = request.POST['addrs']
        reqt.health_issue = request.POST['health']
        reqt.blood_type = request.POST['group']
        reqt.quantity = request.POST['qunty']
        reqt.save()
        return redirect('/requestlist')

    return render(request, 'approve_reject.html')


def delete_request(request, id):
    reqt = get_object_or_404(UserBloodRequest, id=id)
    reqt.delete()
    return redirect('/requestlist')

def detailed_request(request,id):
    reqt = get_object_or_404(UserBloodRequest, id=id)
    return render(request,'request_details.html',{'data':reqt})


def view_profile(request):
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    return render(request,'profile.html',{'user':user})

def update_profile(request):
    user_id = request.user.id
    user = User.objects.get(id=user_id)

    if request.method == 'POST':
        user.username = request.POST['uname']
        user.first_name = request.POST['fname']
        user.last_name = request.POST['lname']
        user.email = request.POST['email']

        user.save()
        return redirect('/adminhome')

    return render(request,'profile.html')

def change_password(request):
    if request.method == 'POST':
        old_pass = request.POST['oldpass']
        new_pass = request.POST['newpass']
        cnf_pass = request.POST['cpass']
        data = check_password(old_pass,request.user.password )
        if data:
            if new_pass == cnf_pass:
                u = User.objects.get(id=request.user.id)
                u.set_password(new_pass)
                u.save()
                logout(request)
                return redirect('/')
            else:
                return render(request, 'changepass.html', {
                    'error_message': 'password is not matching.'
                })
        else:
            return render(request, 'changepass.html', {
                'error_message': 'Enter the correct password.'
            })

    return render(request,'changepass.html')

def inactivate_user(request):
    user = User.objects.get(id=request.user.id)
    user.is_active = False
    user.save()
    logout(request)
    return redirect('/')

