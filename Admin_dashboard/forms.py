from datetime import date
from django import forms
from jsonschema import ValidationError
from .models import *
from django.forms import modelformset_factory
from django.forms import URLInput

        
class NewsletterSignupForm(forms.Form):
    email = forms.EmailField()


class LifeAtPinesphereForm(forms.ModelForm):
    class Meta:
        model = life_at_pinesphere
        fields = ['title', 'content', 'image', 'url']

    # Optionally, you can add custom widgets or labels here
    def __init__(self, *args, **kwargs):
        super(LifeAtPinesphereForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'placeholder': 'Enter title'})
        self.fields['content'].widget.attrs.update({'placeholder': 'Enter content'})
        self.fields['url'].widget.attrs.update({'placeholder': 'Enter URL'})
        
class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['index_num', 'logo', 'title', 'content', 'client', 'developed_using', 'purpose']

# Create a formset for PortfolioImage
PortfolioImageFormSet = modelformset_factory(
    PortfolioImage,
    fields=('image',),
    extra=1,  # This determines how many empty forms to display
    max_num=5,  # Set maximum number of images allowed
)
class ClientPageForm(forms.ModelForm):
    class Meta:
        model = client_page
        fields = ['index_num', 'image', 'image2', 'Title', 'url']
        widgets = {
            'url': URLInput(attrs={'placeholder': 'Enter a valid URL here'}),
        }
        

class JobPostForm(forms.ModelForm):
    class Meta:
        model = Job_Post
        fields = ['index_num', 'head_tag', 'title', 'location', 'experience']
        
        
class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobFormSubmission
        fields = [
            'first_name', 'last_name', 'date_of_birth', 'email_address', 'phone_number',
            'location', 'experience', 'ctc', 'notice_period', 'resume',
            'willing_to_relocate', 'description', 'agree_to_terms', 'subscribe_me'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Type your enquiry here...'}),
            'resume': forms.ClearableFileInput(attrs={'accept': '.pdf, .doc, .docx'}),
        }
    
    def clean_date_of_birth(self):
        dob = self.cleaned_data.get('date_of_birth')
        if dob > date.today():
            raise ValidationError("Date of birth cannot be in the future.")
        return dob

    