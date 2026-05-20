from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('about/',views.about,name='about'),
    path('market/',views.market,name='market'),
    path('login/',views.login_user,name='login'),
    path('logout/',views.logout_user,name='logout'),
    path('register/',views.register_user,name='register'),
    path('profile/', views.profile, name='profile'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('order/create/', views.create_order, name='create_order'),
    path('order/update/<int:order_id>/', views.update_order, name='update_order'),
    path('order/delete/<int:order_id>/', views.delete_order, name='delete_order'),
]
