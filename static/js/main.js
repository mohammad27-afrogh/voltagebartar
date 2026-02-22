$(document).ready(function (e) {
    //    hover-menu-overlay--------------------------
    $('li.nav-overlay').hover(function () {
        $('.mega-menu').removeClass('active');
        $('.nav-categories-overlay').addClass('active');
    }, function () {
        $('.nav-categories-overlay').removeClass('active');
    });

    //    resposive-megamenu-mobile------------------
    $('.dropdown-toggle').on('click', function (e) {
        e.stopPropagation();
        e.preventDefault();

        var self = $(this);
        if (self.is('.disabled, :disabled')) {
            return false;
        }
        self.parent().toggleClass("open");
    });

    $(document).on('click', function (e) {
        if ($('.dropdown').hasClass('open')) {
            $('.dropdown').removeClass('open');
        }
    });

    $('.nav-btn.nav-slider').on('click', function () {
        $('.overlay').show();
        $('nav').toggleClass("open");
    });

    $('.overlay').on('click', function () {
        if ($('nav').hasClass('open')) {
            $('nav').removeClass('open');
        }
        $(this).hide();
    });


    $('li.active').addClass('open').children('ul').show();
    $("li.has-sub > a").on('click', function () {
        $(this).removeAttr('href');
        var e = $(this).parent('li');
        if (e.hasClass('open')) {
            e.removeClass('open');
            e.find('li').removeClass('opne');
            e.find('ul').slideUp(200);
        }
        else {
            e.addClass('open');
            e.children('ul').slideDown(200);
            e.siblings('li').children('ul').slideUp(200);
            e.siblings('li').removeClass('open');
            e.siblings('li').find('li').removeClass('open');
            e.siblings('li').find('ul').slideUp(200);
        }
    });
    //    resposive-megamenu-mobile------------------

    // searchResult--------------------------------------
    $('.header-search .header-search-box .form-search .header-search-input').on('click', function () {
        $(this).parents('.header-search').addClass('show-result').find('.search-result').fadeIn();
        $(".overlay-search-box").css({ "opacity": "1", "visibility": "visible" });
    })
    $(document).click(function (e) {
        if ($(e.target).is('.header-search *')) return;
        $('.search-result').hide();
        $(".overlay-search-box").css({ "opacity": "0", "visibility": "hidden" });
    });
    // searchResult--------------------------------------

    // slider-product------------------------
    $(".product-carousel").owlCarousel({
        rtl: true,
        margin: 10,
        nav: true,
        navText: ['<i class="fa fa-angle-right"></i>', '<i class="fa fa-angle-left"></i>'],
        dots: false,
        responsiveClass: true,
        responsive: {
            0: {
                items: 1,
                slideBy: 1
            },
            576: {
                items: 1,
                slideBy: 1
            },
            768: {
                items: 3,
                slideBy: 2
            },
            992: {
                items: 4,
                slideBy: 2
            },
            1400: {
                items: 4,
                slideBy: 3
            }
        }
    });

    // brand---------------------------------------
    $(".product-carousel-brand").owlCarousel({
        items: 4,
        rtl: true,
        margin: 10,
        nav: true,
        navText: ['<i class="fa fa-angle-right"></i>', '<i class="fa fa-angle-left"></i>'],
        dots: false,
        responsiveClass: true,
        responsive: {
            0: {
                items: 1,
                slideBy: 1
            },
            576: {
                items: 1,
                slideBy: 1
            },
            768: {
                items: 3,
                slideBy: 2
            },
            992: {
                items: 5,
                slideBy: 2
            },
            1400: {
                items: 5,
                slideBy: 3
            }
        }
    });
    // brand---------------------------------------

    // Symbol--------------------------------------
    $(".product-carousel-symbol").owlCarousel({
        rtl: true,
        items: 2,
        loop: true,
        margin: 10,
        dots: false,
        autoplay: true,
        autoplayTimeout: 3000,
        autoplayHoverPause: true,
        responsiveClass: true,
        responsive: {
            0: {
                items: 1,
                slideBy: 1,
                autoplay: true,
            },
            576: {
                items: 1,
                slideBy: 1,
                autoplay: true,
            },
            768: {
                items: 1,
                slideBy: 1,
                autoplay: true,
            },
            992: {
                items: 1,
                slideBy: 1,
                autoplay: true,
            },
            1400: {
                items: 1,
                slideBy: 1,
                autoplay: true,
            }
        }
    });
    // Symbol--------------------------------------

    $("#suggestion-slider").owlCarousel({
        rtl: true,
        items: 1,
        autoplay: true,
        autoplayTimeout: 5000,
        loop: true,
        dots: false,
        onInitialized: startProgressBar,
        onTranslate: resetProgressBar,
        onTranslated: startProgressBar
    });

    function startProgressBar() {
        $(".slide-progress").css({
            width: "100%",
            transition: "width 5000ms"
        });
    }

    function resetProgressBar() {
        $(".slide-progress").css({
            width: 0,
            transition: "width 0s"
        });
    }

    // product-more
    $(".product-carousel-more").owlCarousel({
        rtl: true,
        autoplay: true,
        autoplayTimeout: 5000,
        margin: 10,
        nav: true,
        navText: ['<i class="fa fa-angle-right"></i>', '<i class="fa fa-angle-left"></i>'],
        dots: true,
        loop: true,
        responsiveClass: true,
        responsive: {
            0: {
                items: 1,
                slideBy: 1
            },
            576: {
                items: 1,
                slideBy: 1
            },
            768: {
                items: 1,
                slideBy: 2
            },
            992: {
                items: 1,
                slideBy: 2
            },
            1400: {
                items: 1,
                slideBy: 3
            }
        }
    });

    // advantages-----------------------------
    var inputs = $('#advantage-input, #disadvantage-input');
    var inputChangeCallback = function () {
        var self = $(this);
        if (self.val().trim().length > 0) {
            self.siblings('.js-icon-form-add').show();
        } else {
            self.siblings('.js-icon-form-add').hide();
        }
    };
    inputs.each(function () {
        inputChangeCallback.bind(this)();
        $(this).on('change keyup', inputChangeCallback.bind(this));
    });
    $("#advantages").delegate(".js-icon-form-add", 'click', function (e) {

        var parent = $('.js-advantages-list');
        if (parent.find(".js-advantage-item").length >= 5) {
            return;
        }

        var advantageInput = $('#advantage-input');

        if (advantageInput.val().trim().length > 0) {
            parent.append(
                '<div class="ui-dynamic-label ui-dynamic-label--positive js-advantage-item">\n' +
                advantageInput.val() +
                '<button type="button" class="ui-dynamic-label-remove js-icon-form-remove"></button>\n' +
                '<input type="hidden" name="comment[advantages][]" value="' + advantageInput
                    .val() + '">\n' +
                '</div>');

            advantageInput.val('').change();
            advantageInput.focus();
        }

    }).delegate(".js-icon-form-remove", 'click', function (e) {
        $(this).parent('.js-advantage-item').remove();
    });

    $("#disadvantages").delegate(".js-icon-form-add", 'click', function (e) {

        var parent = $('.js-disadvantages-list');
        if (parent.find(".js-disadvantage-item").length >= 5) {
            return;
        }

        var disadvantageInput = $('#disadvantage-input');

        if (disadvantageInput.val().trim().length > 0) {
            parent.append(
                '<div class="ui-dynamic-label ui-dynamic-label--negative js-disadvantage-item">\n' +
                disadvantageInput.val() +
                '<button type="button" class="ui-dynamic-label-remove js-icon-form-remove"></button>\n' +
                '<input type="hidden" name="comment[disadvantages][]" value="' +
                disadvantageInput.val() + '">\n' +
                '</div>');

            disadvantageInput.val('').change();
            disadvantageInput.focus();
        }

    }).delegate(".js-icon-form-remove", 'click', function (e) {
        $(this).parent('.js-disadvantage-item').remove();
    });
    // advantages-----------------------------

    // sidebar-sticky-------------------------
    if ($('.sticky-sidebar').length) {
        $('.sticky-sidebar').theiaStickySidebar();
    }

    //   countdown----------------------------
    ! function (l) {
        var t = {
            init: function () {
                t.countDown()
            },
            countDown: function (t, i) {
                l(".countdown").each(function () {
                    var t = l(this),
                        a = l(this).data("date-time"),
                        e = l(this).data("labels");
                    (i || t).countdown(a, function (t) {
                        l(this).html(t.strftime('<div class="countdown-item"><div class="countdown-value">%D</div><div class="countdown-label">' + e["label-day"] + '</div></div><div class="countdown-item"><div class="countdown-value">%H</div><div class="countdown-label">' + e["label-hour"] + '</div></div><div class="countdown-item"><div class="countdown-value">%M</div><div class="countdown-label">' + e["label-minute"] + '</div></div><div class="countdown-item"><div class="countdown-value">%S</div><div class="countdown-label">' + e["label-second"] + "</div></div>"))
                    })
                })
            },
        };
        l(function () {
            t.init()
        })
    }(jQuery);
    const cd = new Date().getFullYear() + 1
    $('#countdown').countdown({
        year: cd
    });

    // checkout-coupon-------------------------------
    $(".showcoupon").on("click", function () {
        $(".checkout-coupon").slideToggle(200);
    });
    // checkout-coupon-------------------------------

    // add-product-wishes----------------------------
    $(".add-product-wishes").on("click", function () {
        $(this).toggleClass("active");
    });
    // add-product-wishes----------------------------
    // SweetAlert -----------------------------------
    // cart-item-close
    $('.mini-cart-item-close').on('click', function () {
        Swal.fire({
            text: "آیا مطمئن هستید حذف شود؟",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'بله',
            cancelButtonText: 'خیر'
        }).then((result) => {
            if (result.isConfirmed) {
                Swal.fire({
                    title: 'حذف شد!',
                    confirmButtonText: 'باشه',
                    icon: 'success'
                })
            }
        })
    });
    // add-to-cart
    $('.btn-add-to-cart').on('click', function (event) {
        event.preventDefault();
        const Toast = Swal.mixin({
            toast: true,
            position: 'top-end',
            showConfirmButton: false,
            timer: 2000,
            didOpen: (toast) => {
                toast.addEventListener('mouseenter', Swal.stopTimer)
                toast.addEventListener('mouseleave', Swal.resumeTimer)
            }
        })

        Toast.fire({
            icon: 'success',
            title: 'به سبد خرید خود اضافه شد'
        })
    });
    // compare
    $('.btn-compare').on('click', function (event) {
        event.preventDefault();
        const Toast = Swal.mixin({
            toast: true,
            position: 'top-end',
            showConfirmButton: false,
            timer: 2000,
            didOpen: (toast) => {
                toast.addEventListener('mouseenter', Swal.stopTimer)
                toast.addEventListener('mouseleave', Swal.resumeTimer)
            }
        })

        Toast.fire({
            icon: 'success',
            title: 'محصول برای مقایسه اضافه شد'
        })
    });
    // wishes 
    $('.add-product-wishes').on('click', function (event) {
        event.preventDefault();
        const Toast = Swal.mixin({
            toast: true,
            position: 'top-end',
            showConfirmButton: false,
            timer: 2000,
            didOpen: (toast) => {
                toast.addEventListener('mouseenter', Swal.stopTimer)
                toast.addEventListener('mouseleave', Swal.resumeTimer)
            }
        })

        Toast.fire({
            icon: 'success',
            title: 'به لیست علاقه مندی خود اضافه شد'
        })
    });
    // SweetAlert -----------------------------------
    // nice-select-----------------------------------
    if ($('.custom-select-ui').length) {
        $('.custom-select-ui select').niceSelect();
    }
    // nice-select-----------------------------------
    // // //    price-range--------------------------------
    // var nonLinearStepSlider = document.getElementById('slider-non-linear-step');

    // if ($('#slider-non-linear-step').length) {
    //     noUiSlider.create(nonLinearStepSlider, {
    //         start: [0, 5000000],
    //         connect: true,
    //         direction: 'rtl',
    //         format: wNumb({
    //             decimals: 0,
    //             thousand: ','
    //         }),
    //         range: {
    //             'min': [0],
    //             '10%': [500, 500],
    //             '50%': [40000, 1000],
    //             'max': [10000000]
    //         }
    //     });
    //     var nonLinearStepSliderValueElement = document.getElementById('slider-non-linear-step-value');

    //     nonLinearStepSlider.noUiSlider.on('update', function (values) {
    //         nonLinearStepSliderValueElement.innerHTML = values.join(' - ');
    //     });
    // }    
    // // //    price-range--------------------------

    // price-range --------------------------------
var nonLinearStepSlider = document.getElementById('slider-non-linear-step');

    if ($('#slider-non-linear-step').length) {
        var minPrice = parseInt($('#price-min').val()) || 0; // ورودی مخفی قیمت حداقل
        var maxPrice = parseInt($('#price-max').val()) || 5000000; // ورودی مخفی قیمت حداکثر

        noUiSlider.create(nonLinearStepSlider, {
            start: [minPrice, maxPrice],
            connect: true,
            direction: 'rtl',
            format: wNumb({
                decimals: 0,
                thousand: ','
            }),
            range: {
                'min': [minPrice],
                'max': [maxPrice]
            }
        });

        var nonLinearStepSliderValueElement = document.getElementById('slider-non-linear-step-value');

        nonLinearStepSlider.noUiSlider.on('update', function (values) {
            nonLinearStepSliderValueElement.innerHTML = values.join(' - ');
            var min = Number(values[0].replace(/,/g, ''));
            var max = Number(values[1].replace(/,/g, ''));
            $('#price-min').val(min); // مقدار جدید برای قیمت حداقل
            $('#price-max').val(max); // مقدار جدید برای قیمت حداکثر
        });
    }
    $(document).ready(function() {
    // ... کدهای قبلی اسلایدر ...
    
    // **جدید: مدیریت دکمه اعمال فیلتر**
    $('#apply-price-filter').on('click', function(e) {
        e.preventDefault(); // جلوگیری از ارسال مجدد فرم به روش سنتی

        // 1. خواندن مقادیر نهایی از inputهای مخفی که در 'update' آپدیت شده‌اند
        var finalMin = $('#price-min').val();
        var finalMax = $('#price-max').val();

        // 2. فعال کردن حالت لودینگ (اگر لازم است)
        // نمایش یک اسپینر یا اضافه کردن کلاس لودینگ به بخش محتوا
        $('.shop-archive-content').addClass('loading-overlay'); 

        // 3. فراخوانی تابع اصلی که محصولات را فیلتر می‌کند
        // **شما باید نام تابع واقعی خود را جایگزین کنید:**
        filterProducts(finalMin, finalMax); 
    });
    
    // اگر از دکمه "اعمال" استفاده می‌کنید، ایونت 'update' اسلایدر را حذف کنید
    // تا فقط با کلیک روی "اعمال" فیلتر انجام شود.
    // در این صورت، خط زیر از کد قبلی شما باید حذف شود یا کامنت شود:
    /* 
    nonLinearStepSlider.noUiSlider.on('update', function (values) {
        // ... فقط آپدیت نمایش متن ...
        nonLinearStepSliderValueElement.innerHTML = values.join(' - '); 
        // ... حذف کردن کد آپدیت inputها ...
    });
    */
});



    //    quantity-selector--------------------
    jQuery('<div class="quantity-nav"><div class="quantity-button quantity-up">+</div><div class="quantity-button quantity-down">-</div></div>').insertAfter('.quantity input');
    jQuery('.quantity').each(function () {
        var spinner = jQuery(this),
            input = spinner.find('input[type="number"]'),
            btnUp = spinner.find('.quantity-up'),
            btnDown = spinner.find('.quantity-down'),
            min = input.attr('min'),
            max = input.attr('max');

        btnUp.click(function () {
            var oldValue = parseFloat(input.val());
            if (oldValue >= max) {
                var newVal = oldValue;
            } else {
                var newVal = oldValue + 1;
            }
            spinner.find("input").val(newVal);
            spinner.find("input").trigger("change");
        });

        btnDown.click(function () {
            var oldValue = parseFloat(input.val());
            if (oldValue <= min) {
                var newVal = oldValue;
            } else {
                var newVal = oldValue - 1;
            }
            spinner.find("input").val(newVal);
            spinner.find("input").trigger("change");
        });

    });
    //    quantity-selector-------------------

    // Page Loader----------------------------
    // var preloader = $('.P-loader');
    // $(window).on("load", function () {
    //     var preloaderFadeOutTime = 500;
    //     function hidePreloader() {
    //         preloader.fadeOut(preloaderFadeOutTime);
    //     }
    //     hidePreloader();
    // });
    $(".P-loader").fadeOut(2000,"swing");
    // Page Loader----------------------------

    // scroll_progress-------------------------
    var progressPath = document.querySelector('.progress-wrap path');
    var pathLength = progressPath.getTotalLength();
    progressPath.style.transition = progressPath.style.WebkitTransition = 'none';
    progressPath.style.strokeDasharray = pathLength + ' ' + pathLength;
    progressPath.style.strokeDashoffset = pathLength;
    progressPath.getBoundingClientRect();
    progressPath.style.transition = progressPath.style.WebkitTransition = 'stroke-dashoffset 10ms linear';
    var updateProgress = function () {
        var scroll = $(window).scrollTop();
        var height = $(document).height() - $(window).height();
        var progress = pathLength - (scroll * pathLength / height);
        progressPath.style.strokeDashoffset = progress;
    }
    updateProgress();
    $(window).scroll(updateProgress);
    var offset = 50;
    var duration = 1500;
    jQuery(window).on('scroll', function () {
        if (jQuery(this).scrollTop() > offset) {
            jQuery('.progress-wrap').addClass('active-progress');
        } else {
            jQuery('.progress-wrap').removeClass('active-progress');
        }
    });
    jQuery('.progress-wrap').on('click', function (event) {
        event.preventDefault();
        jQuery('html, body').animate({ scrollTop: 0 }, duration);
        return false;
    });


    //    verify-phone-number------------------------
    if ($("#countdown-verify-end").length) {
        var $countdownOptionEnd = $("#countdown-verify-end");

        $countdownOptionEnd.countdown({
            date: (new Date()).getTime() + 180 * 1000, // 1 minute later
            text: '<span class="day">%s</span><span class="hour">%s</span><span>: %s</span><span>%s</span>',
            end: function () {
                $countdownOptionEnd.html("<a href='' class='link-border-verify form-account-link'>ارسال مجدد</a>");
            }
        });
    }
    $(".line-number-account").keyup(function () {
        $(this).next().focus();
    });
    //    verify-phone-number-----------------------

    // tab-------------------------------------
    $(".mask-handler").click(function (e) {
        e.preventDefault();
        var sumaryBox = $(this).parents('.content-expert-summary');
        sumaryBox.find('.mask-text').toggleClass('active');
        sumaryBox.find('.shadow-box').fadeToggle(0);
        $(this).find('.show-more').fadeToggle(0);
        $(this).find('.show-less').fadeToggle(0);
    });

    $(".content-expert-button").click(function (e) {
        e.preventDefault();
        var sumaryBox = $(this).parents('.content-expert-article');
        sumaryBox.find('.content-expert-article').toggleClass('active');
        sumaryBox.find('.content-expert-text').slideToggle();
        $(this).find('.show-more').fadeToggle(0);
        $(this).find('.show-less').fadeToggle(0);
    });
    // tab-------------------------------------


    // product-img-----------------------------
    $("#gallery-slider").owlCarousel({
        rtl: true,
        margin: 10,
        nav: true,
        navText: ['<i class="fa fa-angle-right"></i>', '<i class="fa fa-angle-left"></i>'],
        dots: false,
        responsiveClass: true,
        responsive: {
            0: {
                items: 4,
                slideBy: 1
            }
        }
    });

    $('.back-to-top').click(function (e) {
        e.preventDefault();
        $('html, body').animate({ scrollTop: 0 }, 800, 'easeInExpo');
    });

    if ($("#img-product-zoom").length) {
        $("#img-product-zoom").ezPlus({
            zoomType: "inner",
            containLensZoom: true,
            gallery: 'gallery_01f',
            cursor: "crosshair",
            galleryActiveClass: "active",
            responsive: true,
            imageCrossfade: true,
            zoomWindowFadeIn: 500,
            zoomWindowFadeOut: 500
        });
    }

    //zoomgallerymodal---------------------------
    $(function () {
        $(".zoom-box img").jqZoom({
            selectorWidth: 30,
            selectorHeight: 30,
            viewerWidth: 400,
            viewerHeight: 300
        });
    });

    var $customEvents = $('#custom-events');
    $customEvents.lightGallery();

    var colours = ['#21171A', '#81575E', '#9C5043', '#8F655D'];
    $customEvents.on('onBeforeSlide.lg', function (event, prevIndex, index) {
        $('.lg-outer').css('background-color', colours[index])
    });
    // product-img-----------------------------
});

