from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import MyPasswordChangeForm
urlpatterns = [
    path("password_sucess",views.password_sucess,name="password_sucess"),
    path("changepassword",views.PasswordChangeView.as_view(template_name='app/passwordchange.html'),name="changepassword"),
    # path("changepassword",auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html'),name="changepassword"),
    path("",views.ProductView.as_view(),name='home'),
    path('paymentdone',views.payment_done,name='paymentdone'),
    path('removecart',views.remove_cart,name='removecart'),
    path('minuscart',views.minus_cart,name='minuscart'),
    path('pluscart',views.plus_cart,name='pluscart'),
    path('cart',views.show_cart,name="show_cart"),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('add-to-cart', views.add_to_cart, name='add-to-cart'),
    path('buy', views.buy_now, name='buy'),
    path('profile', views.ProfileView.as_view(), name='profile'),
    path('address', views.address, name='address'),
    path('orders', views.orders, name='orders'),
    # path('changepassword', views.change_password, name='changepassword'),
    path('men-acc', views.men_acc, name='men_acc'),
    path('women-acc', views.women_acc, name='women_acc'),
    path('men-topwear', views.men_top, name='men_top'),
    path('men-bottomwear', views.men_bottom, name='men_bottom'),
    path('men-topwear/<data>', views.men_top, name='men_top'),
    path('men-bottomwear/<data>', views.men_bottom, name='men_bottom'),
    path('women-indian/<data>', views.women_indian, name='women_indian'),
    path('women-western/<data>', views.women_western, name='women_western'),
    path('women-indian', views.women_indian, name='women_indian'),
    path('women-western', views.women_western, name='women_western'),
    path('login', views.signin, name='login'),
    # path('registration/', views.customerregistration, name='registration'),
    path('raiserequest',views.raiserequest,name='raiserequest'),
    path('register', views.register, name="register"),
    path('checkout', views.checkout, name='checkout'),
    path('logout',views.signout,name='logout'),
path('activate/<uidb64>/<token>',views.activate,name='activate'),
    path('passwordchange',auth_views.PasswordChangeView.as_view(template_name ='app/passwordchange.html',form_class=MyPasswordChangeForm),name='passwordchange'),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


