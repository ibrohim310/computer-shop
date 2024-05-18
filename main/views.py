from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,logout
from main import models
from django.http import HttpResponseRedirect
import qrcode
from io import BytesIO
from django.core.files import File
from django.urls import reverse

@login_required(login_url='login')
def report(request):
    enter_records = models.Enter.objects.all()
    out_records = models.Out.objects.all()
    new_products = models.Product.objects.filter(is_new=True)  # Yangi mahsulotlarni filtrlang

    context = {
        'enter_records': enter_records,
        'out_records': out_records,
        'new_products': new_products,
    }
    return render(request, 'index.html', context)


#product
@login_required(login_url='login')
def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        quantity = int(request.POST.get('quantity'))
        price = float(request.POST.get('price'))

        # QR kod ma'lumotlarini yaratish
        qrcode_data = f"{name}, {category_id}, {price}"
        qrcode_img = qrcode.make(qrcode_data)
        
        # Tarangli fayl uchun BytesIO obyekti
        qr_code_io = BytesIO()
        
        # Faylga yozish
        qrcode_img.save(qr_code_io, format='PNG')
        
        # Faylni modellarga bog'lash
        qr_code_io.seek(0)
        qr_code = File(qr_code_io)
        
        # Yangi mahsulotni saqlash
        category = models.Category.objects.get(id=category_id)
        new_product = models.Product.objects.create(name=name, category=category, quantity=quantity, price=price, qr_image=qr_code)
        
        return redirect('list_product')
    categories = models.Category.objects.all()
    return render(request, 'product/create.html', {'categories': categories})


@login_required(login_url='login')
def update_product(request, product_id):
    product = models.Product.objects.get(id=product_id)
    if request.method == 'POST':
        name = request.POST['name']
        category_id = request.POST['category']
        quantity = int(request.POST['quantity'])
        price = float(request.POST['price'])
        
        # Kategoriya ma'lumotlarini olish
        category = models.Category.objects.get(id=category_id)
        
        # Ma'lumotlarni yangilash
        product.name = name
        product.category = category
        product.quantity = quantity
        product.price = price
        product.save()
        
        return redirect('list_product')
    
    categories = models.Category.objects.all()
    return render(request, 'product/update.html', {'product': product, 'categories': categories})

@login_required(login_url='login')
def delete_product(request, product_id):
    models.Product.objects.get(id=product_id).delete()
    return HttpResponseRedirect(reverse('list_product'))


@login_required(login_url='login')
def list_product(request):
    products = models.Product.objects.all()
    context = {'products': products}
    return render(request, 'product/list.html', context)

#category
@login_required(login_url='login')
def create_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            models.Category.objects.create(name=name)
            return redirect('list_category')
    return render(request, 'category/create.html')


@login_required(login_url='login')
def list_category(request):
    categories = models.Category.objects.all()
    return render(request, 'category/list.html', {'categories': categories})


@login_required(login_url='login')
def update_category(request, category_id):
    category = models.Category.objects.get(id=category_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            category.name = name
            category.save()
            return redirect('list_category')
    return render(request, 'category/update.html', {'category': category})


@login_required(login_url='login')
def delete_category(request, category_id):
    models.Category.objects.get(id=category_id).delete()
    return HttpResponseRedirect(reverse('list_category'))


#enter
@login_required(login_url='login')
def enter_list(request):
    # Barcha kirishlar ro'yxatini olish
    enters = models.Enter.objects.all()
    return render(request, 'enter/list.html', {'enters': enters})


@login_required(login_url='login')
def enter_create(request):
    if request.method == 'POST':
        product_id = request.POST.get('product')
        quantity = int(request.POST.get('quantity'))
        product = models.Product.objects.get(id=product_id)
        models.Enter.objects.create(product=product, quantity=quantity)
        return redirect('enter_list')
    products = models.Product.objects.all()
    return render(request, 'enter/create.html', {'products': products})



#out

@login_required(login_url='login')
def sell_product(request):
    if request.method == 'POST':
        product_id = request.POST.get('product')
        quantity = int(request.POST.get('quantity'))

        product = models.Product.objects.get(id=product_id)
        models.Out.objects.create(product=product, quantity=quantity)
        product.quantity -= quantity
        product.save()

        return redirect('list_cell_product')
    products = models.Product.objects.all()
    return render(request, 'out/create.html', {'products': products})


@login_required(login_url='login')
def list_cell_product(request):
    products = models.Product.objects.all()
    return render(request, 'out/list.html', {'products': products})




#return

@login_required(login_url='login')
def return_product(request):
    if request.method == 'POST':
        product_id = request.POST.get('product')
        quantity = int(request.POST.get('quantity'))

        product = models.Product.objects.get(id=product_id)
        models.Return.objects.create(product=product, quantity=quantity)
        product.quantity += quantity
        product.save()

        return redirect('list_product')
    products = models.Product.objects.all()
    return render(request, 'return/create.html', {'products': products})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return redirect('login')
    return render(request, 'login.html')


@login_required(login_url='login')
def user_logout(request):
    logout(request)
    return redirect('login')

