from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Category, Product

def product_list(request, category_id=None):
    sort = request.GET.get('sort', '-created')
    category_from_get = request.GET.get('category')
    
    # Use either the URL parameter or GET parameter for category
    category_id = category_id or category_from_get
    
    products = Product.objects.filter(available=True)
    
    if category_id:
        category = get_object_or_404(Category, id=category_id)
        products = products.filter(category=category)
    
    # Apply sorting
    if sort == 'price_low':
        products = products.order_by('price')
    elif sort == 'price_high':
        products = products.order_by('-price')
    elif sort == 'name':
        products = products.order_by('name')
    else:
        products = products.order_by('-created')
    
    # Pagination
    paginator = Paginator(products, 12)  # Show 12 products per page
    page = request.GET.get('page')
    products = paginator.get_page(page)
    
    categories = Category.objects.all()
    
    context = {
        'products': products,
        'categories': categories,
        'current_category': category_id,
        'current_sort': sort
    }
    return render(request, 'products/product_list.html', context)

def category_detail(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category, available=True)
    
    # Pagination
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    products = paginator.get_page(page)
    
    context = {
        'category': category,
        'products': products
    }
    return render(request, 'products/category_detail.html', context)

def product_detail(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug, available=True)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products
    }
    return render(request, 'products/product_detail.html', context)

def product_search(request):
    query = request.GET.get('q')
    products = []
    
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query),
            available=True
        ).distinct()
        
        # Pagination
        paginator = Paginator(products, 12)
        page = request.GET.get('page')
        products = paginator.get_page(page)
    
    context = {
        'query': query,
        'products': products
    }
    return render(request, 'products/search_results.html', context)
