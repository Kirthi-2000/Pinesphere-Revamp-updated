from django.shortcuts import get_object_or_404, render
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import Http404, HttpResponse, JsonResponse
from django.utils import timezone
from django.conf import settings 
from .models import *
from datetime import datetime
import uuid
import json
from datetime import timedelta
from geopy.geocoders import Nominatim  # For geolocation
from user_agents import parse as parse_user_agent  # Use `parse_user_agent` for user agent parsing
import requests
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from .models import Enquiry
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from email.mime.image import MIMEImage
import os
import firebase_admin

from django.templatetags.static import static
from .forms import *
from django.utils.html import strip_tags
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import PageView
from django.utils import timezone
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from firebase_admin import messaging, credentials
from django.db.models import Count
from django.db.models.functions import TruncDay
import calendar


def billing(request):
    return render(request, 'billing.html')

# View for the RTL (Right to Left) page
def rtl(request):
    return render(request, 'rtl.html')

# View for the tables page
def tables(request):
    return render(request, 'tables.html')

def signup (request):
    return render (request, 'sign-up.html')

def profile (request):
    return render (request, 'profile.html')

def admin_base(request):
    return render (request, "base.html")

def base(request):
    return render(request, 'frontend_templates/base.html')


def index(request):
    return render(request, 'frontend_templates/index.html')


def about_us(request):
    return render(request, 'frontend_templates/about_us.html')


@csrf_exempt
def save_fcm_token(request):
    if request.method == 'POST':
        token = request.POST.get('token')
        if token:
            FCMToken.objects.update_or_create(token=token)
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'})



