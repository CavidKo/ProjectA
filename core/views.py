from datetime import datetime
from random import shuffle
import time
from typing import Any
# from django.db.models.query import _BaseQuerySet
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from requests import request
from .models import *
from core.forms import ContactForm
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.utils import translation

# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
# from sklearn.metrics import jaccard_score
from decimal import Decimal
from random import shuffle
from django.shortcuts import get_object_or_404
from core.context_processors.context_processors import settings



month_mapping = {
    'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4,
    'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8,
    'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12,
}


# Create your views here.
def login(request):
    return render(request, 'login.html') 


def index(request, page_count = 1):
    end_index = (page_count - 1) * 3
    more_items = True if 6 + end_index < Clothes.objects.count() else False

    userinput = request.GET.get('search')
    if userinput:
        product = Clothes.objects.filter(Q(name__icontains=userinput) | Q(description__icontains=userinput))
        more_items = False
    else:
        product = Clothes.objects.all()
        
    category = request.GET.get('category')
    # category
    if category is not None and category != 'all' and category != 'hamısı':
        product = product.filter(category__category=str(category).title())
        more_items = False

    sort_by = request.GET.get('sort_by')
    # sort_by
    if sort_by:
        more_items = False
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

    
    price = request.GET.get('price')    
    # price                  
    if price and price != 'all' and price != 'hamısı':
        more_items = False
        if 'gte' not in str(price):
            price_gte = Decimal(str(price).split('-')[0].replace('$', ''))
            price_lte = Decimal(str(price).split('-')[1].replace('$', ''))
            product = product.filter(price__range=(price_gte, price_lte))
        else:
            price_gte = Decimal(str(price).split('$')[1])
            product = product.filter(price__gte=price_gte)

    color = request.GET.get('color')
    # color
    if color:
        more_items = False
        selected_color = Colors.objects.filter(color__in=[str(color).title()])
        product = product.filter(color__in=selected_color)

    tag = request.GET.get('tag')
    # tag
    if tag:
        more_items = False
        if '-' not in tag:
            selected_tag = Tags.objects.filter(tag__in=[str(tag).title()])
        else:
            selected_tag = Tags.objects.filter(tag__in=[str(tag).replace('-', ' ').capitalize()])
        # selected_tag = Tags.objects.filter(tag__in=[str(tag).title()])
        product = product.filter(tag__in=selected_tag)

    product = product[: 6 + end_index]
    
    context = {
        'products': product,
        'userinput': userinput if userinput is not None else '',
        'search': userinput,
        'sort_by': sort_by,
        'price': price,
        'color': color,
        'tag': tag,
        'page_count': int(page_count) + 1 if page_count else 2,
        'more_items': more_items,
    }
    return render(request, 'index.html', context)


def home2(request):
    blogs = Blog.objects.all()          
    about = About.objects.first()

    context = {
        'products': Clothes.objects.all().filter(active=True),
        'blogs': blogs,
        'aboutus': about.our_story_text,
        'gallery_images': CozaStoreGallery.objects.all()
    }
    return render(request, 'home-02.html', context)


# class Home3List(ListView):
#     model = Clothes
#     template_name = 'home-03.html'
#     context_object_name = 'products'
#     ordering = ['-create_time']
#     paginate_by = 4

#     def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
#         context = super().get_context_data(**kwargs)

#         about = About.objects.first()
#         context['aboutus'] = about.our_story_text
#         context['gallery_images']: CozaStoreGallery.objects.all()

#         search = self.request.GET.get('search')
#         if search:
#             keywords = search.split()
#             query = Q()
#             for keyword in keywords:
#                 query |= Q(name__icontains=keyword) or Q(description__icontains=keyword)
#             context['products'] = Clothes.objects.filter(query).all()
#             context['search'] = search


#         category = self.request.GET.get('category')
#         if category and category != 'all':
#             if '-' in category:
#                 splitted_category = category.split('-')
#                 query = Q(category__icontains=splitted_category[0]) or Q(category__icontains=splitted_category[1])
#                 selected_category = Categories.objects.filter(query)
#                 context['products'] = context['products'].filter(categories__in=selected_category).all()
#             else:
#                 selected_category = Categories.objects.filter(category__in=[str(category).title()])
#                 context['products'] = context['products'].filter(category__in=selected_category).all()
#             context['category'] = category
        
