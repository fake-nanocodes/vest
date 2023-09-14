# Use an official Python runtime as a parent image
FROM python:3.9

# Set environment variables for Python and Django
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE "vest.settings"

# Create and set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container and install dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy the Django project source code into the container
COPY . /app/

# Expose the Gunicorn port (default is 8000)
EXPOSE 8000

ENV GOOGLE_TRANSLATE_LINK "https://translate.yandex.net/website-widget/v1/widget.js?widgetId=ytWidget&pageLang=en&widgetTheme=light&autoMode=true"
ENV CHAT_BOT "//code.jivosite.com/widget/ZPDfMEE7iG"
ENV DATABASE_URL "postgresql://postgres:XiOruCN3Q56YNm3TmMKD@containers-us-west-97.railway.app:6413/railway"
ENV DEBUG "True"
ENV DEFAULT_FROM_EMAIL "info@crestexperts.com"
ENV DISABLE_COLLECTSTATIC 0
ENV EMAIL_HOST "mail.privateemail.com"
ENV EMAIL_HOST_PASSWORD "koko123box"
ENV EMAIL_HOST_USER "info@crestexperts.com"
ENV EMAIL_PORT "465"
ENV EMAIL_USE_TLS "True"
ENV RECIPIENT_ADDRESS "chiomzibae101@gmail.com"
ENV SECRET_KEY "ygfyidhuifvyiyhdffdkjffdjjejerjejkfjkwdgu63633784278478784278yuwewjhsdjhsdjsdjsdjsdj8781818w778a8a8sa8s8sd8sd8"

RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

# Start Gunicorn to serve your Django application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "vest.wsgi:application"]
