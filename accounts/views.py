import random
import urllib

from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from Donation import settings
from accounts.models import Profile
import http.client

from number.forms import NumberForm


#
def send_otp(mobile, otp):
    conn = http.client.HTTPSConnection("api.msg91.com")
    authkey = settings.AUTH_KEY
    headers = {'content-type': "application/json"}
    message = "Your otp is " + otp
    url = "http://control.msg91.com/api/sendotp.php?authkey=" + authkey + "&mobile=" + mobile + "&otp=" + otp + "&message=" + urllib.parse.quote(
        message) + "&country=91"
    conn.request("GET", url, headers=headers)
    res = conn.getresponse()
    data = res.read()
    print(data)
    return None


def Register(request):
    profile = Profile.objects.all()
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        check_user = User.objects.filter(email=email).exists()
        check_profile = Profile.objects.filter(mobile=mobile).exists()
        if check_user or check_profile:
            context = {'message': 'user already exists', 'class': 'danger'}
            return render(request, 'Html/Register.html', context)
        user = User(username=email, email=email, first_name=name)
        user.save()
        otp = str(random.randint(1000, 9999))
        profile = Profile(user=user, mobile=mobile, otp=otp)
        profile.save()
        send_otp(mobile, otp)
        request.session['mobile'] = mobile
        return redirect('otp')
    return render(request, 'Html/Register.html', {'profiles': profile})


def otp(request):
    mobile = request.session['mobile']
    context = {'mobile': mobile}
    form = NumberForm()
    if request.method == 'POST':
        otp = request.POST.get('otp')
        print(otp)
        profile = Profile.objects.filter(mobile=mobile).first()
        if otp == profile.otp:
            print('Debug')
            return redirect('payment')
        else:
            print('Debug1')

            context = {'message': 'wrong otp', 'class': 'danger', 'mobile': mobile}
            return render(request, 'Html/otp.html', context)
    return render(request, 'Html/otp.html', context)


def login_attempt(request):
    if request.method == 'POST':
        mobile = request.POST.get('mobile')

        user = Profile.objects.filter(mobile=mobile).first()

        if user is None:
            context = {'message': 'User not found', 'class': 'danger'}
            return render(request, 'Html/login.html', context)

        otp = str(random.randint(1000, 9999))
        user.otp = otp
        user.save()
        send_otp(mobile, otp)
        request.session['mobile'] = mobile
        return redirect('login_otp')
    return render(request, 'Html/login.html')


def login_otp(request):
    mobile = request.session['mobile']
    context = {'mobile': mobile}
    if request.method == 'POST':
        otp = request.POST.get('otp')
        profile = Profile.objects.filter(mobile=mobile).first()

        if otp == profile.otp:
            user = User.objects.get(id=profile.user.id)
            login(request, user)
            return redirect('payment')
        else:
            context = {'message': 'Wrong OTP', 'class': 'danger', 'mobile': mobile}
            return render(request, 'Html/login_otp.html', context)

    return render(request, 'Html/login_otp.html', context)


def logout_view(request):
    logout(request)
    return redirect('register')


def thanku(request):
    return render(request, 'includes/navbar.html')
