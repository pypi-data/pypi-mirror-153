try:
    from ..codebase.html_base_code import *
except ImportError:
    from codebase.html_base_code import *
from termcolor import colored
from colorama import init
init()

django_hitcount_help_text = """\n
 DJANGO HITCOUNT USAGE 
from hitcount.views import HitCountDetailView

class PostCountHitDetailView(HitCountDetailView):
    model = Post        # your model goes here
    count_hit = True    # set to True if you want it to try and count the hit
Docs URL: https://django-hitcount.readthedocs.io/en/latest/installation.html

"""


django_taggit_help_text = f"""\n
 DJANGO TAGGIT USAGE 
from django.db import models

from taggit.managers import TaggableManager

class Food(models.Model):
    # ... fields here

    tags = TaggableManager()
Docs URL: https://django-taggit.readthedocs.io/en/latest/getting_started.html

"""

django_unicorn_help_text = f"""\n
 DJANGO UNICORN USAGE 
{django_unicorn_base_html}
Docs URL: https://www.django-unicorn.com/docs

"""

django_tailwind_help_text = f"""\n
 DJANGO TAILWIND USAGE 
{django_tailwind_base_html}
Docs URL: https://django-tailwind.readthedocs.io/en/latest/installation.html

"""

django_htmx_help_text = f"""\n
\n= DJANGO HTMX USAGE 
{django_htmx_base_html}
Docs URL: https://django-htmx.readthedocs.io/en/latest/installation.html

"""

django_tailwind_crispy_help_text = """\n
\n= DJANGO TAILWIND CRISPY USAGE ")
Current functionality allows the |crispy filter to be used to style your form. In your template:

    Load the filter: {% load tailwind_filters %}
    Apply the crispy filter: {{ form|crispy }}
Docs URL: https://github.com/django-crispy-forms/crispy-tailwind

"""


ckeditor_help_text = f"""\n

Usage
Field

The quickest way to add rich text editing capabilities to your models is to use the included RichTextField model field type. A CKEditor widget is rendered as the form field but in all other regards the field behaves like the standard Django TextField. For example:

from django.db import models
from ckeditor.fields import RichTextField

class Post(models.Model):
    content = RichTextField()

For file upload support use RichTextUploadingField from ckeditor_uploader.fields.
Widget

Alternatively, you can use the included CKEditorWidget as the widget for a formfield. For example:

from django import forms
from django.contrib import admin
from ckeditor.widgets import CKEditorWidget

from post.models import Post

class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Post
        fields = '__all__'

class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm

admin.site.register(Post, PostAdmin)

For file upload support use CKEditorUploadingWidget from ckeditor_uploader.widgets.

Docs URL: https://github.com/django-ckeditor/django-ckeditor

"""