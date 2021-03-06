# -*- coding: utf-8 -*-
# __author__ = 'jason_lee'
from models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.safestring import mark_safe
from django.forms.widgets import FileInput
from django import forms
from django.utils.translation import ugettext_lazy as _


class AdminImageFieldWithThumbWidget(FileInput):

    def __init__(self, thumb_width=50, thumb_height=50):
        self.width = thumb_width
        self.height = thumb_height
        super(AdminImageFieldWithThumbWidget, self).__init__({})

    def render(self, name, value, attrs=None):
        thumb_html = ''
        if value and hasattr(value, "url"):
            thumb_html = '<img src="%s" width="%s" width="%s"/>' % (value.url, self.width, self.height)
        return mark_safe("%s%s" % (thumb_html, super(AdminImageFieldWithThumbWidget, self).render(name, value, attrs)))


class UserCreationForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"), widget=forms.PasswordInput,
                                help_text=_("Enter the same password as above, for verification."))

    class Meta:
        model = User
        fields = ("email",)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label=_("Password"),
                                         help_text=_("Raw passwords are not stored, so there is no way to see \
                                                     this user's password, but you can change the password \
                                                     using <a href=\"password/\">this form</a>."))

    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class PermissionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PermissionForm, self).__init__(*args, **kwargs)
        # access object through self.instance...
        self.fields['content_type'].queryset = ContentType.objects.filter(app_label__in=['account', 'discussion'])

    class Meta:
        model = Permission
        fields = ('name', 'codename', 'content_type', 'display')


class AccountForm(forms.ModelForm):
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"), widget=forms.PasswordInput,
                                help_text=_("Enter the same password as above, for verification."))
    user_image = forms.ImageField()

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', 'phone_number', 'user_image')

    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            self.fields['email'].widget.attrs['readonly'] = 'readonly'
            if self.instance.phone_number:
                self.fields['phone_number'].widget.attrs['readonly'] = 'readonly'
