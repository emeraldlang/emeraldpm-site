from django.urls import path

from .. import views


app_name = 'accounts'

urlpatterns = [
    path('create-token/', views.CreateTokenView.as_view(), name='create_token'),
]
