# -*- coding:utf-8 -*-
from django.shortcuts import HttpResponseRedirect, render
from django.views.generic import TemplateView
from forms import AccountForm
from models import User
from django.contrib import messages
from django.contrib.auth import logout, login
from backends import EmailOrNumberModelBackend
from django.utils.translation import ugettext_lazy as _
# Create your views here.


def account_logout(request):
    logout(request)
    return HttpResponseRedirect('/account/login/')


def account_login(request):
    logout(request)
    if request.POST:
        email = request.POST['email']
        password = request.POST['password']

        user = EmailOrNumberModelBackend().authenticate(username=email, password=password)
        if user:
            user.backend = 'account.backends.EmailOrNumberModelBackend'
            login(request, user)
            return HttpResponseRedirect('/discussion/list/')
        else:
            messages.add_message(request, messages.ERROR,  _('email or password is invalid.'))
    return render(request, 'login.html')


class AccountDetail(TemplateView):
    template_name = 'user_info.html'
    model = User

    def get_context_data(self, **kwargs):
        context = super(AccountDetail, self).get_context_data(**kwargs)
        context['userform'] = AccountForm(instance=self.request.user)
        context['current_image'] = self.request.user.user_image.url
        return context

    def post(self, *args, **kwargs):
        if self.request.FILES.get("user_image"):
            self.request.user.user_image = self.request.FILES.get("user_image")
            self.request.user.save()
            messages.add_message(self.request, messages.INFO, _('user_photo change success'))
        if self.request.POST.get("password1") and self.request.POST.get("password2"):
            if self.request.POST.get("password1") == self.request.POST.get("password2"):
                self.request.user.set_password(self.request.POST.get("password1"))
                self.request.user.save()
                messages.add_message(self.request, messages.INFO, _('password change success'))
                return HttpResponseRedirect('/account/login/')
            else:
                print _("password are not consistent")
                messages.add_message(self.request, messages.ERROR, _('password are not consistent'))
        if self.request.user.phone_number != self.request.POST.get("phone_number"):
            self.request.user.phone_number = self.request.POST.get("phone_number")
            self.request.user.save()
            messages.add_message(self.request, messages.INFO, _('add phone_number success'))

        return HttpResponseRedirect('/account/detail/')
