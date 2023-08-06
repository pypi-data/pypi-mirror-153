# Danemco Content

Provides a user friendly content management system.

 - pages and category structure instead of direct urls
 - snippets for inserting content

Generally, you should only use `django.contrib.flatpages`. This app is provided
if you need to allow your client to customize sections of text that might exist
across multiple URLs.

## Installation

### Step 1 of 7: Install package

```bash
pip install danemco-content
```

### Step 2 of 7: Update settings.py

Add the following to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = (
    ...
    'django.contrib.sites',
    'content',  # Must come before django_wysiwyg
    'django_wysiwyg',
    ...
)
```

Add the following at the end of your `MIDDLEWARE_CLASSES`:

```python
MIDDLEWARE_CLASSES = (
    ...
    'content.middleware.PageFallbackMiddleware',
)
```

Add the following settings:

```python
DJANGO_WYSIWYG_FLAVOR = 'tinymce'

SITE_ID = 1
```

Make sure the following settings are configured the way you want them:

```
STATIC_ROOT
STATIC_URL
```

### Step 3 of 7: Update urls.py

Create a URL pattern in your urls.py:

```python
from django.conf.urls import include, url

urlpatterns = [
    ...
    url(r'^content/', include('content.urls')),
    ...
]
```

### Step 4 of 7: Update bower.json

Add the following to your dependencies:

```json
"medium-editor": "~1.9.4"
```

### Step 5 of 7: Add the database tables

Run the following command:

```bash
python manage.py migrate
```

### Step 6 of 7: Collect the static files

Run the following commands:

```bash
bower install
python manage.py collectstatic
```

### Step 7 of 7: Update your project's `base.html` template (if necessary)

If you will be using the template that comes with this app, make sure your
project has a `base.html` template and that it has these blocks:

1. description

1. keywords

1. title

1. content

1. extra_styles

1. extra_scripts

1. Optional: pagetitle

## Configuration

To change the TinyMCE settings in the admin, override the
"django_wysiwyg/tinymce/includes.html" template like this:

    {% extends 'content/django_wysiwyg/tinymce/includes.html' %}

    {% block django_wysiwyg_editor_config %}
        {{ block.super }}

        django.jQuery.extend(django_wysiwyg_editor_config, {
            'some_tinymce_option': 'some_value',
        });
    {% endblock django_wysiwyg_editor_config %}

## Snippet Usage

In the template you would like to use a snippet in, use this code:

```
{% load content_tags %}

{% snippet 'name-of-section' 'Optional fallback value if no snippet exists for this section at this URL' %}
```
