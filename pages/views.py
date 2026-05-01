from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.views.generic import TemplateView

from .models import NewsRoom, AboutUs
from products.models import Questions_and_answers, Answer

class HomePageView(TemplateView):
    template_name = 'home.html'

def about_us_view_page(request):
    about_us = AboutUs.objects.all()

    return render(request, 'pages/aboutus.html', context={'about_us': about_us})

class PrivacyPageView(TemplateView):
    template_name = 'pages/privacy.html'

class OrderRegistrationPageView(TemplateView):
    template_name = 'pages/order_registration.html'

def faq_home_page_view(request):
    category = request.GET.get('category')

    if category:
        questions = Questions_and_answers.objects.filter(category_question=category)

    else:
        questions = Questions_and_answers.objects.all()

    # عکس مربوط به هر دسته بندی 
    category_images = {
        'LAR': '/static/img/page-faq/add-group.png',
        'ORP': '/static/img/page-faq/open-box.png',
        'OT': '/static/img/page-faq/tracking.png',
        'RG': '/static/img/page-faq/return.png',
        'DCG': '/static/img/page-faq/gift.png',
        'OS': '/static/img/page-faq/other.svg',
    }

    context = {
        'questions': questions,
        'selected_category': category,
        # برای نمایش دکمه ها 
        'categories': Questions_and_answers.CHOICES_QUESTION_AND_ANSWER,
        'category_images': category_images,
    }

    return render(request, 'pages/faq.html', context)


def news_room_page_view(request):
    news = NewsRoom.objects.all()

    NUMBER_PAGINATOR = 5
    paginator = Paginator(news, NUMBER_PAGINATOR)
    page_number = request.GET.get('page', 1)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {
        'news': page_obj.object_list,
        'page_obj': page_obj,
        'paginator': paginator,
        'is_paginated': page_obj.has_other_pages(),
    }

    return render(request, 'pages/news_list.html', context)


def news_detail_by_slug(request, news_slug):
    new = get_object_or_404(NewsRoom, slug=news_slug)
    new.view_count = new.view_count + 1
    new.save()

    return render(request, 'pages/news_detail.html', context={'new': new})
