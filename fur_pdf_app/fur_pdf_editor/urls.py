from django.urls import path
from . import views
from .views import *
from django.contrib.auth.views import LogoutView

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
    path('login1/', views.custom_login_view, name='login'),
    path('signup1/', views.signup_view, name='signup'),
    path('send-magic-link/', send_magic_link, name='send_magic_link'),
    path('verify-magic-link/<uidb64>/<token>/', verify_magic_link, name='verify_magic_link'),
    path('upgrade/', views.upgrade, name='upgrade'),
    path('contact-sales/', views.contact_sales, name='contact_sales'),
    path('profile/', views.profile_view, name='profile'),
    path('logout1/', LogoutView.as_view(next_page='login', http_method_names=['get', 'post']), name='logout'),
]
