from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.conf import settings
from django.db.models import Q, Count
from django.db.models import Min, Max, Avg
from star_ratings.models import Rating
from datetime import timedelta
from django.utils import timezone

from .models import  Product, Comment, Category, Brand
from .forms import CommentForm, QuestionsAndAnswersForm



def product_list_view(request):
    # مقداردهی اولیه برای حالتی که هیچ فیلتری اعمال نشده است
    products = Product.objects.all().order_by('id')
    current_category_name = "همه محصولات"

    selected_category_slug = request.GET.get('category')

    if selected_category_slug:
        try:
            # یافتن دسته‌ای که کاربر روی آن کلیک کرده است
            category = Category.objects.get(slug__iexact=selected_category_slug)

            # 1. تمام زیردسته‌های (فرزندان در هر عمقی) این دسته را پیدا کن
            all_descendants = category.get_all_descendants()

            # 2. لیست نهایی دسته‌ها شامل: خود دسته + تمام نوادگان
            all_related_categories = [category] + all_descendants

            # 3. فیلتر کردن محصولات بر اساس این لیست دسته‌ها
            products = Product.objects.filter(category__in=all_related_categories).order_by('id')

            current_category_name = category.name

        except Category.DoesNotExist:
            # اگر دسته‌ای با این اسلاگ پیدا نشد، لیست محصولات خالی می‌شود
            products = Product.objects.none()
            current_category_name = "دسته مورد نظر یافت نشد"

    context = {
        'products': products,
        'categories': Category.objects.all(),  # این برای نمایش منوی دسته‌بندی‌ها در نوار کناری استفاده می‌شود
        'current_category_name': current_category_name,
    }

    # نام فایل قالب HTML شما (که محصولات را رندر می‌کند)
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
        ).prefetch_related('discounts'),
        slug=product_slug
    )

    product.increment_view_count()

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

    # 1. دریافت لیست تمام دسته‌بندی‌های زیرین، از جمله خود دسته فعلی
    # ما باید خود دسته فعلی (include_self) را نیز به لیست اضافه کنیم.
    all_related_categories = current_category.get_all_descendants()
    all_related_categories.append(current_category)  # اضافه کردن دسته مادر

    # 2. فیلتر کردن محصولات بر اساس لیست دسته‌بندی‌های جمع‌آوری شده
    products_in_category = Product.objects.filter(category__in=all_related_categories).prefetch_related('discounts')

    # فیلتر برای یافتن فرزندان مستقیم
    child_categories = Category.objects.filter(parent=current_category)

    # ************ منطق جدید: فیلتر برندهای مرتبط ************

    # استخراج برندهای منحصر به فرد از کوئری محصولات موجود
    related_brand_ids = products_in_category.values_list('brand_id', flat=True).distinct()

    # بازیابی اشیاء Brand با استفاده از IDهای منحصر به فرد به دست آمده
    # (این فرض را می‌کند که مدل Product شما دارای فیلد 'brand_id' است که به مدل Brand اشاره دارد)
    related_brands = Brand.objects.filter(id__in=related_brand_ids)

    price_range = products_in_category.aggregate(min_price=Min('base_price'), max_price=Max('base_price'))

    default_time = timezone.now()
    one_month_ago = default_time - timedelta(days=60)

    new_products = (products_in_category.filter(Q(date_time_create__gte=one_month_ago) &
                                              Q(date_time_create__lte=default_time))
                       .prefetch_related('discounts')  # *** اصلاح: اضافه کردن prefetch_related ***
                       )

    products_cheapest = products_in_category.order_by('base_price')
    products_most_expensive = products_in_category.order_by('-base_price')


    successful_sale_products = products_in_category.order_by('-successful_sales_count')

    # *** اصلاح: اضافه کردن ویژگی active_discount ***
    for product in successful_sale_products:
        # این خط، اولین تخفیف فعال را پیدا کرده و به عنوان active_discount اضافه می‌کند
        product.active_discount = product.discounts.filter(is_active=True).first()

    Number_of_visits = products_in_category.order_by('-view_count')

    popular_active_products = products_in_category.annotate(
    # 1. ایجاد یک فیلد جدید به نام 'active_comment_count'
    active_comment_count=Count(
        'comments',  # نام رابطه معکوس به مدل Comment
        
        # 2. شرط فیلتر کردن در حین شمارش: فقط نظراتی که is_active=True دارند
        filter=Q(comments__is_active=True) 
            )
        ).filter(
            # 3. فیلتر نهایی: فقط محصولاتی که تعداد نظرات فعالشان > 5 است
            active_comment_count__gte=5
        ).order_by('-active_comment_count')

    # اگر ساختار شما از فیلد 'category' در مدل محصول استفاده می‌کند که یک شیء Category است،
    # این کوئری تمام محصولات موجود در تمام سطوح زیرین آن دسته را برمی‌گرداند.

    context = {
        'category': current_category,
        'products': products_in_category,
        'child_categories': child_categories,
        'brands': related_brands,
        'min_price': price_range['min_price'],
        'max_price': price_range['max_price'],
        'new_products': new_products,
        'products_cheapest': products_cheapest,
        'products_most_expensive': products_most_expensive,
        'successful_sale_products': successful_sale_products,
        'Number_of_visits': Number_of_visits,
        'popular_active_products': popular_active_products,
    }

    return render(request, 'products/product_list.html', context)
