"""
URL configuration for ALORA project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('register/',views.user_register,name='register'),
    path('home/',views.home,name='home'),
    path('login/',views.user_login,name='login'),
    path('logout/',views.user_logout,name='logout'),
    path('profile/',views.user_profile,name='profile'),
    path('update/',views.update_profile,name='update'),

    path('admin_dash/',views.admin_dash,name='admin_dash'),
    path('view_users/',views.view_users,name='view_users'),
    path('hall_details/',views.hall_details,name='hall_details'),
    path('add_hall/',views.add_hall,name='add_hall'),
    path('food_details/',views.food_details,name='food_details'),
    path('add_food/',views.add_food,name='add_food'),
    path('decoration_details/',views.decoration_details,name='decoration_details'),
    path('add_decoration',views.add_decoration,name='add_decoration'),
    path('adminviewbooking/',views.admin_view_booking,name='admin_view_booking'),
    path('adminacceptreject/<int:id>/',views.accept_reject_booking,name='acceptrejectbooking'),


    path('resetpassword',views.password_reset_request,name='resetpassword'),
    path('verifyotp',views.verify_otp,name='verifyotp'),
    path('newpassword',views.set_new_password,name='newpassword'),

    path('booking_page',views.booking_page,name='booking_page'),
    path('booking_view',views.booking_view,name='booking_view'),
    path('view_bookings',views.view_bookings,name='view_bookings'),

    path('stripe_payments/<int:id>',views.stripe_payments,name='stripe_payments'),
    path('payment_status/<int:id>/',views.payment_status, name='payment_status'),

    path('service',views.service,name='service'),
    path('aboutus',views.aboutus,name='aboutus'),
    path('gallery',views.gallery,name='gallery'),
    path('testimonial',views.testimonial,name='testimonial'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) 
