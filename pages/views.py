from django.shortcuts import render

from django.views.generic import TemplateView

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
