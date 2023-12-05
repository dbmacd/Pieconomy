"""Pieconomy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from main import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('login', views.LogInView.as_view(), name='login'),
    path('logout', views.LogOutView.as_view(), name='logout'),
    path('calculator', views.calculator, name='calculator'),
    path('shop', views.ShopListView.as_view(), name='shop'),
    path('item-detail/<int:pk>', views.ShopItemDetailView.as_view(), name='item-detail'),
    path('item-add/<int:item_id>', views.add_order_item, name='item-add'),
    path('item-remove/<int:item_id>', views.remove_order_item, name='item-remove'),
    path('order/<int:pk>', views.OrderDetailView.as_view(), name='order'),
    path('order-complete/<int:order_id>', views.complete_order, name='order-complete'),
    path('order-reverse/<int:order_id>', views.reverse_order, name='order-reverse'),
    path('orders', views.OrderListView.as_view(), name='orders'),
    path('profile', views.UserProfileView.as_view(), name='user-profile'),
    path('register', views.register, name='register'),
    path('forgot-password', auth_views.PasswordResetView.as_view(), name='forgot-password'),
    path('password-change', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password-change', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password-reset', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset-done', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-complete', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