#         return context
        
#     def get_paginate_by(self, queryset):
#         return self.paginate_by



def add_to_cart(request, product_id):
    current_language = 'az' if translation.get_language() == 'en' else 'en'
    if request.method == 'POST':
        product = get_object_or_404(Clothes, id=product_id)
        quantity = request.POST.get('quantity', 1)
        size = request.POST.get('size', '')
        color = request.POST.get('color', '')

        en_az_size = Sizes.objects.filter(size=size).first()
        with translation.override(current_language):
            translated_size = en_az_size.size
    
        en_az_color = Colors.objects.filter(color=color).first()
        with translation.override(current_language):
            translated_color = en_az_color.color

        
        existing_item = CartProduct.objects.filter(
            product__id=product_id,
            size=size,
            color=color,
            active=True
        ).first()

        if existing_item:
            existing_item.quantity += int(quantity)
            existing_item.save()

        else:
            if translation.get_language() == 'en':
                CartProduct.objects.create(
                    product=product,
                    quantity=int(quantity),
                    size_en=size, 
                    size_az=translated_size,
                    color_en=color, 
                    color_az=translated_color,
                    active=True
                )
            else:
                CartProduct.objects.create(
                    product=product,
                    quantity=int(quantity),
                    size_en=translated_size, 
                    size_az=size,
                    color_en=translated_color, 
                    color_az=color,
                    active=True
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

    reviews = Reviews.objects.filter(product=product).all()
    
    context = {
        'product': product,
        'sizes': sizes,
        'colors': colors,
        'related_product': related_product,
        'reviews': reviews,
        'review_count': reviews.count()
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

class BlogList(ListView):
    model = Blog
    template_name = 'blog.html'
    context_object_name = 'blogs'
    ordering = ['-create_time']
    paginate_by = 3

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context['count'] = Blog.objects.all().count()
        context['categories'] = BlogCategories.objects.all()
        context['tags'] = Tags.objects.all()

        all_models = list(Clothes.objects.all())
        shuffle(all_models)
        context['chosen_models'] = all_models[:5]

        search = self.request.GET.get('search')
        if search:
            keywords = search.split()
            query = Q()
            for keyword in keywords:
                query |= Q(name__icontains=keyword) or Q(description__icontains=keyword)
            context['blogs'] = Blog.objects.filter(query).all()
            context['search'] = search

        category = self.request.GET.get('category')
        if category:
            if '-' in category:
                splitted_category = category.split('-')
                query = Q(category__icontains=splitted_category[0]) or Q(category__icontains=splitted_category[1])
                selected_category = BlogCategories.objects.filter(query)
                context['blogs'] = Blog.objects.filter(categories__in=selected_category).all()
            else:
                selected_category = BlogCategories.objects.filter(category__in=[str(category).title()])
                context['blogs'] = Blog.objects.filter(categories__in=selected_category).all()
            context['category'] = category

        archive = self.request.GET.get('archive')
        if archive:
            month = archive.split('-')[0].title()
            filtered_blogs = Blog.objects.filter(create_time__month=month_mapping[month]).all()
            context['blogs'] = filtered_blogs
            context['archive'] = archive
        
        tag = self.request.GET.get('tag')
        if tag:
            selected_tag = Tags.objects.filter(tag__icontains=tag)
            context['blogs'] = Blog.objects.filter(tags__in=selected_tag).all()
            context['tag'] = tag

        context['archive_dates_and_counts'] = []
        for blog in context['blogs']:
            original_datetime_str = str(blog.create_time)
            original_datetime = datetime.fromisoformat(original_datetime_str)
            blog.create_time = original_datetime.strftime("%d %b %Y")
            blog.create_time = [str(blog.create_time).split()[0], ' '.join(str(blog.create_time).split()[1:])]
            
            blog_month_number = month_mapping[blog.create_time[1].split()[0]]
            blog_year = int(blog.create_time[1].split()[1])

            blog_count = Blog.objects.filter(
                Q(create_time__month=blog_month_number) &
                Q(create_time__year=blog_year)
            ).count()

            to_append = [blog.create_time[1], blog_count]
            if to_append not in context['archive_dates_and_counts']:
                context['archive_dates_and_counts'].append(to_append)

        return context

    def get_paginate_by(self, queryset):
        return self.paginate_by


def blog_detail(request, id_):
    detailed_blog = Blog.objects.get(id=id_)

    original_datetime_str = str(detailed_blog.create_time)
    original_datetime = datetime.fromisoformat(original_datetime_str)
    detailed_blog.create_time = original_datetime.strftime("%d %b %Y")
    detailed_blog.create_time = [str(detailed_blog.create_time).split()[0], str(detailed_blog.create_time).split()[1], str(detailed_blog.create_time).split()[2]]

    all_models = list(Clothes.objects.all())
    shuffle(all_models)

    archive_dates_and_counts = []
    for blog in Blog.objects.all():
            original_datetime_str = str(blog.create_time)
            original_datetime = datetime.fromisoformat(original_datetime_str)
            blog.create_time = original_datetime.strftime("%d %b %Y")
            blog.create_time = [str(blog.create_time).split()[0], ' '.join(str(blog.create_time).split()[1:])]
            
            blog_month_number = month_mapping[blog.create_time[1].split()[0]]
            blog_year = int(blog.create_time[1].split()[1])

            blog_count = Blog.objects.filter(
                Q(create_time__month=blog_month_number) &
                Q(create_time__year=blog_year)
            ).count()

            to_append = [blog.create_time[1], blog_count]
            if to_append not in archive_dates_and_counts:
                archive_dates_and_counts.append(to_append)

    context = {
        'blog': detailed_blog,
        'categories': BlogCategories.objects.all(),
        'tags': Tags.objects.all(),
        'chosen_models': all_models[:5],
        'archive_dates_and_counts': archive_dates_and_counts
    }
    return render(request, 'blog-detail.html', context)


def general_search(request):
    userinput = request.GET.get('general-search')
    if userinput:
        keywords = userinput.split()
        search_query = Q()
        # query = Q()
        for keyword in keywords:
            search_query |= Q(name__icontains=keyword) | Q(description__icontains=keyword)
            # query |= Q(name__icontains=keyword) or  Q(description__icontains=keyword)

        blogs = Blog.objects.filter(search_query)
        products = Clothes.objects.filter(search_query)

        for blog in blogs:
            original_datetime_str = str(blog.create_time)
            original_datetime = datetime.fromisoformat(original_datetime_str)
            blog.create_time = original_datetime.strftime("%d %b %Y")
            blog.create_time = [str(blog.create_time).split()[0], ' '.join(str(blog.create_time).split()[1:])]

        context = {
            'products': products,
            'blogs': blogs,
        }
        return render(request, 'search-results.html', context)
    return render(request, 'search-results.html')


def home3(request, page_count = 1):
    about = About.objects.first()

    end_index = (page_count - 1) * 3
    more_items = True if 6 + end_index < Clothes.objects.count() else False

    userinput = request.GET.get('search')
    if userinput:
        more_items = False
        keywords = userinput.split()
        search_query = Q()
        for keyword in keywords:
            search_query |= Q(name__icontains=keyword) or Q(description__icontains=keyword)
        product = Clothes.objects.filter(search_query)
    else:
        product = Clothes.objects.all()

    category = request.GET.get('category')

    sort_by = request.GET.get('sort_by')

    price = request.GET.get('price')

    color = request.GET.get('color')

    tag = request.GET.get('tag')

    # category
    if category is not None and category != 'all':
        more_items = False
        if category == 'accessories':
            categories = ['Bags', 'Watches', 'Shoes']
            product = product.filter(category__category__in = categories)
        else:
            product = product.filter(category__category=str(category).title())
    
    # sort_by
    if sort_by is not None:
        more_items = False
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
    if price is not None and price != 'all' and price != 'hamısı':
        more_items = False
        if 'gte' not in str(price):
            price_gte = Decimal(str(price).split('-')[0].replace('$', ''))
            price_lte = Decimal(str(price).split('-')[1].replace('$', ''))
            product = product.filter(price__range=(price_gte, price_lte))
        else:
            price_gte = Decimal(str(price).split('$')[1])
            product = product.filter(price__gte=price_gte)

    # color
    if color is not None:
        more_items = False
        selected_color = Colors.objects.filter(color__in=[str(color).title()])
        product = product.filter(color__in=selected_color)

    # tag
    if tag is not None:
        more_items = False
        if '-' not in tag:
            selected_tag = Tags.objects.filter(tag__in=[str(tag).title()])
        else:
            selected_tag = Tags.objects.filter(tag__in=[str(tag).replace('-', ' ').capitalize()])
        # selected_tag = Tags.objects.filter(tag__in=[str(tag).title()])
        product = product.filter(tag__in=selected_tag)
    
    context = {
        'products': product[: 6 + end_index],
        'search': userinput if userinput != '' and userinput is not None else None,
        'sort_by': sort_by if sort_by != '' and sort_by is not None else None,
        'price': price if price != '' and price is not None else None,
        'color': color if color != '' and color is not None else None,
        'tag': tag if tag != '' and tag is not None else None,
        'category': category if category != '' and category is not None else None,
        'aboutus': about.our_story_text,
        'gallery_images': CozaStoreGallery.objects.all(),
        'page_count': int(page_count) + 1 if page_count else 2,
        'more_items': more_items,
    }

    return render(request, 'home-03.html', context)


def product(request, page_count = 1):
    end_index = (page_count - 1) * 3
    more_items = True if 6 + end_index < Clothes.objects.count() else False

    userinput = request.GET.get('search')
    if userinput:
        more_items = False
        keywords = userinput.split()
        search_query = Q()
        for keyword in keywords:
            search_query |= Q(name__icontains=keyword) or Q(description__icontains=keyword)
        product = Clothes.objects.filter(search_query)

    else:
        product = Clothes.objects.all()

    category = request.GET.get('category')

    sort_by = request.GET.get('sort_by')

    price = request.GET.get('price')

    color = request.GET.get('color')

    tag = request.GET.get('tag')

    # category
    if category is not None and category != 'all' and category != 'hamısı':
        more_items = False
        if category == 'accessories' or category == 'aksesuarlar':
            categories = ['Bags', 'Watches', 'Shoes', 'Çantalar', 'Saatlar', 'Ayaqqabılar']
            product = product.filter(category__category__in = categories)
        else:
            product = product.filter(category__category=str(category).title())
    
    # sort_by
    if sort_by is not None:
        more_items = False
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
        more_items = False
        if 'gte' not in str(price):
            price_gte = Decimal(str(price).split('-')[0].replace('$', ''))
            price_lte = Decimal(str(price).split('-')[1].replace('$', ''))
            product = product.filter(price__range=(price_gte, price_lte))
        else:
            price_gte = Decimal(str(price).split('$')[1])
            product = product.filter(price__gte=price_gte)

    # color
    if color is not None:
        more_items = False
        selected_color = Colors.objects.filter(color__in=[str(color).title()])
        product = product.filter(color__in=selected_color)

    # tag
    if tag is not None:
        more_items = False
        if '-' not in tag:
            selected_tag = Tags.objects.filter(tag__in=[str(tag).title()])
        else:
            selected_tag = Tags.objects.filter(tag__in=[str(tag).replace('-', ' ').capitalize()])
        product = product.filter(tag__in=selected_tag)

    
    product = product[: 6 + end_index]
    
    context = {
        'product': product,
        'search': userinput if userinput != '' and userinput is not None else None,
        'sort_by': sort_by if sort_by != '' and sort_by is not None else None,
        'price': price if price != '' and price is not None else None,
        'color': color if color != '' and color is not None else None,
        'tag': tag if tag != '' and tag is not None else None,
        'category': category if category != '' and category is not None else None,
        'page_count': int(page_count) + 1 if page_count else 2,
        'more_items': more_items,
    }
        
    return render(request, 'product.html', context)

def about(request):
    context = {
        'about': About.objects.all()
    }
    print(context)
    return render(request, 'about.html', context)


def features(request):
    button = request.GET.get('button_clicked')
    if button == 'update_cart':
        quantities_of_products = request.GET.getlist('num-product1')

        if quantities_of_products:
            for product, related_quantity in zip(CartProduct.objects.filter(active = True), quantities_of_products):
                if int(related_quantity) == 0:
                    print('RELATED QUANTITY IS ZEROOO')
                    product.quantity = 0
                    product.active = False
                    product.save() 

                elif int(product.quantity) != int(related_quantity):
                    product.quantity = int(related_quantity)
                    product.save()

    elif button == 'proceed_to_checkout':
        for product in CartProduct.objects.filter(active=True):
            product.active = False
            product.save()

    products = CartProduct.objects.filter(active=True)
    context = {
        'products': products if products else None,
        'error_message': 'There are no products yet...',
    }
    return render(request, 'shoping-cart.html', context)


def change_whish(request, product_id):
    product = Clothes.objects.filter(id=product_id).first()
    if product.added_to_whishlist is False:
        product.added_to_whishlist = True
    else:
        product.added_to_whishlist=False
    product.save()

    return JsonResponse(
        {
            'added_to_wishlist': product.added_to_whishlist
        }, status=200
    )


def add_review(request, product_id):
    product = Clothes.objects.filter(Q(id=int(product_id)) & Q(active=True)).first()

    if request.method == 'GET':
        rating = request.GET.get('rating')
        message = request.GET.get('review')
        name = request.GET.get('name')
        email = request.GET.get('email')

        if rating:
            product.rating = round((product.rating + int(rating)) / 2, 0)
            product.save()

        review = Reviews.objects.filter(
            Q(product=product) & Q(rating=rating) & Q(message=message) & Q(name=name) & Q(email=email)
        ).first()

        if not review:
            Reviews.objects.create(
                product=product,
                rating=int(rating),
                message=message,
                name=name,
                email=email
            )
        else:
            review.rating = rating
            review.name = name
            review.message = message
            review.email = email
    
    related_product = Clothes.objects.filter(category__category = product.category).exclude(pk=product.pk)

    sizes = product.size.all()
    colors = product.color.all()

    reviews = Reviews.objects.filter(product=product).all()
    
    context = {
        'product': product,
        'sizes': sizes,
        'colors': colors,
        'related_product': related_product,
        'reviews': reviews,
        'review_count': reviews.count()
    }
    return render(request, 'product-detail.html', context)


def add_blog_comment(request, blog_id):
    detailed_blog = Blog.objects.filter(id=blog_id).first()

    if request.method == 'GET':
        comment = request.GET.get('cmt')
        name = request.GET.get('name')
        email = request.GET.get('email')
        website = request.GET.get('web')

        if name and comment and email:
            blog_comment = BlogComments.objects.filter(
                Q(blog=detailed_blog) & Q(name=name) & Q(email=email) & Q(message=comment)
            ).first()

            detailed_blog.comment_count += 1
            detailed_blog.save()

            if not blog_comment:
                BlogComments.objects.create(
                    blog=detailed_blog,
                    message=comment,
                    name=name,
                    email=email,
                    website=website
                )
            else:
                blog_comment.name = name
                blog_comment.message = comment
                blog_comment.email = email
                blog_comment.website = website

    original_datetime_str = str(detailed_blog.create_time)
    original_datetime = datetime.fromisoformat(original_datetime_str)
    detailed_blog.create_time = original_datetime.strftime("%d %b %Y")
    detailed_blog.create_time = [str(detailed_blog.create_time).split()[0], str(detailed_blog.create_time).split()[1], str(detailed_blog.create_time).split()[2]]

    all_models = list(Clothes.objects.all())
    shuffle(all_models)

    archive_dates_and_counts = []
    for blog in Blog.objects.all():
        original_datetime_str = str(blog.create_time)
        original_datetime = datetime.fromisoformat(original_datetime_str)
        blog.create_time = original_datetime.strftime("%d %b %Y")
        blog.create_time = [str(blog.create_time).split()[0], ' '.join(str(blog.create_time).split()[1:])]
        
        blog_month_number = month_mapping[blog.create_time[1].split()[0]]
        blog_year = int(blog.create_time[1].split()[1])

        blog_count = Blog.objects.filter(
            Q(create_time__month=blog_month_number) &
            Q(create_time__year=blog_year)
        ).count()

        to_append = [blog.create_time[1], blog_count]
        if to_append not in archive_dates_and_counts:
            archive_dates_and_counts.append(to_append)

    context = {
        'blog': detailed_blog,
        'categories': BlogCategories.objects.all(),
        'tags': Tags.objects.all(),
        'chosen_models': all_models[:5],
        'archive_dates_and_counts': archive_dates_and_counts
    }
    return render(request, 'blog-detail.html', context)

