from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name='index'),
    path('category/',views.category,name='category'),
    path('single-product/',views.single_product,name='single-product'),
    path('checkout/',views.checkout,name='checkout'),
    path('cart/',views.cart,name='cart'),
    path('blog/',views.blog,name='blog'),
    path('single-blog/',views.single_blog,name='single-blog'),
    path('tracking/',views.tracking,name='tracking'),
    path('elements/',views.elements,name='elements'),
    path('contact/',views.contact,name='contact'),
    path('signup/',views.signup,name='signup'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('profile/', views.profile, name='profile'),
    path('change-password/',views.change_password,name='change-password'),
    path('forgot-password/',views.forgot_password,name='forgot-password'),
    path('new-password/',views.new_password,name='new-password'),
    path('verify-otp/',views.verify_otp,name='verify-otp'),

]