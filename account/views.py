from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from .forms import SignUpForm, LoginForm, ChangePassForm, ResetPassForm
from .utils import generate_code, send_to_mail
# Create your views here.


# def singnup_view(request):
#     if request.method == "POST":
#         username = request.POST['username']
#         first_name = request.POST['first_name']
#         last_name = request.POST['last_name']
#         email = request.POST['email']
#         password1 = request.POST['password1']
#         password2 = request.POST['password2']
        
#         if password1 != password2:
#             messages.error(request, 'Parollar togri kelmadi')
#             return redirect('signup')
        
#         if User.objects.filter(username=username).exists():
#             messages.error(request, 'Bu username orqali oldin roxatdan otilgan')
#             return redirect('signup')
            
#         User.objects.create_user(username=username, first_name=first_name, \
#             last_name=last_name, email=email, password=password1)
#         messages.success(request, 'Siz muvaffaqqiyatli roxatdan otdingiz!')
#         return redirect('login')
    
#     return render(request, 'account/signup.html')
    
        
            
# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
        
#         if username is None or password is None:
#             messages.error(request, 'Login yoki parol kiritilmadi.')
        
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             messages.success(request, 'Siz login qildingiz!')
#             return redirect('index')

#         messages.error(request, 'Bunaqa user topilmadi')
#         return redirect('login')
#     return render(request, 'account/login.html')
        
                
def logout_view(request):
    logout(request)
    messages.info(request, 'Siz dasturdan chiqdingiz')
    return redirect('index')


def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Bu username orqali oldin roxatdan otilgan')
            form.save()
            messages.success(request, "Roxatdan otdizgiz")
            return redirect('login')
        else:
            messages.error(request, 'Nimzdir xatolik ketdi')
        
    form = SignUpForm()
    return render(request, 'account/signup.html', {'form':form})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Siz dasturga kirdingiz')
            return redirect('index')
        else:
            messages.error(request, 'Nimzdir xato ketdi')
    form = LoginForm()
    return render(request, 'account/login.html',  {'form':form})

            
def change_pass_view(request):
    if request.method == "GET":
        code = generate_code()
        request.session['verification_code'] = code
        send_to_mail(request.user.email, code)
        messages.info(request, 'Emailingizga kod yuborildi')
        form = ChangePassForm()
        return render(request, 'account/change_pass.html', {'form': form})
    else:
        form = ChangePassForm(request.POST)
        if form.is_valid():
            old_pass = form.cleaned_data['old_pass']
            new_pass = form.cleaned_data['new_pass']
            code = form.cleaned_data['code']
            session_code = request.session.get('verification_code')
            
            if not request.user.check_password(old_pass):
                messages.error(request, 'Siz eski parolingizni xato kiritdingiz!')
                return redirect('change-pass')
            if session_code != code:
                messages.error(request, 'Tasdiqlash codeingiz xato')
                return redirect('change-pass')
            
            user = request.user
            user.set_password(new_pass)
            user.save()
            messages.success(request, 'Parolingiz ozgartirildi')
            update_session_auth_hash(request, user)
            del request.session['verification_code']
            return redirect('profile')
        return redirect('change-pass')

from datetime import datetime, timedelta
def reset_pass(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            user = User.objects.get(username=username)
            code = generate_code()
            request.session['reset_code'] = code
            request.session['username'] = username
            request.session['create_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            send_to_mail(user.email, code)
            return redirect('reset2')
        
        except User.DoesNotExist:
            return render(request, 'account/reset_pass1.html')
    
    return render(request, 'account/reset_pass1.html')


def reset_pass2(request):
    if request.method == 'POST':
        form = ResetPassForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            code = form.cleaned_data['code']
            session_code = request.session.get('reset_code')
            username = request.session.get('username')
            create_at_ = request.session.get('create_at')
            create_at = datetime.strptime(create_at_, '%Y-%m-%d %H:%M:%S')

            
            if datetime.now() - create_at > timedelta(minutes=1):
                messages.info(request, 'Emailga yuborilgan kod eskirgan')
                return redirect('reset2')

            if session_code != code:
                messages.error(request, 'Tasdiqlash codeingiz xato')
                return redirect('reset2')
            
            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()
            messages.success(request, 'Parolingiz ozgartirildi')
            del request.session['reset_code']
            del request.session['username']
            return redirect('login')
    return render(request, 'account/reset_pass2.html')
            
        
        

        
                 
        
            
        
        
        
        
        
        
        
        
            