@csrf_exempt  # Consider removing this and handling CSRF properly
def ContactUs(request):
    if request.method == 'POST':
        # Form data
        type_of_enquiry = request.POST.get('type_of_enquiry')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email_address = request.POST.get('email_address')
        phone_number = request.POST.get('phone_number', '')
        message = request.POST.get('message')
        subscribe_me = request.POST.get('subscribe_me', False)
        agree_terms = request.POST.get('agree_terms', False)

        # reCAPTCHA validation
        recaptcha_response = request.POST.get('g-recaptcha-response')
        data = {
            'secret': '6LdHM1MqAAAAACc2Cjwb5Uf5m0HIwsoserSId4ZZ',
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()

        # Check if reCAPTCHA is valid and required fields are filled
        if result['success']:
            # Save Enquiry to the database
            enquiry = Enquiry.objects.create(
                type_of_enquiry=type_of_enquiry,
                first_name=first_name,
                last_name=last_name,
                email_address=email_address,
                phone_number=phone_number,
                message=message,
                subscribe_me=bool(subscribe_me),
                agree_terms=1
            )

            # Send Email Notification with template
            subject = f'New Enquiry from {first_name} {last_name}'
            context = {
                'first_name': first_name,
                'last_name': last_name,
                'type_of_enquiry': type_of_enquiry,
                'email_address': email_address,
                'phone_number': phone_number,
                'message': message,
                'subscribe_me': subscribe_me,
                'agree_terms': agree_terms,
            }
            email_message = render_to_string('frontend_templates/contact_us_email.html', context)
            recipient_list = ['vandhana.jayakumar1106@gmail.com']  # Replace with your recipient email

            send_mail(subject, '', 'vandhana.jayakumar1106@gmail.com', recipient_list, html_message=email_message)

            # Send confirmation reply email to the user (Implement this function separately)
            send_confirmation_email_contactus(first_name, last_name, type_of_enquiry, email_address)

            messages.success(request, 'Thank you for your enquiry!')
            return redirect('ContactUs')
        else:
            messages.error(request, 'Invalid reCAPTCHA. Please try again.')

    return render(request, 'frontend_templates/ContactUs.html')
def send_confirmation_email_contactus(first_name, last_name, type_of_enquiry, email_address):
    reply_subject = 'Thank you for contacting us!'
    context = {
        'first_name': first_name,
        'last_name': last_name,
        'type_of_enquiry': type_of_enquiry,
        'thanks_image_cid': 'thanks_image_cid',
        'linkedin_image_cid': 'linkedin_image_cid',
        'instagram_image_cid': 'instagram_image_cid',
    }
    reply_message = render_to_string('frontend_templates/contact_us_reply_email.html', context)

    email = EmailMultiAlternatives(
        subject=reply_subject,
        body='',  # Empty plain text version
        from_email='vandhana.jayakumar1106@gmail.com',
        to=[email_address]
    )

    email.attach_alternative(reply_message, "text/html")

    # Embed images in the email template using CID
    attach_images_to_email_contactus(email)

    email.send()

def attach_images_to_email_contactus(email):
    static_image_paths = [
        ('Images/Thanks.jpg', 'thanks_image_cid'),
        ('Images/image-1.png', 'linkedin_image_cid'),
        ('Images/image-2.png', 'instagram_image_cid')
    ]

    for image_path, image_cid in static_image_paths:
        full_image_path = os.path.join(settings.STATICFILES_DIRS[0], image_path)
        with open(full_image_path, 'rb') as img:
            mime_image = MIMEImage(img.read())
            mime_image.add_header('Content-ID', f'<{image_cid}>')
            mime_image.add_header('Content-Disposition', 'inline')  # Ensure the image is treated as inline
            email.attach(mime_image)
def Contact(request):
    return render(request, 'ContactUs 1.html')

def Contact(request):
    return render(request, 'frontend_templates/ContactUs 1.html')

def lifeatpines(request):
    return render (request, 'frontend_templates/lifeatpines.html')

def careers (request):
    return render (request, 'frontend_templates/careers.html')

def digital_learning (request):
    return render (request, 'frontend_templates/DigitalLearning.html')
def Ml_Ai (request):
    return render (request, 'frontend_templates/MlAi.html')
def IotService (request):
    return render (request, 'frontend_templates/IotService.html')
def DwmService (request):
    return render (request, 'frontend_templates/DwmService.html')
def RpaService (request):
    return render (request, 'frontend_templates/RpaService.html')
def CloudService (request):
    return render (request, 'frontend_templates/CloudService.html')

def portfolio (request):
    return render (request, 'frontend_templates/portfolio.html')

def workwithus (request):
    return render (request, 'frontend_templates/workwithus.html')

def teams (request):
    return render(request, 'frontend_templates/teams.html')

def Pines_News_R (request):
    return render(request, 'frontend_templates/Pines_News_R.html')

def t_c (request):
    return render(request, 'frontend_templates/T&C.html')

def privacy_p (request):
    return render(request, 'frontend_templates/privacy_p.html')

def support (request):
    return render(request, 'frontend_templates/support.html')


def form (request, job_id):
    job = get_object_or_404(Job_Post, pk=job_id)  # Get the job by ID
    
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the application logic here
            # You can access form data using form.cleaned_data
            
            # Example: Save the application details along with the job role
            applicant_name = form.cleaned_data['name']
            applicant_email = form.cleaned_data['email']
            resume = form.cleaned_data['resume']

            # Optionally, process the application (e.g., save to the database)
            
            return redirect('application_success')  # Redirect on successful submission
    else:
        form = JobApplicationForm()
    
    return render(request, 'frontend_templates/form.html', {'form': form, 'job': job , "job_id":job_id})
def pinesnews1 (request):
    return render(request, 'frontend_templates/pinesnews1.html')
def pinesnews2 (request):
    return render(request, 'frontend_templates/pinesnews2.html')
def pinesnews3 (request):
    return render(request, 'frontend_templates/pinesnews3.html')


def apply_for_job(request, job_id):
    job = get_object_or_404(Job_Post, pk=job_id)  # Get the job by ID
    
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the application logic here
            # You can access form data using form.cleaned_data
            
            # Example: Save the application details along with the job role
            applicant_name = form.cleaned_data['name']
            applicant_email = form.cleaned_data['email']
            resume = form.cleaned_data['resume']

            # Optionally, process the application (e.g., save to the database)
            
            return redirect('application_success')  # Redirect on successful submission
    else:
        form = JobApplicationForm()
    
    return render(request, 'form.html', {'form': form, 'job': job , "job_id":job_id})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required

def dashboard(request):
    # Get the current date
    today = datetime.now().date()

    # Filter internship applications created today
    internship_applications_today = InternshipApplication.objects.filter(created_at__date=today)

    # Other context data
    now = datetime.now()
    current_date = now.strftime("%d-%m-%y")
    current_day = now.strftime("%A")
    username = request.user.username if request.user.is_authenticated else "Guest"
    login_success = request.session.pop('login_success', None)
    pinenews_count = PineNews.objects.all().count()
    contactus_count = Enquiry.objects.all().count()
    jobpost_count = Job_Post.objects.all().count()
    mobile_view = PageView.objects.filter(device_type="Mobile").count()
    tablet_view = PageView.objects.filter(device_type="Tablet").count()
    pc_view = PageView.objects.filter(device_type="PC").count()
    others_view = PageView.objects.filter(device_type="Other").count()

    internship_applications_count = InternshipApplication.objects.all().count()

    context = {
        'mobile_view': mobile_view,
        'tablet_view': tablet_view,
        'pc_view': pc_view,
        'others_view': others_view,
        'internship_applications_count': internship_applications_count,
        'jobpost_count': jobpost_count,
        'contactus_count': contactus_count,
        'pinenews_count': pinenews_count,
        'current_date': current_date,
        'login_success': login_success,
        'current_day': current_day,
        'username': username,
        'internship_applications_today': internship_applications_today,  # Pass today's applications
        'active': 'dashboard',
    }

    return render(request, 'index.html', context)



def get_page_view_counts(request):
    # Get today's date
    today = timezone.now()

    # Get the first day of the current month and the previous month
    first_day_current_month = today.replace(day=1)
    first_day_previous_month = (first_day_current_month - timezone.timedelta(days=1)).replace(day=1)
    last_day_previous_month = first_day_current_month - timezone.timedelta(days=1)

    # Count page views for the current month (up to today's date)
    current_month_page_views = (
        PageView.objects.filter(timestamp__gte=first_day_current_month, timestamp__lte=today)
        .annotate(day=TruncDay('timestamp'))
        .values('day')
        .annotate(count=Count('id'))
        .order_by('day')
    )

    # Count page views for the previous month
    previous_month_page_views = (
        PageView.objects.filter(timestamp__gte=first_day_previous_month, timestamp__lte=last_day_previous_month)
        .annotate(day=TruncDay('timestamp'))
        .values('day')
        .annotate(count=Count('id'))
        .order_by('day')
    )

    # Prepare data for the chart
    current_month_data = {day['day'].day: day['count'] for day in current_month_page_views}
    previous_month_data = {day['day'].day: day['count'] for day in previous_month_page_views}

    # Fill in missing days with 0
    current_month_days = [current_month_data.get(day, 0) for day in range(1, today.day + 1)]
    previous_month_days = [previous_month_data.get(day, 0) for day in range(1, calendar.monthrange(last_day_previous_month.year, last_day_previous_month.month)[1] + 1)]

    return JsonResponse({
        'current_month': current_month_days,
        'previous_month': previous_month_days,
    })

from django.db.models import Count
from django.http import JsonResponse
from .models import PageView

def get_device_type_counts(request):
    # Aggregate the count of each device type
    device_counts = PageView.objects.values('device_type').annotate(count=Count('device_type')).order_by('-count')

    # Prepare data for JSON response
    data = {
        'labels': [entry['device_type'] for entry in device_counts],
        'counts': [entry['count'] for entry in device_counts],
    }
    return JsonResponse(data)


def logout_view(request):
    logout(request)
    # Set a session variable to indicate successful logout
    request.session['logout_success'] = True
    return redirect('/accounts/login/')


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

def login_view(request):
    # Check for logout success message
    logout_success = request.session.pop('logout_success', None)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Set a session variable to indicate successful login
            request.session['login_success'] = True
            # Redirect to the next page or a default page
            return redirect(request.GET.get('next', 'dashboard'))  
        else:
            # Return an 'invalid login' error message.
            return render(request, 'sign-in.html', {'error': 'Invalid credentials', 'logout_success': logout_success})

    return render(request, 'sign-in.html', {'logout_success': logout_success})


def save_location(request):
    if request.method == 'POST':
        # Check if the user has a unique ID in cookies
        user_unique_id = request.COOKIES.get('user_unique_id')

        if not user_unique_id:
            # Generate a new unique ID if it doesn't exist
            user_unique_id = str(uuid.uuid4())

        # Load request data
        data = json.loads(request.body)
        ip_address = request.META.get('REMOTE_ADDR')
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        city, country = get_city_country_from_coords(latitude, longitude)

        # Get device info and browser details
        device_info = get_device_info(request)
        device_type = device_info[0]
        user_agent = device_info[1]
        browser_name = device_info[2]
        browser_version = device_info[3]

        # Time threshold for checking 24-hour window
        now = timezone.now()
        time_threshold = now - timedelta(hours=24)

        # Check if a PageView exists for this user within the last 24 hours
        recent_view = PageView.objects.filter(user_unique_id=user_unique_id, timestamp__gte=time_threshold).exists()

        if recent_view:
            return JsonResponse({'status': 'Visitor has already been recorded within the last 24 hours'})
        else:
            # Save new page view but reuse the same user_unique_id
            page_view = PageView.objects.create(
                user_unique_id=user_unique_id,
                ip_address=ip_address,
                city=city,
                country=country,
                device_type=device_type,
                user_agent=user_agent,  # Save the user agent here
                user_browser=f'{browser_name} {browser_version}'  # Save browser name and version
            )

            # Set the cookie if it's a new visitor
            response = JsonResponse({'status': 'New page view recorded for returning visitor'})
            if not request.COOKIES.get('user_unique_id'):
                response.set_cookie('user_unique_id', user_unique_id, max_age=60*60*24*365)  # Save cookie for 1 year

            return response

    return JsonResponse({'status': 'Invalid request'}, status=400)


def is_english(text):
    try:
        text.encode('ascii')
    except UnicodeEncodeError:
        return False
    return True

def get_city_country_from_coords(latitude, longitude):
    geo_locator = Nominatim(user_agent='geoapiExcises')
    location = geo_locator.reverse(f"{latitude},{longitude}", timeout=10)  # Increase the timeout to 10 seconds
    address = location.raw.get('address', {})
    
    state_district = address.get('state_district', 'unknown')
    country = address.get('country', 'unknown')
    
    # Check if the values are in English, otherwise set to 'unknown'
    if not is_english(state_district):
        state_district = 'unknown'
    if not is_english(country):
        country = 'unknown'
    
    return state_district, country
from user_agents import parse as parse_user_agent
def get_device_info(request):
    user_agent_string = request.META.get('HTTP_USER_AGENT', '')
    user_agent = parse_user_agent(user_agent_string)  # Use this to parse the user agent

    # Determine the device type
    if user_agent.is_mobile:
        device_type = 'Mobile'
    elif user_agent.is_tablet:
        device_type = 'Tablet'
    elif user_agent.is_pc:
        device_type = 'PC'
    else:
        device_type = 'Other'

    # Get browser name and version
    browser_name = user_agent.browser.family  # e.g., 'Chrome'
    browser_version = user_agent.browser.version_string  # e.g., '89.0.4389.82'
    print(browser_name, browser_version)

    return device_type, user_agent_string, browser_name, browser_version


def unsubscribe(request, email):
    if email:
        try:
            subscriber = NewsletterSubscriber.objects.get(email=email, active = True)
            subscriber.active = False
            subscriber.save()
            return HttpResponse("You have been unsubscribed successfully.")
        except NewsletterSubscriber.DoesNotExist:
            return HttpResponse("Email address not found.")
    return HttpResponse("Invalid request.")

def newsletter_signup(request):
    if request.method == 'POST':
        form = NewsletterSignupForm(request.POST)
        
        # We can access the email directly now
        email = form.data.get('email_address')

        if email:  # Ensure we got an email
            # Check if the email already exists in the database
            try:
                newsletter_signup = NewsletterSubscriber.objects.get(email=email)

                if newsletter_signup.active:
                    # If the subscription is already active
                    return JsonResponse({
                        'message': "You are already signed up."
                    }, status=200)
                else:
                    # If the subscription exists but is inactive, activate it
                    newsletter_signup.active = True
                    newsletter_signup.save()

                    # Generate unsubscribe URL
                    unsubscribe_url = request.build_absolute_uri(
                        reverse('unsubscribe', kwargs={'email': email})
                    )

                    # Render the email template for reactivation
                    template_dir = os.path.join(settings.BASE_DIR, 'templates', 'Mail_Templates')
                    message_html = render_to_string(os.path.join(template_dir, 'subscribed.html'), {'unsubscribe_url': unsubscribe_url})
                    message_plain = strip_tags(message_html)

                    # Send confirmation email
                    send_mail(
                        'Newsletter Signup Confirmation',
                        message_plain,
                        settings.DEFAULT_FROM_EMAIL,
                        [email],
                        html_message=message_html,
                    )

                    return JsonResponse({
                        'message': "You have successfully signed up for the newsletter!"
                    }, status=200)

            except NewsletterSubscriber.DoesNotExist:
                # If the email doesn't exist, create a new subscriber
                newsletter_signup = NewsletterSubscriber.objects.create(email=email, active=True)

                # Generate unsubscribe URL
                unsubscribe_url = request.build_absolute_uri(
                    reverse('unsubscribe', kwargs={'email': email})
                )

                # Render the email template for new subscription
                template_dir = os.path.join(settings.BASE_DIR, 'templates', 'Mail_Templates')
                message_html = render_to_string(os.path.join(template_dir, 'subscribed.html'), {'unsubscribe_url': unsubscribe_url})
                message_plain = strip_tags(message_html)

                # Send confirmation email
                send_mail(
                    'Newsletter Signup Confirmation',
                    message_plain,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    html_message=message_html,
                )

                return JsonResponse({
                    'message': "You have successfully signed up for the newsletter!"
                }, status=200)

        # If no email was provided
        return JsonResponse({'message': 'Email is required.'}, status=400)

    return JsonResponse({'message': 'Invalid request method'}, status=405)

from dateutil.parser import parse

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def viewers_details(request):
    # Handle date filtering
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Filter the PageView based on the date range if provided
    pageviews = PageView.objects.all()

    if start_date and end_date:
        try:
            # Parse the dates and make them timezone-aware
            start_date = parse(start_date).astimezone(timezone.get_current_timezone())
            end_date = parse(end_date).astimezone(timezone.get_current_timezone())
            
            # Filter the pageviews based on date range
            pageviews = pageviews.filter(timestamp__range=[start_date, end_date])
        except (ValueError, TypeError):
            # Handle invalid date formats
            start_date = None
            end_date = None

    # Add ordering to the queryset
    pageviews = pageviews.order_by('-timestamp')

    # Handle pagination
    paginator = Paginator(pageviews, 10)  # Show 10 records per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    total = pageviews.count()
    today = timezone.now().date()

# Filter pageviews for today only
    today_pageviews = pageviews.filter(timestamp__date=today)

# Get the total count of today's pageviews
    total_today = today_pageviews.count()

    context = {
        'total': total,
        'page_obj': page_obj,
        'active': "visitors",
        'start_date': start_date,
        'end_date': end_date,
        'total_today':total_today
    }
    return render(request, 'viewers.html', context)
def delete_pageview(request, pk):
    if request.method == "POST":  # Check if the request is a POST request
        pageview = get_object_or_404(PageView, pk=pk)  # Use get_object_or_404 for safety
        pageview.delete()
        return JsonResponse({'status': 'success', 'message': 'Pageview deleted successfully.'})  # Return success message as JSON

    return JsonResponse({'status': 'error', 'message': 'Error deleting pageview.'}) 

from django.shortcuts import render
from django.utils.dateparse import parse_date

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def internship_applications(request):
    # Get date filters from GET parameters
    start_date_unreviewed = request.GET.get('start_date_unreviewed')
    end_date_unreviewed = request.GET.get('end_date_unreviewed')

    start_date_rejected = request.GET.get('start_date_rejected')
    end_date_rejected = request.GET.get('end_date_rejected')

    start_date_shortlisted = request.GET.get('start_date_shortlisted')
    end_date_shortlisted = request.GET.get('end_date_shortlisted')

    # Fetch applications based on their status
    unreviewed_applications = InternshipApplication.objects.filter(status = "unreviewed")
    rejected_applications = InternshipApplication.objects.filter(status = "shortlisted")
    shortlisted_applications = InternshipApplication.objects.filter(status = "rejected")

    # Apply date filtering for unreviewed applications
    if start_date_unreviewed:
        start_date_unreviewed = parse_date(start_date_unreviewed)
        unreviewed_applications = unreviewed_applications.filter(timestamp__gte=start_date_unreviewed)
    if end_date_unreviewed:
        end_date_unreviewed = parse_date(end_date_unreviewed)
        unreviewed_applications = unreviewed_applications.filter(timestamp__lte=end_date_unreviewed)

    # Apply date filtering for rejected applications
    if start_date_rejected:
        start_date_rejected = parse_date(start_date_rejected)
        rejected_applications = rejected_applications.filter(timestamp__gte=start_date_rejected)
    if end_date_rejected:
        end_date_rejected = parse_date(end_date_rejected)
        rejected_applications = rejected_applications.filter(timestamp__lte=end_date_rejected)

    # Apply date filtering for shortlisted applications
    if start_date_shortlisted:
        start_date_shortlisted = parse_date(start_date_shortlisted)
        shortlisted_applications = shortlisted_applications.filter(timestamp__gte=start_date_shortlisted)
    if end_date_shortlisted:
        end_date_shortlisted = parse_date(end_date_shortlisted)
        shortlisted_applications = shortlisted_applications.filter(timestamp__lte=end_date_shortlisted)

    # Paginate the results for each application group
    paginator_unreviewed = Paginator(unreviewed_applications, 10)
    page_obj_unreviewed = paginator_unreviewed.get_page(request.GET.get('page_unreviewed'))

    paginator_rejected = Paginator(rejected_applications, 10)
    page_obj_rejected = paginator_rejected.get_page(request.GET.get('page_rejected'))

    paginator_shortlisted = Paginator(shortlisted_applications, 10)
    page_obj_shortlisted = paginator_shortlisted.get_page(request.GET.get('page_shortlisted'))

    # Debug: Print the items in the current pages
    print("Unreviewed Applications on this page:")
    for application in page_obj_unreviewed:
        print(application)

    print("Rejected Applications on this page:")
    for application in page_obj_rejected:
        print(application)

    print("Shortlisted Applications on this page:")
    for application in page_obj_shortlisted:
        print(application)

    return render(request, 'internship_enquiries.html', {
        'page_obj_unreviewed': page_obj_unreviewed,
        'page_obj_rejected': page_obj_rejected,
        'page_obj_shortlisted': page_obj_shortlisted,
        'start_date_unreviewed': start_date_unreviewed,
        'end_date_unreviewed': end_date_unreviewed,
        'start_date_rejected': start_date_rejected,
        'end_date_rejected': end_date_rejected,
        'start_date_shortlisted': start_date_shortlisted,
        'end_date_shortlisted': end_date_shortlisted,
    })


def delete_internship_application(request, application_id):
    try:
        application = get_object_or_404(InternshipApplication, id=application_id)
        application.delete()
        return JsonResponse({'status': 'success', 'message': 'Application deleted successfully'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)



def view_resume(request, application_id):
    try:
        # Get the application instance
        application = InternshipApplication.objects.get(id=application_id)

        # Check if the resume exists
        if application.resume:
            # Create an HTTP response with the binary data
            response = HttpResponse(application.resume, content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="resume.pdf"'  # Inline to view in browser
            return response
        else:
            raise Http404("Resume not found")
    except InternshipApplication.DoesNotExist:
        raise Http404("Application does not exist")
    
    
    
@login_required
def delete_application(request, pk):
    application = get_object_or_404(InternshipApplication, pk=pk)
    
    if request.method == 'POST':
        application.delete()
        messages.success(request, 'Internship application deleted successfully.')
        return redirect('internship_enquiries')  # Adjust this to the correct view name
    
    return redirect('internship_enquiries')  # Fall back in case of a non-POST request
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def internship_enquiries(request):
    return render(request, 'internship_enquiries.html', {'active': 'internship_enquiries'})

def update_internship_status(request, candidate_id, new_status):
    try:
        # Find the application by its ID
        application = get_object_or_404(InternshipApplication, id=candidate_id)

        # Check if the new status is valid (define your own statuses if necessary)
        if new_status not in ['unreviewed', 'shortlisted', 'rejected']:
            return JsonResponse({'status': 'error', 'message': 'Invalid status'}, status=400)

        # Update the application's status
        application.status = new_status
        application.save()

        return JsonResponse({'status': 'success', 'message': 'Status updated successfully'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required

def job_applications(request):
    # Get date filters from GET parameters
    start_date_unreviewed = request.GET.get('start_date_unreviewed')
    end_date_unreviewed = request.GET.get('end_date_unreviewed')

    start_date_rejected = request.GET.get('start_date_rejected')
    end_date_rejected = request.GET.get('end_date_rejected')

    start_date_shortlisted = request.GET.get('start_date_shortlisted')
    end_date_shortlisted = request.GET.get('end_date_shortlisted')

    # Fetch candidates based on their status
    unreviewed_candidates = JobFormSubmission.objects.filter(status='unreviewed')
    rejected_candidates = JobFormSubmission.objects.filter(status='rejected')
    print (unreviewed_candidates)
    shortlisted_candidates = JobFormSubmission.objects.filter(status='shortlisted')
    print(shortlisted_candidates)
    # Apply date filtering for unreviewed candidates
    if start_date_unreviewed:
        start_date_unreviewed = parse_date(start_date_unreviewed)
        if start_date_unreviewed:
            unreviewed_candidates = unreviewed_candidates.filter(created_at__gte=start_date_unreviewed)

    if end_date_unreviewed:
        end_date_unreviewed = parse_date(end_date_unreviewed)
        if end_date_unreviewed:
            unreviewed_candidates = unreviewed_candidates.filter(created_at__lte=end_date_unreviewed)

    # Apply date filtering for rejected candidates
    if start_date_rejected:
        start_date_rejected = parse_date(start_date_rejected)
        if start_date_rejected:
            rejected_candidates = rejected_candidates.filter(created_at__gte=start_date_rejected)

    if end_date_rejected:
        end_date_rejected = parse_date(end_date_rejected)
        if end_date_rejected:
            rejected_candidates = rejected_candidates.filter(created_at__lte=end_date_rejected)

    # Apply date filtering for shortlisted candidates
    if start_date_shortlisted:
        start_date_shortlisted = parse_date(start_date_shortlisted)
        if start_date_shortlisted:
            shortlisted_candidates = shortlisted_candidates.filter(created_at__gte=start_date_shortlisted)

    if end_date_shortlisted:
        end_date_shortlisted = parse_date(end_date_shortlisted)
        if end_date_shortlisted:
            shortlisted_candidates = shortlisted_candidates.filter(created_at__lte=end_date_shortlisted)

    # Paginate the results for each candidate group
    paginator_unreviewed = Paginator(unreviewed_candidates, 10)  # Show 10 unreviewed candidates per page
    page_number_unreviewed = request.GET.get('page_unreviewed')
    page_obj_unreviewed = paginator_unreviewed.get_page(page_number_unreviewed)

    paginator_rejected = Paginator(rejected_candidates, 10)  # Show 10 rejected candidates per page
    page_number_rejected = request.GET.get('page_rejected')
    page_obj_rejected = paginator_rejected.get_page(page_number_rejected)

    paginator_shortlisted = Paginator(shortlisted_candidates, 10)  # Show 10 shortlisted candidates per page
    page_number_shortlisted = request.GET.get('page_shortlisted')
    page_obj_shortlisted = paginator_shortlisted.get_page(page_number_shortlisted)
    print (page_obj_shortlisted)


    return render(request, 'job_applications.html', {
        'page_obj_unreviewed': page_obj_unreviewed,
        'page_obj_rejected': page_obj_rejected,
        'page_obj_shortlisted': page_obj_shortlisted,
        'start_date_unreviewed': start_date_unreviewed,
        'end_date_unreviewed': end_date_unreviewed,
        'start_date_rejected': start_date_rejected,
        'end_date_rejected': end_date_rejected,
        'start_date_shortlisted': start_date_shortlisted,
        'end_date_shortlisted': end_date_shortlisted,
    })


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def ip_address(request):
    return render(request, 'ip_address.html', {'active': 'ip_address'})



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def push_notifications(request):
    return render(request, 'push_notifications.html', {'active': 'push_notifications'})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def current_user(request):
    return render(request, 'current_user.html', {'active': 'current_user'})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def top_cities(request):
    return render(request, 'top_cities.html', {'active': 'top_cities'})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def google_analytics(request):
    return render(request, 'google_analytics.html', {'active': 'google_analytics'})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def heatmap(request):
    return render(request, 'heatmap.html', {'active': 'heatmap'})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def report_generation(request):
    return render(request, 'report_generation.html', {'active': 'report_generation'})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def blog(request):
    return render(request, 'blog.html', {'active': 'blog'})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def admin_base(request):
    return render(request, 'email_notifications.html', {'active': 'admin_base'})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def enquiry_list(request):
    # Get all enquiries
    enquiries = Enquiry.objects.all()

    # Date filtering
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        enquiries = enquiries.filter(timestamp__range=[start_date, end_date])

    # Pagination
    paginator = Paginator(enquiries, 10)  # Show 10 enquiries per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'contactus.html', {'page_obj': page_obj})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def delete_enquiry(request, enquiry_id):
    enquiry = get_object_or_404(Enquiry, id=enquiry_id)
    enquiry.delete()
    return redirect('enquiry_list')  # Redirect to the list after deletion


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def culture(request):
    return render(request, 'culture.html', {'active': 'culture'})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def client(request):
    return render(request, 'client.html', {'active': 'client'})

# views.py


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def delete_portfolio(request, pk):
    if request.method == 'DELETE':
        # Get the portfolio item by primary key (pk)
        portfolio = get_object_or_404(Portfolio, pk=pk)
        portfolio.delete()  # Delete the portfolio item
        return JsonResponse({'message': 'Portfolio deleted successfully.'}, status=200)

    return JsonResponse({'error': 'Invalid request method.'}, status=400)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def portfolio_post(request):
    portfolios = Portfolio.objects.all().order_by('-created_at')  # Order by created_at for newest first
    paginator = Paginator(portfolios, 10)  # Show 10 portfolios per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.method == 'POST':
        if 'delete_portfolio' in request.POST:
            portfolio_id = request.POST.get('portfolio_id')
            portfolio = get_object_or_404(Portfolio, id=portfolio_id)
            portfolio.delete()

            # Return a success message as JSON after deletion
            return redirect('portfolio_management')

        # If not delete, proceed with portfolio creation
        portfolio_form = PortfolioForm(request.POST, request.FILES)

        if portfolio_form.is_valid():
            portfolio = portfolio_form.save()

            # Handle multiple images
            images = request.FILES.getlist('images')  # Get the list of uploaded files
            for image in images:
                PortfolioImage.objects.create(portfolio=portfolio, image=image)

            # Return a success message as JSON
            return JsonResponse({'success': True, 'message': 'Portfolio saved successfully!'})

        else:
            # Return error message in JSON if form is invalid
            return JsonResponse({'success': False, 'message': 'Form validation failed. Please check your inputs.'})

    else:
        portfolio_form = PortfolioForm()

    portfolios = Portfolio.objects.all()
    context = {
        'portfolio_form': portfolio_form,
        'portfolios': portfolios,
        'active': 'portfolio_post', 
         'page_obj':page_obj,

    }
    return render(request, 'portfolio_post.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def portfolio_edit(request, pk):
    portfolio = get_object_or_404(Portfolio, id=pk)

    if request.method == 'POST':
        portfolio_form = PortfolioForm(request.POST, request.FILES, instance=portfolio)
        
        if portfolio_form.is_valid():
            portfolio_form.save()

            # Handle new image uploads
            images = request.FILES.getlist('images')  # Get the list of uploaded files
            for image in images:
                PortfolioImage.objects.create(portfolio=portfolio, image=image)

            # Handle existing image deletions
            if 'delete_images' in request.POST:
                delete_image_ids = request.POST.getlist('delete_images')
                PortfolioImage.objects.filter(id__in=delete_image_ids).delete()

            # Return a success message as JSON
            return JsonResponse({'success': True, 'message': 'Portfolio updated successfully!'})
        else:
            # Return an error message as JSON
            return JsonResponse({'success': False, 'message': 'Form validation failed. Please check your inputs.'})

    else:
        portfolio_form = PortfolioForm(instance=portfolio)

    context = {
        'portfolio_form': portfolio_form,
        'portfolio': portfolio,
    }
    return render(request, 'portfolio_edit.html', context)









@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def life_at_pinesphere_create(request):
    form = LifeAtPinesphereForm()  # Default form initialization
    
    # Handle form submission
    if request.method == 'POST':
        form = LifeAtPinesphereForm(request.POST, request.FILES)
        
        if form.is_valid():
            # Create a new instance explicitly without overriding an existing one
            new_entry = life_at_pinesphere(
                title=form.cleaned_data['title'], 
                content=form.cleaned_data['content'], 
                url=form.cleaned_data['url'], 
                image=form.cleaned_data.get('image')  # handle optional fields like image
            )
            new_entry.save()  # Save the new instance
            return JsonResponse({'success': True, 'message': 'Form submitted successfully!'})
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'message': 'Form validation failed.', 'errors': errors})
    
    # Handle listing with pagination
    page_number = request.GET.get('page', 1)  # Get page number from request
    life_entries = life_at_pinesphere.objects.all()
    paginator = Paginator(life_entries, 10)  # Show 10 entries per page
    page_obj = paginator.get_page(page_number)
    
    context = {
        'form': form,
        'page_obj': page_obj
    }
    
    return render(request, "life_at_pine_post.html", context)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def delete_life_at_pinesphere(request, pk):
    if request.method == "POST":
        life_item = get_object_or_404(life_at_pinesphere, pk=pk)
        life_item.delete()
        return JsonResponse({'success': True, 'message': 'Item deleted successfully!'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

def apply(request):
    if request.method == 'POST':
        try:
            # Extract fields from request.POST
            job_id = request.POST.get('job_id')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            dob = request.POST.get('dob')
            email_address = request.POST.get('email_address')
            phone_number = request.POST.get('phone_number')
            location = request.POST.get('location')
            experience = request.POST.get('experience')
            ctc = request.POST.get('ctc')
            notice_period = request.POST.get('notice_period')
            willing_to_relocate = request.POST.get('relocate')
            description = request.POST.get('message')
            agree_to_terms = request.POST.get('by_clicking_on_the_submit_button_you_agree_with_the_terms_condit') == '1'
            subscribe_me = request.POST.get('subscribe_me') == '1'
            requirements = Job_Post.objects.get(id=job_id)

            resume = request.FILES.get('resume')

            # Check for recent application
            three_months_ago = timezone.now() - timedelta(days=90)
            recent_application = JobFormSubmission.objects.filter(
                phone_number=phone_number,
                created_at__gte=three_months_ago
            ).exists()

            if recent_application:
                return JsonResponse({'status': 'error', 'message': 'You have already applied within the last three months. Please apply later.'}, status=200)

            recent_application = JobFormSubmission.objects.filter(
                email_address=email_address,
                created_at__gte=three_months_ago
            ).exists()
            if recent_application:
                return JsonResponse({'status': 'error', 'message': 'You have already applied within the last three months. Please apply later.'}, status=200)

            # Save the model instance
            job_submission = JobFormSubmission(
                job_id=requirements.title,
                first_name=first_name,
                last_name=last_name,
                date_of_birth=dob,
                email_address=email_address,
                phone_number=phone_number,
                location=location,
                experience=experience,
                ctc=ctc,
                notice_period=notice_period,
                willing_to_relocate=willing_to_relocate,
                description=description,
                resume=resume,
                agree_to_terms=agree_to_terms,
                subscribe_me=subscribe_me
            )
            job_submission.save()
            if subscribe_me:
                newsletter_signups(email_address)
            thankyoumail(email_address)

            return JsonResponse({'status': 'success', 'message': 'Form submitted successfully!'}, status=200)

        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'status': 'error', 'message': 'An error occurred while processing your request. Please try again.'}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

import logging

def newsletter_signups(email):
    """Handle newsletter signup process."""
    try:
        # Check if the email already exists in the database
        newsletter_signup = NewsletterSubscriber.objects.get(email=email)
        print(newsletter_signup)

        if newsletter_signup.active:
            print(f"Email {email} is already subscribed.")

        # If the subscription exists but is inactive, activate it
        newsletter_signup.active = True
        newsletter_signup.save()
        print(f"Reactivated subscription for {email}.")
        print("Subscription activated.")

    except NewsletterSubscriber.DoesNotExist:
        # If the email doesn't exist, create a new subscriber
        newsletter_signup = NewsletterSubscriber.objects.create(email=email, active=True)
        print(f"Created new subscription for {email}.")
        print("New subscriber created.")

    # Generate unsubscribe URL
    try:
        unsubscribe_url = f"http://localhost:8000/unsubscribe/{email}/"
        print(f"Unsubscribe URL generated: {unsubscribe_url}")
    except Exception as e:
        print(f"Error generating unsubscribe URL: {e}")

    # Render the email template
    template_dir = os.path.join(settings.BASE_DIR, 'templates', 'Mail_Templates')
    try:
        message_html = render_to_string(os.path.join(template_dir, 'subscribed.html'), {'unsubscribe_url': unsubscribe_url})
        message_plain = strip_tags(message_html)
        print("Email template rendered successfully.")
    except Exception as e:
        print(f"Error rendering email template for {email}: {e}")

    # Send confirmation email
    try:
        send_mail(
            'Newsletter Signup Confirmation',
            message_plain,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            html_message=message_html,
            fail_silently=False,  # Ensure that exceptions are raised if email fails to send
        )
        print(f"Confirmation email sent to {email}.")
    except Exception as e:
        print(f"Error sending email to {email}: {e}")



def thankyoumail(email):
    """Handle newsletter signup process."""
    try:
        # Check if the email already exists in the database
        newsletter_signup = NewsletterSubscriber.objects.get(email=email)
        print(newsletter_signup)

        if newsletter_signup.active:
            print(f"Email {email} is already subscribed.")

        # If the subscription exists but is inactive, activate it
        newsletter_signup.active = True
        newsletter_signup.save()
        print(f"Reactivated subscription for {email}.")
        print("Subscription activated.")

    except NewsletterSubscriber.DoesNotExist:
        # If the email doesn't exist, create a new subscriber
        newsletter_signup = NewsletterSubscriber.objects.create(email=email, active=True)
        print(f"Created new subscription for {email}.")
        print("New subscriber created.")

    # Generate unsubscribe URL
    try:
        unsubscribe_url = f"http://localhost:8000/unsubscribe/{email}/"
        print(f"Unsubscribe URL generated: {unsubscribe_url}")
    except Exception as e:
        print(f"Error generating unsubscribe URL: {e}")

    # Render the email template
    template_dir = os.path.join(settings.BASE_DIR, 'templates', 'Mail_Templates')
    try:
        message_html = render_to_string(os.path.join(template_dir, 'subscribed.html'), {'unsubscribe_url': unsubscribe_url})
        message_plain = strip_tags(message_html)
        print("Email template rendered successfully.")
    except Exception as e:
        print(f"Error rendering email template for {email}: {e}")

    # Send confirmation email
    try:
        send_mail(
            'Newsletter Signup Confirmation',
            message_plain,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            html_message=message_html,
            fail_silently=False,  # Ensure that exceptions are raised if email fails to send
        )
        print(f"Confirmation email sent to {email}.")
    except Exception as e:
        print(f"Error sending email to {email}: {e}")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def edit_life_at_pinesphere(request, pk):
    life_item = get_object_or_404(life_at_pinesphere, pk=pk)

    if request.method == 'POST':
        form = LifeAtPinesphereForm(request.POST, request.FILES, instance=life_item)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Entry updated successfully!'})  # Change to your desired redirect URL
    else:
        form = LifeAtPinesphereForm(instance=life_item)

    return render(request, 'life_at_pine_edit.html', {'form': form, 'image': life_item.image.url, 'pk':pk})

def save_internship_application(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        student_graduate = request.POST.get('student_or_grad')
        department_college = request.POST.get('dept_clg')
        year_of_passing = request.POST.get('year_of_passing')
        email_address = request.POST.get('email_address')
        phone_number = request.POST.get('phone_number')
        resume_file = request.FILES.get('resume')
        internship_domain = request.POST.get('internship_domain')
        duration = request.POST.get('duration')
        description = request.POST.get('description')
        terms_agreed = request.POST.get('by_clicking_on_the_submit_button_you_agree_with_the_terms_condit') == '1'
        newsletter_subscription = request.POST.get('subscribe_me')
        if newsletter_subscription is None:
                newsletter_subscription = False


        # Read the resume file as binary
        resume_data = None
        if resume_file:
            resume_data = resume_file.read()  # Read the file content as binary data
            
        three_months_ago = timezone.now() - timedelta(days=90)
        recent_application = InternshipApplication.objects.filter(
                phone_number=phone_number,
                created_at__gte=three_months_ago
            ).exists()

        if recent_application:
                return JsonResponse({'success': True, 'message': 'You have already applied within the last three months. Please apply later.'}, status=200)

        recent_application = InternshipApplication.objects.filter(
                email_address=email_address,
                created_at__gte=three_months_ago
            ).exists()
        if recent_application:
                return JsonResponse({'success': True, 'message': 'You have already applied within the last three months. Please apply later.'}, status=200)

        # Save the application
        application = InternshipApplication(
            first_name=first_name,
            last_name=last_name,
            email_address=email_address,
            student_graduate=student_graduate,
            year_of_passing=year_of_passing,
            department_college=department_college,
            phone_number=phone_number,
            resume=resume_data,  # Save the binary data
            internship_domain=internship_domain,
            duration=duration,
            description=description,
            agree_to_terms=terms_agreed,
            newsletter_subscription=newsletter_subscription
        )
        application.save()
        if newsletter_subscription:
            newsletter_signups(email_address)
        thankyoumail(email_address)
        return JsonResponse({'status': 'success', 'message': 'Application submitted successfully!'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import PineNews

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def pinenews(request):
    if request.method == "POST":
        try:
            # Create and save PineNews object
            pine_news = PineNews(
                title=request.POST.get('title'),
                content=request.POST.get('content'),
                created_by=request.user if request.user.is_authenticated else User.objects.first(),
                index_num=request.POST.get('index_num'),
                learn_more=request.POST.get('url'),
                topic_covered=request.POST.get('topic_covered'),
                image=request.FILES.get('images')  # Single image upload
            )
            pine_news.save()

            # Set success message and return JSON response
            messages.success(request, 'Your Pine News has been submitted successfully!')
            return JsonResponse({'status': 'success'})  # Respond with JSON for AJAX

        except Exception as e:
            # Handle exceptions and return error response
            messages.error(request, f'An error occurred: {str(e)}')
            return JsonResponse({'status': 'error', 'message': str(e)})

    # Handle GET request to display paginated PineNews
    pinenews = PineNews.objects.all().order_by('-created_at')  # Assuming 'created_at' is in the model
    page_number = request.GET.get('page', 1)
    paginator = Paginator(pinenews, 10)  # 10 items per page
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'active': 'pinenews',
        'success': messages.get_messages(request),  # Display success messages
        'error': messages.get_messages(request),  # Display error messages
    }
    return render(request, 'pinenews.html', context)



def update_pine_news(request, pk):
    pine_news = get_object_or_404(PineNews, pk=pk)
    
    print (pine_news.image.url)

    if request.method == "POST":
        print("Received POST request")
        print("POST data:", request.POST)
        print("FILES data:", request.FILES)

        # Update fields directly from request data
        pine_news.title = request.POST.get('title')
        pine_news.content = request.POST.get('content')
        pine_news.index_num = int(request.POST.get('index_num', 0))  # Default to 0 if not present
        pine_news.learn_more = request.POST.get('url')
        pine_news.topic_covered = request.POST.get('topic_covered')

        # Handle image upload
        if 'images' in request.FILES:
            pine_news.image = request.FILES['images']
            print("Uploaded file name:", request.FILES['images'].name)

        # Handle image deletion if requested
        if 'delete_image' in request.POST:
            pine_news.image = None
            print("Image deleted.")

        # Assign created_by
        pine_news.created_by = request.user if request.user.is_authenticated else User.objects.first()

        try:
            pine_news.save()
            print("Pine news saved successfully.")
            return JsonResponse({'status': 'success', 'message': "Your update was successful"}, status=200)
        except Exception as e:
            print("Error while saving pine news:", e)
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    else:
        context = {
            'pine_news': pine_news,
            'existing_image': pine_news.image.url if pine_news.image else None  # Pass existing image URL
        }
        return render(request, 'pinenews_edit.html', context)


def delete_pinenews(request, pk):
    if request.method == 'POST':
        pinenews = get_object_or_404(PineNews, pk=pk)
        pinenews.delete()
        return JsonResponse({'success': True, 'message': 'Pine News deleted successfully.'})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


def serve_image(request, pk):
    # Get the PineNews object based on the primary key
    pine_news = get_object_or_404(PineNews, pk=pk)
    
    # Create an HTTP response with the image data
    response = HttpResponse(pine_news.image, content_type="image/jpeg")  # Adjust content_type based on the image type
    response['Content-Disposition'] = f'inline; filename="image_{pk}.jpg"'  # Optional: Set filename for the browser
    return response


def manage_client_pages(request):
    if request.method == 'POST':
        form = ClientPageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success', 'message': 'Client page created successfully!'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Form is invalid. Please correct the errors.'}, status=400)

    # Handle deletion
    

    client_pages = client_page.objects.all().order_by('index_num')  # Order by index_num or any other field

    # Pagination setup
    paginator = Paginator(client_pages, 10)  # Show 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    form = ClientPageForm()

    context = {
        'form': form,
        'page_obj': page_obj,
    }
    return render(request, 'client.html', context)

def delete_client_page(request):
    if request.method == 'POST':
        delete_id = request.POST.get('delete_id')
        if delete_id:
            page_to_delete = get_object_or_404(client_page, id=delete_id)
            page_to_delete.delete()
            return JsonResponse({'status': 'success', 'message': 'Client page deleted successfully!'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid request.'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)


@login_required
def edit_client_page(request, id):
    client = get_object_or_404(client_page, id=id)
    
    if request.method == 'POST':
        form = ClientPageForm(request.POST, request.FILES, instance=client)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success', 'message': 'Client page updated successfully!'})
        else:
            return JsonResponse({'status': 'error', 'message': 'There was an error updating the client page.'})
    else:
        form = ClientPageForm(instance=client)
    
    context = {
        'form': form,
        'client': client,
    }
    return render(request, 'client_edit.html', context)


def job_post_list_create(request):
    if request.method == 'POST':
        form = JobPostForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success', 'message': 'Job post created successfully!', 'redirect_url': '/some-redirect-url/'})
        else:
            # Get the first error message to show in the alert
            error_message = form.errors.as_text()
            return JsonResponse({'status': 'error', 'message': error_message})
    
    else:
        form = JobPostForm()
    
    jobs = Job_Post.objects.all()
    return render(request, 'job_post_list_create.html', {'form': form, 'jobs': jobs})


# Delete a job post
def job_post_delete(request, pk):
    job_post = get_object_or_404(Job_Post, pk=pk)
    job_post.delete()
    return redirect('job_post_list_create')
from django.http import JsonResponse

def job_post_edit(request, pk):
    job_post = get_object_or_404(Job_Post, pk=pk)
    if request.method == 'POST':
        form = JobPostForm(request.POST, instance=job_post)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success', 'message': 'Job post updated successfully!'})
        else:
            # Return error messages from the form
            return JsonResponse({'status': 'error', 'message': 'There were errors in the form submission.'})
    else:
        form = JobPostForm(instance=job_post)
    return render(request, 'job_post_edit.html', {'form': form, 'pk':pk})



def delete_candidate(request, candidate_id):
    try:
        candidate = get_object_or_404(JobFormSubmission, id=candidate_id)
        candidate.delete()
        return JsonResponse({'status': 'success', 'message': 'Candidate deleted successfully'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
def update_status(request, candidate_id, new_status, email, name):
    try:
        candidate = get_object_or_404(JobFormSubmission, id=candidate_id)

        if new_status not in ['unreviewed', 'shortlisted', 'rejected']:
            return JsonResponse({'status': 'error', 'message': 'Invalid status'}, status=400)

        candidate.status = new_status
        candidate.save()
        
        # Check the status and send an email accordingly
        if new_status in ['shortlisted', 'rejected']:
            # Get the template based on the new status
            template_id = 2 if new_status == 'shortlisted' else 1
            email_template = get_object_or_404(Email_Template_JI, id=template_id)

            # Prepare email content
            subject = email_template.Subject
            content = email_template.content
            footer = email_template.footer

            # Replace {{name}} with the actual name
            full_content = content.replace('{{name}}', name) + f"\n\n{footer}"

            # Send email
            send_mail(
                subject=subject,
                message=full_content,
                from_email='your_email@example.com',  # Replace with your email
                recipient_list=[email],
                fail_silently=False,
            )

        return JsonResponse({'status': 'success', 'message': 'Status updated successfully and email sent'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def product_launchs(request):       
    product_launch = Product_Launch.objects.get(id=1)

    return render(request, 'product_launch.html', {'active': 'product_launch', "product_launch":product_launch})




def send_notifications(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        body = request.POST.get('body')
        url = request.POST.get('url')
        image = request.FILES.get('image')

        # Check for required fields
        if not (title and body and url):
            return JsonResponse({"success": False, "error": "Title, body, and URL are required"}, status=400)

        # Handle file upload
        image_url = None
        if image:
            image_name = default_storage.save(image.name, ContentFile(image.read()))
            image_url = default_storage.url(image_name)

        # Send the notification with the custom URL and image
        try:
            send_not(title, body, image_url, url)
            return JsonResponse({"success": True, "message": "Notification sent successfully!"}, status=200)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False, "error": "Only POST requests are allowed"}, status=405)



def send_not(title, body, image_url, url):
    current_directory = os.path.dirname(os.path.abspath(__file__))
    cred = credentials.Certificate(os.path.join(current_directory, 'pinesphere-c7119-firebase-adminsdk-mtt6j-109b5faa33.json'))

    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)

    tokens = FCMToken.objects.values_list('token', flat=True)

    for token in tokens:
        message = messaging.Message(
            webpush=messaging.WebpushConfig(
                
                data={
                    "click_action": url,  # Pass the URL dynamically
                    "image": image_url if image_url else "",  # Dynamic image URL
                    "title": title,  # Pass title
                    "body": body  # Pass body
                }
            ),
            token=token
        )

        try:
            response = messaging.send(message)
            print(f"Successfully sent message to {token}: {response}")
        except messaging.UnregisteredError:
            print(f"Token {token} not registered, removing from database.")
            FCMToken.objects.filter(token=token).delete()
        except Exception as e:
            print(f"An error occurred while sending to {token}: {e}")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def produch_launch_edit(request, product_launch_id):
    try:
        # Get the product launch instance
        product_launch = Product_Launch.objects.get(id=product_launch_id)

        if request.method == 'POST':
            # Update the other fields
            product_launch.title = request.POST.get('title', product_launch.title)
            product_launch.description = request.POST.get('description', product_launch.description)
            product_launch.url = request.POST.get('url', product_launch.url)

            # Handle the main image and logo
            if 'image' in request.FILES:
                product_launch.image = save_image_with_specific_name_product(request.FILES['image'], 'image_title_product')
            if 'logo' in request.FILES:
                product_launch.logo = save_image_with_specific_name_product(request.FILES['logo'], 'logo_product')

            # Save the product launch object with updated fields
            product_launch.save()
            active_subscribers = NewsletterSubscriber.objects.filter(active=True)
            for subscriber in active_subscribers:
                    email_address = subscriber.email
            # Optionally send a confirmation email (if needed)
                    send_confirmation_email_product(
                        product_launch.title,
                        product_launch.description,
                        product_launch.url,
                        email_address
                    )

            # Return a success JSON response
            return JsonResponse({
                'status': 'success',
                'message': 'Product Launch updated successfully!'
            })

        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid request method'
            }, status=400)

    except Product_Launch.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Product Launch does not exist'
        }, status=404)
        
        
def send_confirmation_email_product(main_title, main_content, main_url, email_address):
    reply_subject = 'Pinesphere New Product Launch'
    unsubscribe_url = f"http://localhost:8000/unsubscribe/{email_address}/"
    context = {
        'unsubscribe_url':unsubscribe_url,
        'main_title': main_title,
        'main_content': main_content,
        'main_url': main_url,
        'image_title_cid': 'image_title_cid',
        'logo_cid':'logo_cid'
    }
    reply_message = render_to_string('Mail_Templates/product_launch.html', context)

    email = EmailMultiAlternatives(
        subject=reply_subject,
        body='',  # Empty plain text version
        from_email='vandhana.jayakumar1106@gmail.com',
        to=[email_address]
    )

    email.attach_alternative(reply_message, "text/html")

    # Embed images in the email template using CID
    attach_images_to_email_product(email)

    email.send()

def attach_images_to_email_product(email):
    static_image_paths = [
        ('assets/Images/pine_images/image_title_product.jpg', 'image_title_cid'),
        ('assets/Images/pine_images/logo_product.png', 'logo_cid'),
    ]

    for image_path, image_cid in static_image_paths:
        full_image_path = os.path.join(settings.STATICFILES_DIRS[0], image_path)
        with open(full_image_path, 'rb') as img:
            mime_image = MIMEImage(img.read())
            mime_image.add_header('Content-ID', f'<{image_cid}>')
            email.attach(mime_image)

def save_image_with_specific_name_product(uploaded_file, filename_base):
    """
    Save the uploaded image with a specific filename, overwriting if it exists.
    """
    # Get the file extension from the uploaded file (e.g., '.jpg', '.png')
    extension = os.path.splitext(uploaded_file.name)[1]  # Get the file extension
    
    # Ensure the extension is valid (e.g., only allow certain image types)
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    if extension.lower() not in valid_extensions:
        raise ValueError("Invalid file format. Only .jpg, .jpeg, .png, and .gif files are allowed.")
    
    # Define the directory where images will be saved
    directory = os.path.join(settings.MEDIA_ROOT, 'static/assets/Images/pine_images/')

    # Ensure the directory exists
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Construct the full file path with the correct file extension
    file_path = os.path.join(directory, f"{filename_base}{extension}")

    # Check if file already exists, and remove it if it does
    if os.path.exists(file_path):
        os.remove(file_path)

    # Save the uploaded file with the specified filename
    with open(file_path, 'wb+') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)

    # Return the relative path to store in the model
    return f'assets/Images/pine_images/{filename_base}{extension}'



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def newsletter(request):
    newsletter = Newsletter.objects.get(id=1)

    return render(request, 'newsletter.html', {'active': 'newsletter', "newsletter":newsletter})



def edit_newsletter(request, newsletter_id):
    try:
        # Get the newsletter instance
        newsletter = Newsletter.objects.get(id=newsletter_id)

        if request.method == 'POST':
            # Update the other fields
            newsletter.title = request.POST.get('title', newsletter.title)
            newsletter.description = request.POST.get('description', newsletter.description)
            newsletter.contact_mail = request.POST.get('contact_mail', newsletter.contact_mail)
            newsletter.contact_number = request.POST.get('contact_number', newsletter.contact_number)
            newsletter.url = request.POST.get('url', newsletter.url)
            newsletter.subtopic1_heading = request.POST.get('subtopic1_heading', newsletter.subtopic1_heading)
            newsletter.subtopic1_content = request.POST.get('subtopic1_content', newsletter.subtopic1_content)
            newsletter.subtopic1_url = request.POST.get('subtopic1_url', newsletter.subtopic1_url)
            newsletter.subtopic2_heading = request.POST.get('subtopic2_heading', newsletter.subtopic2_heading)
            newsletter.subtopic2_content = request.POST.get('subtopic2_content', newsletter.subtopic2_content)
            newsletter.subtopic2_url = request.POST.get('subtopic2_url', newsletter.subtopic2_url)

            # Handle the images for main newsletter and subtopics
            if 'image' in request.FILES:
                newsletter.image = save_image_with_specific_name(request.FILES['image'], 'image_title')
            if 'logo' in request.FILES:
                newsletter.logo = save_image_with_specific_name(request.FILES['logo'], 'logo')
            if 'subtopic1_image' in request.FILES:
                newsletter.subtopic1_image = save_image_with_specific_name(request.FILES['subtopic1_image'], 'subtopic1_image')
            if 'subtopic2_image' in request.FILES:
                newsletter.subtopic2_image = save_image_with_specific_name(request.FILES['subtopic2_image'], 'subtopic2_image')

            # Save the newsletter object with updated fields
            newsletter.save()
            active_subscribers = NewsletterSubscriber.objects.filter(active=True)
            for subscriber in active_subscribers:
                    email_address = subscriber.email
            # Send confirmation email
                    send_confirmation_email(
                newsletter.title, newsletter.description, newsletter.contact_mail, newsletter.contact_number,
                newsletter.url, newsletter.subtopic1_heading, newsletter.subtopic1_content,
                newsletter.subtopic1_url, newsletter.subtopic2_heading, newsletter.subtopic2_content,
                newsletter.subtopic2_url, email_address
            )

            # Return JSON response for success
            return JsonResponse({"message": "Newsletter updated successfully"}, status=200)

        else:
            return JsonResponse({"message": "Invalid request method"}, status=400)

    except Newsletter.DoesNotExist:
        # Return JSON response for error if newsletter doesn't exist
        return JsonResponse({"message": "Newsletter does not exist"}, status=404)

    except Exception as e:
        # Return JSON response for any other errors
        return JsonResponse({"message": f"An error occurred: {str(e)}"}, status=500)

import os
from django.conf import settings

def save_image_with_specific_name(uploaded_file, filename_base):
    """
    Save the uploaded image with a specific filename, overwriting if it exists.
    """
    # Get the file extension from the uploaded file (e.g., '.jpg', '.png')
    extension = os.path.splitext(uploaded_file.name)[1]  # Get the file extension
    
    # Ensure the extension is valid (e.g., only allow certain image types)
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    if extension.lower() not in valid_extensions:
        raise ValueError("Invalid file format. Only .jpg, .jpeg, .png, and .gif files are allowed.")
    
    # Define the directory where images will be saved
    directory = os.path.join(settings.MEDIA_ROOT, 'static/assets/Images/pine_images/')

    # Ensure the directory exists
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Construct the full file path with the correct file extension
    file_path = os.path.join(directory, f"{filename_base}{extension}")

    # Check if file already exists, and remove it if it does
    if os.path.exists(file_path):
        os.remove(file_path)

    # Save the uploaded file with the specified filename
    with open(file_path, 'wb+') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)

    # Return the relative path to store in the model
    return f'assets/Images/pine_images/{filename_base}{extension}'







def send_confirmation_email(main_title, main_content,contact_mail,contact_number, main_url,topic_one_heading,topic_one_content,
                            topic_one_link,topic_two_heading,topic_two_content,topic_two_link, email_address):
    reply_subject = 'Thank you for contacting us!'
    unsubscribe_url = f"http://localhost:8000/unsubscribe/{email_address}/"

    context = {
        'unsubscribe_url':unsubscribe_url,
        'main_title': main_title,
        'main_content': main_content,
        'contact_number':contact_number,
        'contact_mail':contact_mail,
        'main_url': main_url,
        'topic_one_heading': topic_one_heading,
        'topic_one_content': topic_one_content,
        'topic_one_link': topic_one_link,
        'topic_two_heading': topic_two_heading,
        'topic_two_content': topic_two_content,
        'topic_two_link': topic_two_link,
        'image_title_cid': 'image_title_cid',
        'subtopic1_image_cid': 'subtopic1_image_cid',
        'subtopic2_image_cid': 'subtopic2_image_cid',
        'logo_cid':'logo_cid'
    }
    reply_message = render_to_string('Mail_Templates/Newsletter_template.html', context)

    email = EmailMultiAlternatives(
        subject=reply_subject,
        body='',  # Empty plain text version
        from_email='vandhana.jayakumar1106@gmail.com',
        to=[email_address]
    )

    email.attach_alternative(reply_message, "text/html")

    # Embed images in the email template using CID
    attach_images_to_email(email)

    email.send()

def attach_images_to_email(email):
    static_image_paths = [
        ('assets/Images/pine_images/image_title.jpg', 'image_title_cid'),
        ('assets/Images/pine_images/logo.png', 'logo_cid'),
        ('assets/Images/pine_images/subtopic1_image.jpg', 'subtopic1_image_cid'),
        ('assets/Images/pine_images/subtopic2_image.jpg', 'subtopic2_image_cid')
    ]

    for image_path, image_cid in static_image_paths:
        full_image_path = os.path.join(settings.STATICFILES_DIRS[0], image_path)
        with open(full_image_path, 'rb') as img:
            mime_image = MIMEImage(img.read())
            mime_image.add_header('Content-ID', f'<{image_cid}>')
            email.attach(mime_image)
            

def newsletter_subscribers_report(request):
    subscribers = NewsletterSubscriber.objects.all()

    # Handle delete request
    if 'delete' in request.GET:
        subscriber_id = request.GET.get('delete')
        subscriber = get_object_or_404(NewsletterSubscriber, id=subscriber_id)
        subscriber.delete()
        return redirect('newsletter_subscribers_report')  # Redirect after deletion

    # Handle toggle request
    if 'toggle' in request.GET:
        subscriber_id = request.GET.get('toggle')
        subscriber = get_object_or_404(NewsletterSubscriber, id=subscriber_id)
        subscriber.active = not subscriber.active  # Toggle the active status
        subscriber.save()
        return JsonResponse({'active': subscriber.active})  # Return the new status as JSON

    # Handle filtering by date
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

        # Make datetime objects timezone-aware
        start_date = timezone.make_aware(start_date, timezone.get_current_timezone())
        end_date = timezone.make_aware(end_date, timezone.get_current_timezone())

        # Filter subscribers by the date range
        subscribers = subscribers.filter(subscribed_at__range=[start_date, end_date])

    # Pagination: Show 20 subscribers per page
    paginator = Paginator(subscribers, 20)  # 20 subscribers per page
    page_number = request.GET.get('page')  # Get the page number from the query parameters
    page_obj = paginator.get_page(page_number)  # Get the relevant subscribers for the current page

    # Handle Excel download request
    

    return render(request, 'subscribers_list.html', {'page_obj': page_obj})


# Save the updated Email Template (AJAX call)
@csrf_exempt  # Ensure CSRF token is handled in frontend
def save_email_template(request):
    if request.method == 'POST':
        try:
            print (44)
            # Load the JSON data from the request body
            data = json.loads(request.body)

            # Get the template ID from the data
            template_id = data.get('template_id')
            if not template_id:
                return JsonResponse({'status': 'error', 'message': 'Template ID is required.'})

            # Retrieve the email template object or return a 404 if not found
            email_template = get_object_or_404(Email_Template_JI, id=template_id)

            # Update the email template fields
            email_template.Title = data.get('title', email_template.Title)
            email_template.Subject = data.get('subject', email_template.Subject)
            email_template.content = data.get('content', email_template.content)
            email_template.footer = data.get('footer', email_template.footer)
            email_template.save()
            print (type(template_id))
            

            # If template_id is 3, send email to all internship applicants
            if template_id == '3':
                applicants = InternshipApplication.objects.all()
                print ('test')

                # Loop through all applicants and send them the email
                for applicant in applicants:
                    subject = email_template.Subject
                    content = f"{email_template.content}\n\n{email_template.footer}"
                    recipient_email = applicant.email_address

                    # Personalize the content if needed, e.g., include applicant's name
                    personalized_content = content.replace('{{first_name}}', applicant.first_name)

                    try:
                        print (55)
                        # Send email (ensure email settings are properly configured in settings.py)
                        send_mail(
                            subject,
                            personalized_content,
                            'vandhana.jayakumar1106@gmail.com',  # Replace with the sender's email
                            [recipient_email],
                            fail_silently=False,
                        )
                        print(f"Email sent successfully to {recipient_email}")

                    except Exception as e:
                        # Print error to terminal if email sending fails
                        print(f"Error sending email to {recipient_email}: {str(e)}")

            # Return success response
            return JsonResponse({'status': 'success', 'message': 'Template updated and emails sent successfully!'})

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data.'})
        except Exception as e:
            # Print any other errors to the terminal
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def email_template_view(request):
    email_templates = Email_Template_JI.objects.all()
    selected_template = None

    # Check if the request method is POST
    if request.method == 'POST':
        selected_template_id = request.POST.get('template_id')  # Get the template ID from POST data
        if selected_template_id:
            selected_template = get_object_or_404(Email_Template_JI, id=selected_template_id)

    # Prepare the context to render the template
    context = {
        'email_templates': email_templates,
        'selected_template': selected_template if selected_template else Email_Template_JI(),  # Provide an empty template if none is selected
        'selected_template_id': selected_template.id if selected_template else None,  # Pass the selected template ID
    }

    return render(request, 'email_notifications.html', context)



def report(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Fetch all reports (from PageView model)
    reports = PageView.objects.all()

    # Handle Excel download request
    

    if start_date and end_date:
        # Convert strings to datetime objects
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

        # Make datetime objects timezone-aware
        start_date = timezone.make_aware(start_date, timezone.get_current_timezone())
        end_date = timezone.make_aware(end_date, timezone.get_current_timezone())

        # Filter reports by the date range
        reports = reports.filter(timestamp__range=[start_date, end_date])

    # Pagination: Show 20 reports per page
    paginator = Paginator(reports, 20)  # 20 reports per page
    page_number = request.GET.get('page')  # Get the page number from the query parameters
    page_obj = paginator.get_page(page_number)  # Get the relevant reports for the current page

    context = {
        'page_obj': page_obj,  # Pass the paginated object to the template
    }

    return render(request, 'report_pages/views_report.html', context)


def job_report(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Fetch all job form submissions
    submissions = JobFormSubmission.objects.all()

    if start_date and end_date:
        # Convert strings to datetime objects
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

        # Make datetime objects timezone-aware
        start_date = timezone.make_aware(start_date, timezone.get_current_timezone())
        end_date = timezone.make_aware(end_date, timezone.get_current_timezone())

        # Filter submissions by the date range
        submissions = JobFormSubmission.objects.filter(submitted_at__range=[start_date, end_date])

    # Pagination: Show 20 submissions per page
    paginator = Paginator(submissions, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Handle Excel download request
    
    context = {
        'page_obj': page_obj,
    }

    return render(request, 'report_pages/job_application_report.html', context)




def newsletter_subscribers_report(request):
    subscribers = NewsletterSubscriber.objects.all()

    # Handle delete request
    if 'delete' in request.GET:
        subscriber_id = request.GET.get('delete')
        subscriber = get_object_or_404(NewsletterSubscriber, id=subscriber_id)
        subscriber.delete()
        return redirect('newsletter_subscribers_report')  # Redirect after deletion

    # Handle toggle request
    if 'toggle' in request.GET:
        subscriber_id = request.GET.get('toggle')
        subscriber = get_object_or_404(NewsletterSubscriber, id=subscriber_id)
        subscriber.active = not subscriber.active  # Toggle the active status
        subscriber.save()
        return JsonResponse({'active': subscriber.active})  # Return the new status as JSON

    # Handle filtering by date
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

        # Make datetime objects timezone-aware
        start_date = timezone.make_aware(start_date, timezone.get_current_timezone())
        end_date = timezone.make_aware(end_date, timezone.get_current_timezone())

        # Filter subscribers by the date range
        subscribers = subscribers.filter(subscribed_at__range=[start_date, end_date])

    # Pagination: Show 20 subscribers per page
    paginator = Paginator(subscribers, 20)  # 20 subscribers per page
    page_number = request.GET.get('page')  # Get the page number from the query parameters
    page_obj = paginator.get_page(page_number)  # Get the relevant subscribers for the current page

    # Handle Excel download request
    

    return render(request, 'report_pages/subscriber_report.html', {'page_obj': page_obj})



def contactus_report(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Fetch all enquiries from the Enquiry model
    enquiries = Enquiry.objects.all()

    # Filter by date range if provided
    if start_date and end_date:
        # Convert strings to datetime objects
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

        # Make datetime objects timezone-aware
        start_date = timezone.make_aware(start_date, timezone.get_current_timezone())
        end_date = timezone.make_aware(end_date, timezone.get_current_timezone())

        # Filter by the date range
        enquiries = enquiries.filter(timestamp__range=[start_date, end_date])

    # Pagination: Show 20 enquiries per page
    paginator = Paginator(enquiries, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,  # Pass paginated enquiries to the template
    }

    return render(request, 'report_pages/contactus_report.html', context)



def internship_report(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Fetch all reports (from PageView model)
    reports = InternshipApplication.objects.all()

    # Handle Excel download request
    

    if start_date and end_date:
        # Convert strings to datetime objects
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

        # Make datetime objects timezone-aware
        start_date = timezone.make_aware(start_date, timezone.get_current_timezone())
        end_date = timezone.make_aware(end_date, timezone.get_current_timezone())

        # Filter reports by the date range
        reports = reports.filter(timestamp__range=[start_date, end_date])

    # Pagination: Show 20 reports per page
    paginator = Paginator(reports, 20)  # 20 reports per page
    page_number = request.GET.get('page')  # Get the page number from the query parameters
    page_obj = paginator.get_page(page_number)  # Get the relevant reports for the current page

    context = {
        'page_obj': page_obj,  # Pass the paginated object to the template
    }

    return render(request, 'report_pages/internship_report.html', context)


def sustainability (request):
    return render(request, 'frontend_templates/sustainability.html')
def recognition (request):
    return render(request, 'frontend_templates/recognition.html')
def ourbrand(request):
    return render(request, 'frontend_templates/ourbrand.html')

def investors(request):
    return render(request, 'frontend_templates/investors.html')
    
def customer(request):
    return render(request, 'frontend_templates/customer.html')

def whypine(request):
    return render(request, 'frontend_templates/whypine.html')

def capabilities(request):
    return render(request, 'frontend_templates/capabilities.html')

def industries(request):
    return render(request, 'frontend_templates/industries.html')

def Industries_services(request):
    return render(request, 'frontend_templates/Industries_services.html')

def case_studies(request):
    return render(request, 'frontend_templates/case_studies.html')

def analyst_insights(request):
    return render(request, 'frontend_templates/analyst_insights.html')

def View(request):
    return render(request, 'frontend_templates/View.html')

def corporate (request):
    return render(request, 'frontend_templates/corporate.html')

def pineway (request):
    return render(request, 'frontend_templates/pineway.html')
def insights (request):
    return render(request, 'frontend_templates/insights.html')

def Foundation (request):
    return render(request, 'frontend_templates/Foundation.html')

def social_responsibility (request):
    return render(request, 'frontend_templates/social_responsibility.html')

def education (request):
    return render(request, 'frontend_templates/education.html')