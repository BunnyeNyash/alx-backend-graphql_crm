import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from django.db import transaction, IntegrityError
from django.core.exceptions import ValidationError
from .models import Customer, Product, Order
from .filters import CustomerFilter, ProductFilter, OrderFilter

# GraphQL Types
class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        fields = ('id', 'name', 'email', 'phone', 'created_at')

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'stock')

class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = ('id', 'customer', 'products', 'total_amount', 'order_date')

# Input Types
class CustomerInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone = graphene.String(required=False)

class ProductInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    price = graphene.Decimal(required=True)
    stock = graphene.Int(required=False, default_value=0)

class OrderInput(graphene.InputObjectType):
    customer_id = graphene.ID(required=True)
    product_ids = graphene.List(graphene.ID, required=True)
    order_date = graphene.DateTime(required=False)

# Mutations
class CreateCustomer(graphene.Mutation):
    class Arguments:
        input = CustomerInput(required=True)

    customer = graphene.Field(CustomerType)
    message = graphene.String()

    def mutate(self, info, input):
        try:
            customer = Customer(name=input.name, email=input.email, phone=input.phone)
            customer.clean()
            customer.save()
            return CreateCustomer(customer=customer, message="Customer created successfully")
        except IntegrityError:
            raise Exception("Email already exists")
        except ValidationError as e:
            raise Exception(str(e))
        except Exception as e:
            raise Exception(f"Error creating customer: {str(e)}")

class BulkCreateCustomers(graphene.Mutation):
    class Arguments:
        input = graphene.List(CustomerInput, required=True)

    customers = graphene.List(CustomerType)
    errors = graphene.List(graphene.String)

    def mutate(self, info, input):
        customers = []
        errors = []

        with transaction.atomic():
            for item in input:
                try:
                    customer = Customer(name=item.name, email=item.email, phone=item.phone)
                    customer.clean()
                    customer.save()
                    customers.append(customer)
                except (IntegrityError, ValidationError) as e:
                    errors.append(f"Failed to create customer {item.name}: {str(e)}")
                except Exception as e:
                    errors.append(f"Unexpected error for {item.name}: {str(e)}")

        return BulkCreateCustomers(customers=customers, errors=errors)

class CreateProduct(graphene.Mutation):
    class Arguments:
        input = ProductInput(required=True)

    product = graphene.Field(ProductType)

    def mutate(self, info, input):
        try:
            product = Product(name=input.name, price=input.price, stock=input.stock)
            product.clean()
            product.save()
            return CreateProduct(product=product)
        except ValidationError as e:
            raise Exception(str(e))
        except Exception as e:
            raise Exception(f"Error creating product: {str(e)}")

class CreateOrder(graphene.Mutation):
    class Arguments:
        input = OrderInput(required=True)

    order = graphene.Field(OrderType)

    def mutate(self, info, input):
        try:
            customer = Customer.objects.get(id=input.customer_id)
        except Customer.DoesNotExist:
            raise Exception("Invalid customer ID")

        if not input.product_ids:
            raise Exception("At least one product is required")
        products = Product.objects.filter(id__in=input.product_ids)
        if len(products) != len(input.product_ids):
            raise Exception("One or more product IDs are invalid")

        try:
            with transaction.atomic():
                order = Order(customer=customer)
                if input.order_date:
                    order.order_date = input.order_date
                order.save()
                order.products.set(products)
                order.save()  # Triggers total_amount calculation
                return CreateOrder(order=order)
        except Exception as e:
            raise Exception(f"Error creating order: {str(e)}")

# Query and Mutation Classes
class Query(graphene.ObjectType):
    hello = graphene.String()

    all_customers = DjangoFilterConnectionField(CustomerType, filterset_class=CustomerFilter)
    all_products = DjangoFilterConnectionField(ProductType, filterset_class=ProductFilter)
    all_orders = DjangoFilterConnectionField(OrderType, filterset_class=OrderFilter)

    def resolve_hello(self, info):
        return "Hello, GraphQL!"

    def resolve_all_customers(self, info, **kwargs):
        return Customer.objects.all()

    def resolve_all_products(self, info, **kwargs):
        return Product.objects.all()

    def resolve_all_orders(self, info, **kwargs):
        return Order.objects.all()
        
class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()
