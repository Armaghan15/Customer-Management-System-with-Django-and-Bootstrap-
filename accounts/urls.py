from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
	path('', views.home, name='home'),

	path('login/', views.loginPage, name='login'),
	path('register/', views.registerPage, name='register'),
	path('logout/', views.logoutPage, name='logout'),
	path('user/', views.userPage, name='user-page'),

	path('account/', views.accountSettings, name='account'),

	path('products/', views.products, name='products'),
	
	path('customer/<str:pk>/', views.customer, name="customer"),
	path('create_customer/', views.createCustomer, name='create_customer'),
	path('delete_customer/<str:pk>/', views.deleteCustomer, name='delete_customer'),
	path('create_customer_order/<str:pk>', views.createCustomerOrder, name='create_customer_order'),
	
	path('create_order/', views.createOrder, name='create_order'),
	path('update_order/<str:pk>', views.updateOrder, name='update_order'),
	path('delete_order/<str:pk>', views.deleteOrder, name='delete_order'),

	# View for submiting Email form
	path('reset_password/', auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"), name="reset_password"),

	# View for sending success message for recieving email
	path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"), name="password_reset_done"),

	# View for the link to password Reset Form in Email
	path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"), name='password_reset_confirm'),

	# View for sending message for successfullay changing the Password
	path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"), name='password_reset_complete'),

]