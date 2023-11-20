import time
from typing import Any
# from django.db.models.query import _BaseQuerySet
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from .models import *
from core.forms import ContactForm
from django.views.generic import ListView, DetailView
from django.db.models import Q

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import jaccard_score
from decimal import Decimal
from random import shuffle
from django.shortcuts import get_object_or_404
from core.context_processors.context_processors import settings


# Create your views here.
def login(request):
    return render(request, 'login.html') 


def index(request):
    userinput = request.GET.get('search')
    if userinput:
        product = Clothes.objects.filter(Q(name__icontains=userinput) | Q(description__icontains=userinput))
        count = product.count()
    else:
        product = Clothes.objects.all()
        count = product.count()
    
    context = {
        'product': product,
        'count': count,
        'userinput': userinput if userinput is not None else '',
    }
    print('context: ', context)
    return render(request, 'index.html', context)


# class ClothesList(ListView):
#     model = Clothes
#     template_name = 'index.html'
#     context_object_name = 'product'
#     ordering = ['create_time']
#     paginate_by = 1

#     def get_context_data(self, **kwargs: Any):
#         context = super().get_context_data(**kwargs)
#         context['count'] = Clothes.objects.filter(active=True).count()
#         return context
    
#     def get_paginate_by(self, queryset):
#         paginate_by = self.request.GET.get('page')
#         if paginate_by:
#             return paginate_by
#         return self.paginate_by


def home2(request):
    context = {
        'product': Clothes.objects.all().filter(active=True)
    }
    return render(request, 'home-02.html', context)


def home3(request):
    context = {
        'product': Clothes.objects.all().filter(active=True)
    }
    return render(request, 'home-03.html', context)


def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Clothes, id=product_id)
        quantity = request.POST.get('quantity', 1)
        size = request.POST.get('size', '')
        color = request.POST.get('color', '')
        
        existing_item = CartProduct.objects.filter(
            product=product,
            size=size,
            color=color,
        ).first()

        if existing_item:
            existing_item.quantity += int(quantity)
            existing_item.save()
        else:
            CartProduct.objects.create(
                product=product,
                quantity=int(quantity),
                size=size,
                color=color,
            )
    return HttpResponse(status=204)


def update_quantity(request, product_id, quantity):
    if request.method == 'POST':
        print('post:', product_id, quantity)
        # product = get_object_or_404(CartProduct, id=product_id)
        # if product:
        #     product.quantity = int(quantity)
        #     product.save()

    return HttpResponse(status=204)
    


def single_product(request, slug):
    product = Clothes.objects.get(slug=slug)
    
    related_product = Clothes.objects.filter(category__category = product.category).exclude(pk=product.pk)

    sizes = product.size.all()
    colors = product.color.all()
    
    context = {
        'product': product,
        'sizes': sizes,
        'colors': colors,
        'related_product': related_product,
    }
    return render(request, 'product-detail.html', context)


def contact(request):
    context = {
        'contact': ContactForm()
    }
    if request.method == 'POST':
        result = ContactForm(request.POST)
        if result.is_valid():
            result.save()
        else:
            print(result.errors)
    return render(request, 'contact.html', context)


def blog(request):
    return render(request, 'blog.html')

def blog_detail(request):
    return render(request, 'blog-detail.html')


def general_search(request):
    userinput = request.GET.get('general-search')
    if userinput:
        keywords = userinput.split()
        search_query = Q()
        for keyword in keywords:
            search_query |= Q(name__icontains=keyword) or Q(description__icontains=keyword)
        products = Clothes.objects.filter(search_query)

        context = {
            'products': products,
        }
        return render(request, 'search-results.html', context)
    return render(request, 'search-results.html')


