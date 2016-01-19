# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from django.contrib import auth
from django.contrib.contenttypes.models import ContentType
from django.core.validators import EmailValidator, RegexValidator
from django.core.exceptions import PermissionDenied
from PIL import Image
from easy_thumbnails.fields import ThumbnailerImageField
from django.core.mail import send_mail
from django.db import models
from django.utils import six
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import GroupManager, BaseUserManager, AbstractBaseUser, PermissionManager


@python_2_unicode_compatible
class Permission(models.Model):

    name = models.CharField(_('name'), max_length=255)
    content_type = models.ForeignKey(ContentType, verbose_name=_('Content_type'), related_name='content_types')
    codename = models.CharField(_('codename'), max_length=100)
    display = models.BooleanField(_('show in front end'), default=False)
    objects = PermissionManager()

    class Meta:
        verbose_name = _('Access permission')
        verbose_name_plural = _('Access permissions')
        unique_together = (('content_type', 'codename'),)
        ordering = ('content_type__app_label', 'content_type__model',
                    'codename')

    def __str__(self):
        return "%s | %s | %s" % (
            six.text_type(self.content_type.app_label),
            six.text_type(self.content_type),
            six.text_type(self.name))

    def natural_key(self):
        return (self.codename,) + self.content_type.natural_key()
    natural_key.dependencies = ['contenttypes.contenttype']


@python_2_unicode_compatible
class Department(models.Model):

    name = models.CharField(_('name'), max_length=80, unique=True)
    permissions = models.ManyToManyField(Permission,
                                         verbose_name=_('Permissions'), blank=True)

    objects = GroupManager()

    class Meta:
        verbose_name = _('Department')
        verbose_name_plural = _('Departments')

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.name,)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, name=None, password=None):
        if not email:
            raise ValueError(_('email is required'))
        check_email = EmailValidator(message=_('please input a valid email'))
        check_email(email)
        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.name = name
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user


def _user_get_all_permissions(user, obj):
    permissions = set()
    for backend in auth.get_backends():
        if hasattr(backend, "get_all_permissions"):
            permissions.update(backend.get_all_permissions(user, obj))
    return permissions


def _user_has_perm(user, perm, obj):

    for backend in auth.get_backends():
        if not hasattr(backend, 'has_perm'):
            continue
        try:
            if backend.has_perm(user, perm, obj):
                return True
        except PermissionDenied:
            return False
    return False


def _user_has_module_perms(user, app_label):

    for backend in auth.get_backends():
        if not hasattr(backend, 'has_module_perms'):
            continue
        try:
            if backend.has_module_perms(user, app_label):
                return True
        except PermissionDenied:
            return False
    return False


class PermissionsMixin(models.Model):

    is_superuser = models.BooleanField(_('superuser status'), default=False,
                                       help_text=_('Designates that this user has all permissions without '
                                       'explicitly assigning them.'))
    departments = models.ManyToManyField(Department, verbose_name=_('Department'),
                                         blank=True, help_text=_('The departments this user belongs to. A user will '
                                                                 'get all permissions granted to each of '
                                                                 'their departments.'),
                                         related_name="user_set", related_query_name="user")
    user_permissions = models.ManyToManyField(Permission,
                                              verbose_name=_('User permissions'), blank=True,
                                              help_text=_('Specific permissions for this user.'),
                                              related_name="user_set", related_query_name="user")

    class Meta:
        abstract = True

    def get_department_permissions(self, obj=None):

        permissions = set()
        for backend in auth.get_backends():
            if hasattr(backend, "get_department_permissions"):
                permissions.update(backend.get_department_permissions(self, obj))
        return permissions

    def get_all_permissions(self, obj=None):
        return _user_get_all_permissions(self, obj)

    def has_perm(self, perm, obj=None):

        if self.is_active and self.is_superuser:
            return True

        return _user_has_perm(self, perm, obj)

    def has_perms(self, perm_list, obj=None):

        for perm in perm_list:
            if not self.has_perm(perm, obj):
                return False
        return True

    def has_module_perms(self, app_label):

        if self.is_active and self.is_superuser:
            return True

        return _user_has_module_perms(self, app_label)


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(
        verbose_name=_('Email'),
        max_length=255,
        unique=True, validators=[EmailValidator])
    name = models.CharField(max_length=20, blank=True, null=True, verbose_name=_('Name'))
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="must be digit")
    phone_number = models.CharField(validators=[phone_regex], blank=True, null=True,
                                    max_length=15, unique=True, verbose_name=_('Phone_number'))
    date_of_birth = models.DateField(blank=True, null=True, verbose_name=_('Date_of_birth'))
    is_active = models.BooleanField(default=False, verbose_name=_('is_active'))
    is_admin = models.BooleanField(default=False, verbose_name=_('is_admin'))
    user_image = ThumbnailerImageField(upload_to='user_photo', blank=True, null=True, verbose_name=_('User_photo'))
    image_height = models.PositiveIntegerField(null=True, blank=True, editable=False, default="50")
    image_width = models.PositiveIntegerField(null=True, blank=True, editable=False, default="50")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=_('created'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated'))
    objects = UserManager()
    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['date_of_birth']

    class Meta:
        verbose_name = _('Account')
        verbose_name_plural = _('Accounts')
        # unique_together = ('email', 'phone_number')

    def get_full_name(self):
        # The user is identified by their email address
        return self.name

    def get_short_name(self):
        # The user is identified by their email address
        return self.name

    def __unicode__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def user_thumbnail(self):
        if self.user_image:
            return u'<img src="%s" />' % (self.user_image.url)
        else:
            return u'<img src="/media/default.png" />'
    user_thumbnail.short_description = _('user_photo')
    user_thumbnail.allow_tags = True

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        if not self.user_image:
            return
        image = Image.open(self.user_image)
        # (width, height) = image.size
        size = (int(self.image_width), int(self.image_height))
        image = image.resize(size, Image.ANTIALIAS)
        image.save(self.user_image.path)

    def email_user(self, subject, message, from_email=None, **kwargs):

        send_mail(subject, message, from_email, [self.email], **kwargs)

    def get_first_department(self):
        try:
            department = self.departments.all()[0]
        except:
            department = ''
        return department

    def get_all_department(self):
        return Department.objects.all()

    def get_users_except_self(self):
        return User.objects.exclude(id=self.id)

