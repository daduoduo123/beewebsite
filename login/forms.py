from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from .models import OAuthRelationship


class LoginForm(forms.Form):
    username_or_email = forms.CharField(label='用户名或邮箱',
                                        widget=forms.TextInput(
                                            attrs={'class': 'form-control', 'placeholder': '请输入用户名或邮箱'}))
    password = forms.CharField(label='密码',
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入用密码'}))

    def clean(self):
        username_or_email = self.cleaned_data.get('username_or_email')
        password = self.cleaned_data.get('password')

        user = auth.authenticate(username=username_or_email, password=password)
        if user is None:
            if User.objects.filter(email=username_or_email).exists():
                username = User.objects.get(email=username_or_email).username
                user = auth.authenticate(username=username, password=password)
                if user is None:
                    raise forms.ValidationError('用户名或密码不正确')
                else:
                    self.cleaned_data['user'] = user
            else:
                raise forms.ValidationError('用户名或密码不正确')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data


class RegForm(forms.Form):
    username = forms.CharField(label='用户名',
                               max_length=30,
                               min_length=3,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入3-30位用户名'}))
    email = forms.EmailField(label='邮箱',
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '请输入邮箱'}))
    verification_code = forms.CharField(label='验证码',
                                        required=False,
                                        widget=forms.TextInput(
                                            attrs={'class': 'form-control', 'placeholder': '点击发送验证码'}))
    password = forms.CharField(label='密码',
                               min_length=6,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入密码'}))
    password_again = forms.CharField(label='重复密码',
                                     min_length=6,
                                     widget=forms.PasswordInput(
                                         attrs={'class': 'form-control', 'placeholder': '请再次输入密码'}))

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(RegForm, self).__init__(*args, **kwargs)

    def clean(self):
        code = self.request.session.get('register_code', '')
        verification_code = self.cleaned_data.get('verification_code', '')
        if not (code != '' and code == verification_code):
            raise forms.ValidationError('验证码不正确')
        return self.cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已存在')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱已存在')
        return email

    def clean_password_again(self):
        password = self.cleaned_data.get('password')
        password_again = self.cleaned_data.get("password_again")
        if password != password_again:
            raise forms.ValidationError('两次密码输入不一致')
        return password_again

    def clean_verification_code(self):
        verification_code = self.cleaned_data.get('verification_code')
        if verification_code == '':
            raise forms.ValidationError('验证码不能为空')
        return verification_code


class ChangeNicknameForm(forms.Form):
    nickname_new = forms.CharField(
        label='新的昵称',
        max_length=20,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '请输入新的昵称'}
        )
    )

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(ChangeNicknameForm, self).__init__(*args, **kwargs)

    def clean(self):
        # 判断用户是否登录
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('用户尚未登录')
        return self.cleaned_data

    def clean_nickname_new(self):
        nickname_new = self.cleaned_data.get('nickname_new', '').strip()
        if nickname_new == '':
            raise forms.ValidationError("新的昵称不能为空")
        return nickname_new


class BindEmailForm(forms.Form):
    email = forms.EmailField(label='邮箱',
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '请输入邮箱'}))
    verification_code = forms.CharField(label='验证码',
                                        required=False,
                                        widget=forms.TextInput(
                                            attrs={'class': 'form-control', 'placeholder': '点击发送验证码'}))

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(BindEmailForm, self).__init__(*args, **kwargs)

    def clean(self):
        # 用户是否登录
        if self.request.user.is_authenticated:
            self.cleaned_data['user'] = self.request.user
        else:
            raise forms.ValidationError('用户尚未登录')
        # 用户是否绑定
        if self.request.user.email != '':
            raise forms.ValidationError('你已经绑定邮箱')
        # 判断验证码
        code = self.request.session.get('bind_email_code')
        verification_code = self.cleaned_data.get('verification_code', '')
        if not (code != '' and code == verification_code):
            raise forms.ValidationError('验证码不正确')
        return self.cleaned_data

    def clean_verification_code(self):
        verification_code = self.cleaned_data.get('verification_code')
        if verification_code == '':
            raise forms.ValidationError('验证码不能为空')
        return verification_code

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('该邮箱已经绑定')
        return email


class ChangePasswordForm(forms.Form):
    password_old = forms.CharField(label='旧密码',
                                   min_length=6,
                                   widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入旧密码'}))
    password_new = forms.CharField(label='新密码',
                                   min_length=6,
                                   widget=forms.PasswordInput(
                                       attrs={'class': 'form-control', 'placeholder': '请输入新密码'}))
    password_new_again = forms.CharField(label='重复新密码',
                                         min_length=6,
                                         widget=forms.PasswordInput(
                                             attrs={'class': 'form-control', 'placeholder': '请重复输入新密码'}))

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        # 判断用户是否登录,
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('用户尚未登录')
        return self.cleaned_data

    def clean_password_old(self):
        password_old = self.cleaned_data.get('password_old')
        if not self.user.check_password(password_old):
            raise forms.ValidationError("原先密码错误")
        return password_old

    def clean_password_new_again(self):
        password_new = self.cleaned_data.get('password_new', '')
        password_new_again = self.cleaned_data.get("password_new_again", '')
        if password_new != password_new_again or password_new == '':
            raise forms.ValidationError('两次密码输入不一致')
        return self.cleaned_data


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label='邮箱',
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入用户名邮箱'}))

    password_new = forms.CharField(label='新密码',
                                   min_length=6,
                                   widget=forms.PasswordInput(
                                       attrs={'class': 'form-control', 'placeholder': '请再次输入密码'}))
    verification_code = forms.CharField(label='验证码',
                                        required=False,
                                        widget=forms.TextInput(
                                            attrs={'class': 'form-control', 'placeholder': '点击发送验证码'}))

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(ForgotPasswordForm, self).__init__(*args, **kwargs)

    def clean_username(self):
        email = self.cleaned_data.get('email').strip()
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('不存在该邮箱')
        return email

    def clean_verification_code(self):
        code = self.request.session.get('forget_password_code', '')
        verification_code = self.cleaned_data.get('verification_code', '')
        if verification_code == '':
            raise forms.ValidationError('验证码不能为空')
        if not (code != '' and code == verification_code):
            raise forms.ValidationError('验证码不正确')
        return verification_code


class BindQQForm(forms.Form):
    username_or_email = forms.CharField(label='用户名或邮箱',
                                        widget=forms.TextInput(
                                            attrs={'class': 'form-control', 'placeholder': '请输入用户名或邮箱'}))
    password = forms.CharField(label='密码',
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入用密码'}))

    def clean(self):
        username_or_email = self.cleaned_data.get('username_or_email')
        password = self.cleaned_data.get('password')

        user = auth.authenticate(username=username_or_email, password=password)
        if user is None:
            if User.objects.filter(email=username_or_email).exists():
                username = User.objects.get(email=username_or_email).username
                user = auth.authenticate(username=username, password=password)
                if user is None:
                    raise forms.ValidationError('用户名或密码不正确')
                else:
                    self.cleaned_data['user'] = user
            else:
                raise forms.ValidationError('用户名或密码不正确')
        else:
            self.cleaned_data['user'] = user

        if OAuthRelationship.objects.filter(user=user, oauth_type=0).exists():
            raise forms.ValidationError('该用户已经绑定QQ账号')
        return self.cleaned_data