def product(request):
    userinput = request.GET.get('search')
    if userinput:
        # product = Clothes.objects.filter(Q(name__icontains=userinput) | Q(description__icontains=userinput))
        keywords = userinput.split()
        search_query = Q()
        for keyword in keywords:
            search_query |= Q(name__icontains=keyword) or Q(description__icontains=keyword)
        product = Clothes.objects.filter(search_query)
        
        # ---------------------------------------------------------------
        # ---------------------------------------------------------------
        # search_terms = ' '.join(userinput.split())
        # print('search_terms: ', search_terms)

        # products = Clothes.objects.filter(active=True)
        # product_texts = [
        #     f"{product.name} {product.description.replace('<p>', '').replace('</p>', '').replace('<strong>', '').replace('</strong>', '').replace('<u>', '').replace('</u>', '').replace('<s>', '').replace('</s>', '')}"
        #     for product in products
        # ]
        # print('product_texts: ', product_texts)

        # vectorizer = CountVectorizer()
        # product_vectors = vectorizer.fit_transform(product_texts)
        # print('product_vectors: ', product_vectors)

        # query_vector = vectorizer.transform([search_terms])
        # print('query_vector: ', query_vector)

        # print("query_vector shape: ", query_vector.shape)
        # print("product_vectors shape: ", product_vectors.shape)

        
        # # similarity_scores = cosine_similarity(query_vector, product_vectors).flatten()
        # similarity_scores = cosine_similarity(query_vector, product_vectors).flatten()
        # print('similarity_scores: ', similarity_scores)

        # similarity_threshold = 0.1

        # relevant_indices = [index for index, score in enumerate(similarity_scores) if score > similarity_threshold]  #  if score > similarity_threshold

        # product = [products[index] for index in relevant_indices]

    else:
        product = Clothes.objects.all()

    category = request.GET.get('category')

    sort_by = request.GET.get('sort_by')

    price = request.GET.get('price')

    color = request.GET.get('color')

    tag = request.GET.get('tag')

    # category
    if category is not None and category != 'all':
        if category == 'accessories':
            categories = ['Bags', 'Watches', 'Shoes']
            product = product.filter(category__category__in = categories)
        else:
            product = product.filter(category__category=str(category).title())
    
    # sort_by
    if sort_by is not None:
        if str(sort_by) == 'hightolow':
            product = product.order_by('-price')
        elif str(sort_by) == 'lowtohigh':
            product = product.order_by('price')
        elif str(sort_by) == 'newness':
            product = product.order_by('-update_time')
        elif str(sort_by) == 'rating':
            product_list = list(product)
            shuffle(product_list)
        elif str(sort_by) == 'popularity':
            product_list = list(product)
            shuffle(product_list)
        else:
            product = product

    # price                  
    if price is not None and price != 'all':
        if 'gte' not in str(price):
            price_gte = Decimal(str(price).split('-')[0].replace('$', ''))
            price_lte = Decimal(str(price).split('-')[1].replace('$', ''))
            product = product.filter(price__range=(price_gte, price_lte))
        else:
            price_gte = Decimal(str(price).split('$')[1])
            product = product.filter(price__gte=price_gte)

    # color
    if color is not None:
        selected_color = Colors.objects.filter(color__in=[str(color).title()])
        product = product.filter(color__in=selected_color)

    # tag
    if tag is not None:
        selected_tag = Tags.objects.filter(tag__in=[str(tag).title()])
        product = product.filter(tag__in=selected_tag)
  
    context = {
        'product': product,
        'search': userinput if userinput != '' and userinput is not None else None,
        'sort_by': sort_by if sort_by != '' and sort_by is not None else None,
        'price': price if price != '' and price is not None else None,
        'color': color if color != '' and color is not None else None,
        'tag': tag if tag != '' and tag is not None else None,
        'category': category if category != '' and category is not None else None,
    }
        
    return render(request, 'product.html', context)

def about(request):
    return render(request, 'about.html')

def features(request):
    products = CartProduct.objects.all() 

    context = {
        'products': products if products else None,
        'error_message': 'There are no products yet...',
    }
    return render(request, 'shoping-cart.html', context)

