from django import forms
from app.models import Rating, Comment, Review, User, Part, Course
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review  # Replace 'Review' with the actual name of your model
        fields = ['body']  # Specify the fields you want to include in the form

        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Write your review'}),
        }
        
class RatingForm(forms.ModelForm):
    RATING_CHOICES = [
        ('5', '★★★★★ (5/5)'),
        ('4', '★★★★☆ (4/5)'),
        ('3', '★★★☆☆ (3/5)'),
        ('2', '★★☆☆☆ (2/5)'),
        ('1', '★☆☆☆☆ (1/5)'),
    ]

    rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.Select(attrs={'class': 'form-select js-choice'}))
    
    class Meta:
        model = Rating
        fields = ['rating'] 

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment  # Replace 'Review' with the actual name of your model
        fields = ['body']  # Specify the fields you want to include in the form

        widgets = {
            'body': forms.Textarea(attrs={'class': 'one form-control pe-4 bg-light', 'rows': 1, 'placeholder': 'Write your comment'}),
        }

class UserForm(forms.ModelForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs = {
                "placeholder" : "Password",
                "class" : "form-control"
            }
        ))

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs = {
                "placeholder" : "Password check",
                "class" : "form-control"
            }
        ))
    
    class Meta:
        model = User
        fields = ['avatar', 'username', 'email', 'first_name', 'last_name', 'phone', 'address', 'password1', 'password2']
        
class MyUserCreationForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs = {
                "placeholder" : "Username",
                "class" : "form-control"
            }
        ))


    user_type = forms.ChoiceField(
        choices=User.USER_TYPES,
        widget=forms.Select(
            attrs={
                "class": "form-control"
            }
        )
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs = {
                "placeholder" : "Password",
                "class" : "form-control"
            }
        ))

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs = {
                "placeholder" : "Password check",
                "class" : "form-control"
            }
        ))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'user_type']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['username']
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs = {
                "placeholder" : "Username",
                "class" : "form-control"
            }
        ))

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs = {
                "placeholder" : "Password",
                "class" : "form-control"
            }
        ))

    class Meta:
        model = User
        fields = ['username', 'password']

class CourseSearchForm(forms.Form):
    PRICE_LEVEL_CHOICES = [
        ('', 'All'),
        ('Free', 'Free'),
        ('Paid', 'Paid'),
    ]

    SKILL_LEVEL_CHOICES = [
        ('', 'All levels'),
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ]

    price_level = forms.ChoiceField(choices=PRICE_LEVEL_CHOICES, required=False)
    skill_level = forms.ChoiceField(choices=SKILL_LEVEL_CHOICES, required=False)

    def __init__(self, *args, **kwargs):
        super(CourseSearchForm, self).__init__(*args, **kwargs)

        # Dynamically retrieve parts from the database
        parts = Part.objects.all()
        part_choices = [('', 'All')]
        part_choices.extend([(part.slug, part.name) for part in parts])

        # Update the choices for the 'category' field
        self.fields['category'] = forms.ChoiceField(choices=part_choices, required=False)
        
class CourseForm(forms.ModelForm):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
            'placeholder': 'Type Course name',
        }),
        required=True,
    )

    level = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
            'placeholder': 'Course color',
        }),
        required=True,
    )

    price = forms.DecimalField(
        widget=forms.NumberInput(attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
            'placeholder': '$2999',
        }),
        required=True,
    )

    part = forms.ModelChoiceField(
        queryset=Part.objects.all(),
        widget=forms.Select(attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
        }),
        required=True,
    )

    body = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
            'placeholder': 'Write Course description here',
            'rows': 4,
        }),
        required=False,
    )
    image = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={
            'class': 'your-custom-css-class',  # Add your custom CSS class here
        }),
        required=False,  # Set to True if image is mandatory
    )
    class Meta:
        model = Course
        fields  = '__all__'
        exclude = ['like']