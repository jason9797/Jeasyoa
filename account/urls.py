from django.conf.urls import url
from views import AccountDetail, account_logout, account_login
urlpatterns = [
                url(r'detail/$', AccountDetail.as_view(), name='account_detail'),
                url(r'logout/$', account_logout, name="account_logout"),
                url(r'^login/$', account_login, name="account_login")
              ]
