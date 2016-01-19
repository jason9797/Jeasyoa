# -*- coding: utf-8 -*-
__author__ = 'jason_lee'
# from models import MyUser
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


class EmailOrNumberModelBackend(ModelBackend):

    def authenticate(self, username=None, password=None, **kwargs):

        usermodel = get_user_model()
        if '@' in username:
            user_name = {'email': username}
        else:
            user_name = {'phone_number': username}

        try:
            user = usermodel.objects.get(**user_name)
            if user.check_password(password):
                return user
        except usermodel.DoesNotExist:
            return None

    def get_user(self, user_id):
        usermodel = get_user_model()
        try:
            return usermodel.objects.get(pk=user_id)
        except usermodel.DoesNotExist:
            return None

