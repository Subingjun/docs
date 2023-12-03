from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms.models import ModelForm
from django import forms
from mobsf.register.encrypt import md5


class RegisterModelForm(ModelForm):

    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ["username", "password", "confirm_password"]
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if confirm != pwd:
            raise ValidationError("密码不一致")
        return confirm

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        for name,field in self.fields.items():

            if field.widget.attrs:
                field.widget.attrs["class"] = "form-control"
            else:
                field.widget.attrs = {
                    "class":"form-control",
                }


def register(request):
    if request.method == "GET":
        form = RegisterModelForm()
        context = {
            'title': "用户注册",
            'form': form
        }
        return render(request, 'register/register.html', context)

    elif request.method == 'POST':

        form = RegisterModelForm(data=request.POST)

        user_name = request.POST.get('username')
        pwd = request.POST.get('password')
        confirm_pwd = request.POST.get('confirm_password')

        if form.is_valid():

            user = User.objects.create_user(
                username=user_name,
                password=pwd,
            )
            return redirect('/register/') # 要改成登陆页面

        if pwd != confirm_pwd:
            error = '密码不一致'

        context = {
                'title': "用户注册",
                'form': form,
                'error':error
            }

        return render(request, 'register/register.html', context)
