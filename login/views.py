import random
import string
import time
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings

from .forms import RegForm, LoginForm, ChangeNicknameForm, BindEmailForm, ChangePasswordForm, ForgotPasswordForm
from .models import Profile


# Create your views here.
# 登录
def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data.get('user')
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        login_form = LoginForm()
    context = {}
    context['login_form'] = login_form
    return render(request, 'login/login.html', context)


# 注册
def register(request):
    if request.method == 'POST':
        reg_form = RegForm(request.POST, request=request)
        if reg_form.is_valid():
            username = reg_form.cleaned_data.get('username')
            password = reg_form.cleaned_data.get('password1')
            email = reg_form.cleaned_data.get('email')
            # 创建用户
            User.objects.create_user(username, email, password)
            # 清除session
            del request.session['register_code']
            # 登录用户
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        reg_form = RegForm()

    context = {}
    context['reg_form'] = reg_form
    return render(request, 'login/register.html', context)


# 登出
def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('from', reverse('home')))


# 用户个人信息
def user_info(request):
    context = {}
    return render(request, 'login/user_info.html', context)


# 登录窗口
def login_for_medal(request):
    login_form = LoginForm(request.POST)
    data = {}
    if login_form.is_valid():
        user = login_form.cleaned_data['user']
        auth.login(request, user)
        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)


# 修改昵称
def change_nickname(request):
    redirect_to = request.GET.get('from', reverse('home'))
    if request.method == 'POST':

        form = ChangeNicknameForm(request.POST, user=request.user)
        if form.is_valid():
            nickname_new = form.cleaned_data.get('nickname_new')
            profile, created = Profile.objects.get_or_create(user=request.user)
            profile.nickname = nickname_new
            profile.save()
            return redirect(redirect_to)
    else:
        form = ChangeNicknameForm()
    context = {}
    context['page_title'] = '修改昵称'
    context['form_title'] = '修改昵称'
    context['submit_text'] = '修改'
    context['form'] = form
    context['return_back_url'] = redirect_to
    return render(request, 'form.html', context)


#　用户绑定邮箱
def bind_email(request):
    redirect_to = request.GET.get('from', reverse('home'))
    if request.method == 'POST':
        form = BindEmailForm(request.POST, request=request)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            request.user.email = email
            request.user.save()
            # 清除session
            del request.session['register_code']
            return redirect(redirect_to)
    else:
        form = BindEmailForm()
    context = {}
    context['page_title'] = '绑定邮箱'
    context['form_title'] = '绑定邮箱'
    context['submit_text'] = '绑定'
    context['form'] = form
    context['return_back_url'] = redirect_to
    return render(request, 'login/bind_email_form.html', context)


# 往邮箱发送验证码
def send_verification_code(request):
    email = request.GET.get('email', '')
    print(email)
    send_for = request.GET.get('send_for', '')
    data = {}
    print('hello')
    if email != '':
        # 生成验证码
        code = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        print(code)
        now = int(time.time())
        print(now)
        send_code_time = request.session.get('send_code_time', 0)
        if now - send_code_time <= 30:
            data['status'] = 'ERROR'
        else:
            # 把信息存在session中
            request.session['send_code_time'] = now
            request.session[send_for] = code
            # print(code)
            # 发送邮件
            send_mail(
                '%s绑定邮箱' % settings.EMAIL_SUBJECT_PREFIX,  # Subject here
                '验证码:%s' % code,  # Here is the message
                settings.EMAIL_HOST_USER,  # from@example.com
                [email],  # to@example.com
                fail_silently=False,
            )
            data['status'] = 'SUCCESS'

    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)


# 更改密码
def change_password(request):
    redirect_to = request.GET.get('from', reverse('home'))
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST, user=request.user)
        if form.is_valid():
            password_new = form.cleaned_data.get('password_new')
            request.user.set_password(password_new)
            request.user.save()
            auth.logout(request)
            return redirect(redirect_to)
    else:
        form = ChangePasswordForm()

    context = {}
    context['page_title'] = '修改密码'
    context['form_title'] = '修改密码'
    context['submit_text'] = '确认修改'
    context['form'] = form
    context['return_back_url'] = redirect_to
    return render(request, 'form.html', context)


# 忘记密码，重置密码
def forget_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST, request=request)
        if form.is_valid():
            password_new = form.cleaned_data.get('password_new')
            email = form.cleaned_data.get('email')
            user = User.objects.get(email=email)
            user.set_password(password_new)
            user.save()
            del request.session['forget_password_code']
            return redirect(reverse('home'))
    else:
        form = ForgotPasswordForm()

    context = {}
    context['page_title'] = '重置密码'
    context['form_title'] = '重置密码'
    context['submit_text'] = '确认修改'
    context['form'] = form
    context['return_back_url'] = reverse('home')
    return render(request, 'login/forget_password.html', context)
