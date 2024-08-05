from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.upload_code, name='upload_code'),  # Homepage
    path('review/<int:code_file_id>/', views.reviews_code, name='reviews_code'),
    path('accounts/', include('django.contrib.auth.urls')),  # Authentication URLs
    path('register/', views.register, name='register'),
]

