from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.views.generic import TemplateView

from .models import NewsRoom
from products.models import Questions_and_answers

class HomePageView(TemplateView):
    template_name = 'home.html'

class AboutUsPageView(TemplateView):
    template_name = 'pages/aboutus.html'

class PrivacyPageView(TemplateView):
    template_name = 'pages/privacy.html'

class OrderRegistrationPageView(TemplateView):
    template_name = 'pages/order_registration.html'

def faq_home_page_view(request):
    all_faq_items = Questions_and_answers.objects.all()

    li_LAR = []
    li_ORP = []
    li_OT = []
    li_RG = []
    li_DCG = []
    li_OS = []

    for item in all_faq_items:
        if item.category_question == 'LAR':
            li_LAR.append(item)
        elif item.category_question == 'ORP':
            li_ORP.append(item)
        elif item.category_question == 'OT':
            li_OT.append(item)
        elif item.category_question == 'RG':
            li_RG.append(item)
        elif item.category_question == 'DCG':
            li_DCG.append(item)
        elif item.category_question == 'OS':
            li_OS.append(item)

    context = {
        'li_LAR': li_LAR,
        'li_ORP': li_ORP,
        'li_OT': li_OT,
        'li_RG': li_RG,
        'li_DCG': li_DCG,
        'li_OS': li_OS,
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
