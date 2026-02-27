from django.urls import path

from . import views

urlpatterns = [
    # path('process/', views.pyment_process, name='pyment_process'),
    # path('call_back/', views.pyment_callback, name='pyment_callback'),
    path('process/', views.pyment_process_sandbox, name='pyment_process'),
    path('call_back/', views.pyment_callback_sandbox, name='pyment_callback'),
]
