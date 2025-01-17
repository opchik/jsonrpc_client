from django.urls import path
from .views import JsonRpcView

urlpatterns = [
    path('', JsonRpcView.as_view(), name='jsonrpc'),
]