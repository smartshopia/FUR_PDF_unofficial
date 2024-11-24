from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('upload/', views.upload_pdf, name='upload_pdf'),
    path('list/', views.pdf_list, name='pdf_list'),
    path('view/<int:pdf_id>/', views.view_pdf, name='view_pdf'),
    path('tail/', views.tailwind, name='tailwind'),
    path('boot/', views.boot, name='tailwin9d'),
    path('features/', views.features, name='features'),
    path('pricing/', views.pricing, name='pricing'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
]