function toggleFavorite(productId, isCurrentlyFavorite) {
    const url = `/api/toggle-favorite/${productId}/`; // آدرس صحیح API خود را وارد کنید
    let method;
    let bodyData = {}; // برای POST نیاز است

    if (isCurrentlyFavorite) {
        // اگر قبلاً مورد علاقه است، با کلیک دوباره، حذف (DELETE) می‌کنیم
        method = 'DELETE';
    } else {
        // اگر مورد علاقه نیست، با کلیک، اضافه (POST) می‌کنیم
        method = 'POST';
        // در اینجا، اگر لازم باشد داده‌ای بفرستیم، مثلاً:
        // bodyData = { some_extra_data: 'value' }; 
    }

    fetch(url, {
        method: method,
        headers: {
            // در صورت استفاده از احراز هویت مبتنی بر توکن (مثل JWT) باید توکن را اینجا قرار دهید
            // 'Authorization': 'Bearer your_token_here', 
            'Content-Type': 'application/json',
            // CSRF Token برای درخواست‌های POST/PUT/DELETE در جنگو ضروری است مگر اینکه API جدا باشد
            'X-CSRFToken': getCookie('csrftoken') // تابعی برای گرفتن کوکی CSRF
        },
        // فقط در متد POST بدنه‌ای ارسال می‌شود
        body: method === 'POST' ? JSON.stringify(bodyData) : undefined 
    })
    .then(response => {
        if (response.ok) {
            // اگر پاسخ موفقیت آمیز بود (مثلاً 201 CREATED یا 204 NO CONTENT)
            console.log(`عملیات ${method} موفقیت آمیز بود.`);
            
            // اینجا باید ظاهر دکمه را در صفحه به‌روز کنید (مثلاً آیکون قلب را تغییر دهید)
            updateFavoriteButtonAppearance(productId, !isCurrentlyFavorite); 

            return response.json().catch(() => ({})); // در صورت 204 پاسخ خالی است
        } else if (response.status === 401) {
            alert("لطفاً ابتدا وارد شوید.");
        } else {
            // خطاهای دیگر (مثل 400 BAD REQUEST)
            return response.json().then(err => { throw err; });
        }
    })
    .then(data => {
        if (data && data.detail) {
            console.log("پیام از سرور:", data.detail);
        }
    })
    .catch(error => {
        console.error('خطا در ارسال درخواست:', error);
    });
}

