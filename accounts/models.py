from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# The Customer Model
class Customer(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	phone = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, null=True)
	profile_pic = models.ImageField(null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)	

	# Function for displaying the customer with it's name
	def __str__(self):
		return self.name



# Tag for the order
class Tag(models.Model):
	name = models.CharField(max_length=200)

	# Function for displaying the tag with it's name
	def __str__(self):
		return self.name


# The Product Model
class Product(models.Model):
	
	# Tuples of choices for the category of the product
	CATEGORY = (
			('Indoor', 'Indoor'),
			('Outdoor', 'Outdoor'),
		)



	name = models.CharField(max_length=200, null=True)
	price = models.FloatField(null=True)
	category = models.CharField(max_length=200, null=True, choices=CATEGORY) 
	description = models.CharField(max_length=200, null=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	tag = models.ManyToManyField(Tag)

	# Function for displaying the product with it's name
	def __str__(self):
		return self.name


# The Order Model
class Order(models.Model):
	
	# Tuples of choices for order status
	STATUS = (
			('Pending', 'Pending'),
			('Out for delivery', 'Out for delivery'),
			('Delivered', 'Delivered'),
		)


	customer = models.ForeignKey(Customer, null=True, on_delete= models.SET_NULL) 
	product = models.ForeignKey(Product, null=True, on_delete= models.SET_NULL)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	status = models.CharField(max_length=200, null=True, choices=STATUS)


	def __str__(self):
		return f"{self.customer} has ordered a {self.product}"
