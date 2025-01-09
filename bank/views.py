from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect

from bank.forms import ExtendedUserCreationForm
from bank.models import BloodDonor, BloodInventory


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
            messages.error(request, "Invalid username or password.")
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
        qunty = request.POST['qunty']
        status = 'PENDING'

        # if health_issue is not None and health != 'none':
        #     status = 'Rejected'
        #
        if health == 'other':
            health = health_issue

        donor = BloodDonor(fullname=name,age=age,email=email,mobile_number=phone,address=address,
                               gender=gender,health_issue=health,blood_type=group,quantity=qunty,status=status)
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
        donor.quantity = request.POST['qunty']
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
    inventory = BloodInventory.objects.get(id=id)

    if request.method == 'POST':
        inventory.available_qnty += float (request.POST['qunty'])
        inventory.save()

    return render(request,'collect.html')


def supply_inventory(request, id):
    inventory = BloodInventory.objects.get(id=id)

    if request.method == 'POST':
        inventory.available_qnty -= float (request.POST['qunty'])
        inventory.save()

    return render(request, 'supply_invent.html')

def donor_list(request):
    donors = BloodDonor.objects.all()  # Fetch all records
    return render(request, 'collect.html', {'donors': donors})