// مثال استفاده:
// فرض کنید متوجه شده‌ایم محصول با ID=45 لایک شده است (isCurrentlyFavorite = true)
// toggleFavorite(45, true);

function fetchUserFavorites() {
    const userToken = 'your_jwt_token_here'; // توکن کاربر

    fetch('/api/favorites/', { // آدرس جدید
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${userToken}`, // ارسال توکن برای احراز هویت
            'Content-Type': 'application/json',
        },
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(favoritesData => {
        console.log("لیست علاقه‌مندی‌های کاربر:", favoritesData);
        
        // در اینجا باید منطق رندر کردن این لیست (favoritesData) 
        // در صفحه HTML/UI را پیاده‌سازی کنید.
        renderFavoritesList(favoritesData); 
    })
    .catch(error => {
        console.error('خطا در دریافت لیست علاقه‌مندی‌ها:', error);
    });
}

// فراخوانی این تابع در زمان مناسب (مثلاً هنگام لود شدن صفحه پروفایل)
// fetchUserFavorites();

function renderFavoritesList(favoritesData) {
    const container = document.getElementById('favorites-list-container'); // فرض کنید یک div خالی با این ID در HTML دارید
    
    if (!container) {
        console.error("Container element not found.");
        return;
    }
    
    container.innerHTML = ''; // پاک کردن محتویات قبلی

    if (favoritesData.length === 0) {
        container.innerHTML = '<p>لیست علاقه‌مندی‌های شما خالی است.</p>';
        return;
    }

    favoritesData.forEach(favoriteItem => {
        // توجه: ساختار داده‌ای که از بک‌اند می‌آید (favoritesData) بستگی به Serializer شما دارد.
        // فرض می‌کنیم هر آیتم شامل یک آبجکت product است.
        const product = favoriteItem.product; 
        
        const productElement = document.createElement('div');
        productElement.className = 'favorite-card';
        
        // ساختار HTML برای نمایش هر محصول:
        productElement.innerHTML = `
            <h3>${product.name}</h3>
            <p>قیمت: ${product.price} تومان</p>
            <img src="${product.image_url}" alt="${product.name}" style="width:100px;">
            <button onclick="toggleFavorite(${product.id})">حذف از علاقه‌مندی‌ها</button>
        `;
        
        container.appendChild(productElement);
    });
}
