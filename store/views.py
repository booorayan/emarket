from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.hashers import check_password, make_password
from .models import Products, Category, Customer, Order
from django.views import View
from store.middlewares.auth import auth_middleware


# Create your views here.
class Index(View):

    def post(self, request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity-1
                else:
                    cart[product] = quantity+1
            else:
                cart[product] = 1
        else:
            cart = {product: 1}

        request.session['cart'] = cart
        print('cart', request.session['cart'])
        return redirect('homepage')

    def get(self, request):
        return HttpResponseRedirect(f'/store{request.get_full_path()[1:]}')


class Login(View):
    return_url = None

    def get(self, request):
        Login.return_url = request.GET.get('return_url')
        return render(request, '../templates/login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_message = None
        print(email, password)
        print(customer)
        if customer:
            flag = check_password(password, customer.password)
            # print(flag)
            if flag:
                request.session['customer'] = customer.id

                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url = None
                    return redirect('homepage')
            else:
                error_message = 'Invalid!!'
        else:
            error_message = 'Invalid!!!'

        print(email, password)
        return render(request, '../templates/login.html', {'error': error_message})


class Signup(View):
    def get(self, request):
        return render(request, '../templates/signup.html')

    def post(self, request):
        postData = request.POST
        first_name = postData.get('firstname')
        last_name = postData.get('lastname')
        phone = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')

        # validation
        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email
        }
        error_message = None

        customer = Customer(first_name=first_name, last_name=last_name,
                            phone=phone, email=email, password=password)
        error_message = self.validateCustomer(customer)

        if not error_message:
            print(first_name, last_name, phone, email, password)
            customer.password = make_password(customer.password)
            customer.register()
            return redirect('homepage')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request, '../templates/signup.html', data)

    def validateCustomer(self, customer):
        error_message = None
        if not customer.first_name:
            error_message = 'Please enter your first name!'
        elif len(customer.first_name) < 3:
            error_message = 'First name must be more than 3 characters long!'
        elif not customer.last_name:
            error_message = 'Please enter your last name'
        elif len(customer.last_name) < 3:
            error_message = 'Last name must be more than 3 characters long!'
        elif not customer.phone:
            error_message = 'Enter your phone number!'
        elif len(customer.phone) < 10:
            error_message = 'Phone number must be 10 characters long!!'
        elif len(customer.password) < 5:
            error_message = 'Password must contain 5 or more characters!!'
        elif len(customer.email) < 5:
            error_message = 'Email must be 5 characters long..'
        elif customer.isExists():
            error_message = 'Email address already exists..'

        # save
        return error_message


class Cart(View):
    def get(self, request):
        ids = list(request.session.get('cart').keys())
        products = Products.get_products_by_id(ids)
        print(products)
        return render(request, '../templates/cart.html', {'products': products})


class CheckOut(View):
    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        products = Products.get_products_by_id(list(cart.keys()))
        print(address, phone, customer, cart, products)

        for product in products:
            print(cart.get(str(product.id)))
            order = Order(customer=Customer(id=customer),
                          product=product, price=product.price,
                          address=address, phone=phone,
                          quantity=cart.get(str(product.id)))
            order.save()
        request.session['cart'] = {}
        return redirect('cart')


class OrderView(View):
    def get(self, request):
        customer = request.session.get('customer')
        orders = Order.get_orders_by_customer(customer)
        print(orders)
        return render(request, '../templates/orders.html', {'orders': orders})


def store(request):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
    products = None
    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')
    if categoryID:
        products = Products.get_all_products_by_categoryid(categoryID)
    else:
        products = Products.get_all_products()

    data = {'products': products, 'categories': categories}

    print('you are: ', request.session.get('email'))
    return render(request, '../templates/index.html', data)


def logout(request):
    request.session.clear()
    return redirect('login')
