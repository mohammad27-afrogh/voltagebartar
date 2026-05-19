# 1. انتخاب ایمیج پایه (مثلا Python)
    FROM python:3.11-slim-bullseye 

    # 2. تنظیم متغیرهای محیطی برای pip (مهم برای رجیستری)
    ENV PIP_INDEX_URL https://pypi.mirrors.bfsu.edu.cn/simple/ # یا هر Mirror پایتون معتبر دیگر
    ENV PIP_TRUST_HOST pypi.mirrors.bfsu.edu.cn # گاهی لازم است

    # 3. تنظیم دایرکتوری کاری
    WORKDIR /app

    # 4. کپی فایل requirements.txt
    COPY requirements.txt ./

    # 5. نصب پکیج‌ها با استفاده از Mirror تنظیم شده
    RUN pip install --no-cache-dir -r requirements.txt

    # 6. کپی کردن بقیه فایل‌های پروژه
    COPY . .

    # 7. تنظیم پورت (اگر لازم است)
    ENV PORT 8000 # یا پورتی که Django شما روی آن اجرا می‌شود
    EXPOSE 8000

    # 8. دستور اجرای اپلیکیشن (مثال برای Django)
    # CMD ["python", "manage.py", "runserver", "0.0.0.0:$PORT"] # برای تست محلی
    CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "your_project.wsgi:application"] # برای production