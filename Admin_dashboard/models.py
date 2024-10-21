from django.db import models
import uuid
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone


class PageView(models.Model):
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(default=timezone.now)
    city = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    device_type = models.CharField(max_length=255, null=True, blank=True)
    user_unique_id = models.UUIDField(default=uuid.uuid4, editable=False)  # Unique user ID
    user_agent = models.CharField(max_length=1000)
    user_browser = models.CharField(max_length=100)
    def __str__(self):
        return f'{self.city} {self.device_type} - {self.ip_address}'

class PineNews(models.Model):
    index_num = models.IntegerField()
    title = models.CharField(max_length=700)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    topic_covered = models.TextField(null=True)
    learn_more = models.CharField(max_length=500)
    image = models.ImageField(upload_to='static/media/', null=True, blank=True)


class FCMToken(models.Model):
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.token



class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.email


class MailTemplate(models.Model):
    subject = models.CharField(max_length=500)
    body = models.TextField()
    Footer = models.TextField()
    backgorund = models.ImageField(upload_to='assets/images/pine_images/')
    
    def __str__(self):
        return self.subject
    
    
    
class Job(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
  
class life_at_pinesphere(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='assets/images/pine_images/')
    url = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    
 
class Portfolio(models.Model):
    index_num = models.IntegerField()
    logo = models.ImageField(upload_to='assets/images/pine_images/')
    title = models.CharField(max_length=700)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    client = models.CharField(max_length=255)
    developed_using = models.CharField(max_length=255)
    purpose = models.CharField(max_length=255)
    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Portfolio"

class PortfolioImage(models.Model):
    portfolio = models.ForeignKey(Portfolio, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='assets/images/pine_images/', blank=True, null=True)

    def __str__(self):
        return f"Image for {self.portfolio.title}"

class client_page(models.Model):
    index_num = models.IntegerField()
    image = models.ImageField(upload_to='assets/Images/pine_images/')
    image2 = models.ImageField(upload_to='assets/Images/pine_images/')
    Title = models.CharField(max_length=100)
    url = models.CharField(max_length=500)
    
    
class Job_Post (models.Model):
    index_num = models.IntegerField()
    head_tag = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    experience = models.CharField(max_length=255)
    
class JobFormSubmission(models.Model):
    STATUS_CHOICES = [
        ('unreviewed', 'Unreviewed'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
    ]
    job_id = models.CharField(max_length=200)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    email_address = models.EmailField(max_length=254)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255)
    experience = models.CharField(max_length=50, choices=[
        ('0-1 Year', '0-1 Year'),
        ('1-2 Years', '1-2 Years'),
        ('2-3 Years', '2-3 Years'),
        ('More than 3 years', 'More than 3 years')
    ])
    ctc = models.CharField(max_length=255)
    notice_period = models.CharField(max_length=255)
    resume = models.FileField(upload_to='resumes/')
    willing_to_relocate = models.CharField(max_length=50)
    description = models.TextField()
    agree_to_terms = models.BooleanField()
    subscribe_me = models.BooleanField(default=False)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='unreviewed')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.email_address}'

    
    
   
class Template_image(models.Model):
    image1 = models.ImageField(upload_to='assets/Images/pine_images/')
    
    

class Enquiry(models.Model):
    type_of_enquiry = models.CharField(max_length=100)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email_address = models.EmailField()
    phone_number = models.CharField(max_length=15, blank=True)
    message = models.TextField()
    subscribe_me = models.BooleanField(default=False)
    agree_terms = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.email_address}'
    
class InternshipApplication(models.Model):
    STATUS_CHOICES = [
        ('unreviewed', 'Unreviewed'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
    ]
    timestamp = models.DateField(auto_now = True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email_address = models.EmailField()
    student_graduate = models.CharField(max_length=255)
    department_college = models.CharField(max_length=255)
    year_of_passing = models.PositiveIntegerField()
    phone_number = models.CharField(max_length=15)
    resume = models.BinaryField(null=True, blank=True)  # Change to BinaryField
    internship_domain = models.CharField(max_length=255)  # Free input field for internship domain
    duration = models.CharField(max_length=255)
    description = models.TextField()  # Describe about yourself
    agree_to_terms = models.BooleanField(default=False)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='unreviewed')
    created_at = models.DateTimeField(auto_now_add=True)


    newsletter_subscription = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email_address}"



class Newsletter(models.Model):
    logo =  models.ImageField(upload_to='static/assets/Images/pine_images/', blank=True, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    url = models.URLField(max_length=500)
    image = models.ImageField(upload_to='static/assets/Images/pine_images/', blank=True, null=True)
    contact_number = models.BigIntegerField()
    contact_mail = models.CharField(max_length=100)

    # Subtopic 1 fields
    subtopic1_heading = models.CharField(max_length=255)
    subtopic1_content = models.TextField()
    subtopic1_url = models.URLField(max_length=500)
    subtopic1_image = models.ImageField(upload_to='static/assets/Images/pine_images/', blank=True, null=True)

    # Subtopic 2 fields
    subtopic2_heading = models.CharField(max_length=255)
    subtopic2_content = models.TextField()
    subtopic2_url = models.URLField(max_length=500)
    subtopic2_image = models.ImageField(upload_to='static/assets/Images/pine_images/', blank=True, null=True)

    def __str__(self):
        return self.title
    
    

class Product_Launch(models.Model):
    logo =  models.ImageField(upload_to='static/assets/Images/pine_images/', blank=True, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    url = models.URLField(max_length=500)
    image = models.ImageField(upload_to='static/assets/Images/pine_images/', blank=True, null=True)
    

    def __str__(self):
        return self.title
    
    
class Email_Template_JI(models.Model):
    Title = models.CharField(max_length=255)
    Subject = models.CharField(max_length=255)
    content = models.TextField()
    footer = models.TextField()
    
    def __str__(self):
        return self.Title