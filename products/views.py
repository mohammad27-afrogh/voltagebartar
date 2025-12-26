from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.conf import settings
from django.db.models import Q
from star_ratings.models import Rating

from .models import  Product, Comment, Category
from .forms import CommentForm, QuestionsAndAnswersForm

def product_list_view(request):
    selected_category_slug = request.GET.get('category')
    products = Product.objects.all().order_by('id')
    current_category_name = 'all products'

    if selected_category_slug:
        try:
            category = Category.objects.get(slug__iexact=selected_category_slug)
            # ایجاد فیلتر برای خود دسته و زیر‌دسته‌هایش
            subcategories = category.subcategories.all()
            products = Product.objects.filter(
                Q(category=category) | Q(category__in=subcategories)
            ).order_by('id')

            current_category_name = category.name

        except Category.DoesNotExist:
            products = Product.objects.none()
            current_category_name = f'Category "{selected_category_slug}" not found!'

    context = {
        'products': products,
        'current_category_name': current_category_name,
        'categories': Category.objects.all(),
    }

    return render(request, 'products/product_list.html', context)


def product_detail_view(request, product_slug):
    # --- ۱. بهینه‌سازی کوئری برای محصول و Breadcrumb ---
    # .select_related('category', 'category__parent', 'category__parent__parent')
    # تضمین می‌کند که تمام دسته‌های والد مورد نیاز در یک کوئری کشیده شوند.
    product = get_object_or_404(
        Product.objects.select_related(
            'category',
            'category__parent',
            'category__parent__parent'  # اگر بیشتر از دو سطح والد دارید، این را افزایش دهید
        ),
        slug=product_slug
    )

    product_comments = product.comments.all()  # نظرات همچنان با کوئری جداگانه لود می‌شوند (که برای لیست نظرات استاندارد است)

    # --- ۲. محاسبه زنجیره Breadcrumb در View ---
    category = product.category
    categories_chain = []

    total_inventory_exists = product.product_item.filter(inventory__gt=0).exists()

    if category:
        # اضافه کردن دسته فعلی
        categories_chain.append(category)

        # پیمایش به سمت بالا تا رسیدن به ریشه (category.parent = None)
        while category.parent:
            category = category.parent
            categories_chain.insert(0, category)  # اضافه کردن به ابتدای لیست

    # --- ۳. مدیریت فرم نظرات ---
    if request.method == 'POST':

        # A) *** بخش جدید: مدیریت امتیازدهی محصول ***
        if 'product_rating_value' in request.POST:
            rating_value = request.POST.get('product_rating_value')
            try:
                # استفاده از تابع مخصوص پکیج star_ratings برای اتصال به شیء محصول
                rating_instance, created = Rating.objects.get_or_create_for_object(
                    product,  # امتیاز مستقیماً به شیء Product متصل می‌شود
                    request.user
                )
                rating_instance.value = rating_value
                rating_instance.save()
                # هدایت مجدد برای جلوگیری از ارسال مجدد فرم
                return redirect('product_detail_url_name', product_slug=product_slug)
            except Exception as e:
                # مدیریت خطا در صورت بروز مشکل در ثبت امتیاز
                print(f"Error saving product rating: {e}")
                # می‌توانید یک پیام خطا به کاربر نمایش دهید

        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.product = product  # استفاده از متغیر بهینه شده 'product'
            new_comment.user = request.user
            new_comment.save()
            comment_form = CommentForm()

        question_form = QuestionsAndAnswersForm(request.POST)
        if question_form.is_valid():
            new_question = question_form.save(commit=False)
            new_question.product = product  # استفاده از متغیر بهینه شده 'product'
            new_question.user = request.user
            new_question.save()
            question_form = QuestionsAndAnswersForm()

    else:
        comment_form = CommentForm()
        question_form = QuestionsAndAnswersForm()


    # --- ۴. محاسبه میانگین امتیاز محصول برای Context ---
    # فرض می‌کنیم شیء Product شما یک متد کمکی برای گرفتن امتیاز دارد،
    # اگر نه، باید آن را در اینجا محاسبه کنید:
    try:
        product_avg_rating = product.rating_set.aggregate(avg_rating=Avg('value'))['avg_rating'] or 0.0
    except:
        # اگر مدل Rating برای Product تعریف نشده باشد، باید از طریق محقق (Generic Foreign Key) اقدام کنید
        # این مرحله بستگی به نحوه پیاده‌سازی star_ratings برای Product شما دارد.
        product_avg_rating = 0.0

    context = {
        'product': product,
        'comments': product_comments,
        'comment_form': comment_form,
        'question_form': question_form,
        'media_url': settings.MEDIA_URL,
        'breadcrumb_categories': categories_chain, # ارسال لیست دسته‌ها به قالب
        'features': product.features,
        'inventory': total_inventory_exists,
        'product_avg_rating': product_avg_rating,  # ارسال امتیاز میانگین به قالب
    }

    # --- ۴. ارسال به قالب ---
    return render(request, 'products/product_detail.html', context)


def category_detail_view(request, category_slug):
    current_category = get_object_or_404(Category, slug=category_slug)

    products_in_category = Product.objects.filter(category=current_category)

    context = {
        'category': current_category,
        'products': products_in_category,
    }

    return render(request, 'products/product_list.html', context)

