from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

from .decorators import *
from .models import *
from .forms import *
from .filters import OrderFilter	
# Create your views here.


# Our User Registration Funtion
@unauthenticated_user
def registerPage(request):
	form = CreateUserForm()

	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')

			messages.success(request, f"An account for {username} has been created succesfully")
			return redirect('login')


	context = {'form': form}
	return render(request, 'accounts/register.html', context)



# Our Login Function
@unauthenticated_user
def loginPage(request):
	
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('/')
		else:
			messages.info(request, 'Username or Password incorrect')

	return render(request, 'accounts/login.html')


# Our Logout Function
def logoutPage(request):
	logout(request)
	return redirect('login')




# home function for the dashboard page
@login_required(login_url='login')
@admin_only
def home(request):
	# Grabbing all the components of the Order and Customer Models
	orders = Order.objects.all()
	customers = Customer.objects.all()

	total_customers = customers.count()
	total_orders = orders.count()
	orders_delivered = orders.filter(status='Delivered').count()
	orders_pending = orders.filter(status='Pending').count()


	# Creating a dictionary to assign a name to orders and customers for our front-end page
	context = {
		'orders': orders,
		'customers': customers,
		'total_customers': total_customers,
		'total_orders': total_orders,
		'orders_delivered': orders_delivered,
		'orders_pending': orders_pending
	}

	# Rendering our front-end page dashboard.html
	return render(request, 'accounts/dashboard.html', context)



# Funtion for displaying user information on our front-end
@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
	orders = request.user.customer.order_set.all()

	total_orders = orders.count()
	orders_delivered = orders.filter(status='Delivered').count()
	orders_pending = orders.filter(status='Pending').count()

	context = {
		'orders': orders,
		'total_orders': total_orders,
		'orders_delivered': orders_delivered,
		'orders_pending': orders_pending
	}
	return render(request, 'accounts/user.html', context)




# Function for the account settings of a customer
@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
	customer = request.user.customer
	form = CustomerForm(instance=customer)

	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES, instance=customer)
		if form.is_valid():
			form.save()
			return redirect('account')


	context = {'form': form, 'customer': customer}
	return render(request, 'accounts/account_settings.html', context)




# products function for our products page
@allowed_users(allowed_roles=['admin'])
@login_required(login_url='login')
def products(request):
	# Grabbing all the components of the Product Model
	products = Product.objects.all()

	# Creating a dictionary to assign a name to products for our front-end page
	context = {"products": products}

	return render(request, 'accounts/products.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk):
	customer = Customer.objects.get(id=pk)
	orders = customer.order_set.all()
	orders_count = orders.count()

	myFilter = OrderFilter(request.GET, queryset=orders)
	orders = myFilter.qs


	# Creating a dictionary to assign a name to customer for our front-end page
	context = {
		'customer': customer, 
		'orders': orders, 
		'orders_count': orders_count,
		'myFilter': myFilter
	}

	return render(request, 'accounts/customer.html', context)




#Funtion for creating a customer on our dashboard
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createCustomer(request):
	form = CustomerForm()

	if request.method == 'POST':
		form = CustomerForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form': form}
	return render(request, 'accounts/customer_form.html', context)



# Funtion for deleting/removing a customer on our user dashboard
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteCustomer(request, pk):
	customer = Customer.objects.get(id=pk)

	if request.method == 'POST':
		customer.delete()
		return redirect('/')

	context = {'customer': customer}
	return render(request, 'accounts/delete_customer.html', context)



# Funtion for creating order on our dashboard page
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request):
	order = Order.objects.all()
	form = OrderForm()

	if request.method == 'POST':
		form = OrderForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/')
	context = {'order': order, 'form': form}
	return render(request, 'accounts/order_form.html', context)



# Function for creating a order for a customer on that specific customer's profile page
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createCustomerOrder(request, pk):
	customer = Customer.objects.get(id=pk)
	form = OrderForm(initial={'customer': customer})

	if request.method == 'POST':
		form = OrderForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	
	return render(request, 'accounts/customer_order_form.html', context)





# Function for updating/editing a order on our dashboard
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):
	
	order = Order.objects.get(id=pk)
	form = OrderForm(instance=order)

	if request.method == 'POST':
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form': form, 'order': order}
	return render(request, 'accounts/update_order.html', context)




# Funtion for deleting a order on our dashboard
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
	
	order = Order.objects.get(id=pk)

	if request.method == 'POST':
		order.delete()
		return redirect('/')

	context = {'order': order}
	return render(request, 'accounts/delete_order.html', context)





