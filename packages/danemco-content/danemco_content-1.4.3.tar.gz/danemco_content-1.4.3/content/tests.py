import datetime

from django.contrib.auth import get_user_model
from django.http.response import HttpResponseNotFound
from django.template.base import Template, TemplateSyntaxError
from django.template.context import Context
from django.test.client import RequestFactory
from django.test.testcases import TestCase
from django.test.utils import override_settings
from django.utils import timezone

from content.middleware import PageFallbackMiddleware
from content.models import Page, Section, Snippet


User = get_user_model()


class ContentTestCase(TestCase):

    def setUp(self):
        self.section = Section.objects.create(name="foozle")

    def test_view(self):

        # sanity check
        response = self.client.get("/")
        self.assertEqual(response.status_code, 404)

        Page.objects.create(url="/", content="Foo")
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_login_required_anonymous(self):
        Page.objects.create(url="/", content="Foo", registration_required=True)
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)

    def test_login_required_logged(self):
        Page.objects.create(url="/", content="Foo", registration_required=True)
        User.objects.create_user("test", "", "test")
        self.client.login(username="test", password="test")
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_middleware(self):
        middleware = PageFallbackMiddleware()
        factory = RequestFactory()

        # no page has been created
        response = middleware.process_response(
            factory.get("/test/"),
            HttpResponseNotFound()
        )

        self.assertEqual(response.status_code, 404)

        # insert page
        Page.objects.create(url="/test/")

        response = middleware.process_response(
            factory.get("/test/"),
            HttpResponseNotFound()
        )
        self.assertEqual(response.status_code, 200)

    @override_settings(DEBUG=False)
    def test_snippet_without_debug(self):

        self.assertEqual(Section.objects.filter(name="foo").count(), 0)

        template_missing_section_name = \
            Template("{% load content_tags %}{% snippet %}")
        self.assertEqual(template_missing_section_name.render(Context()), "")

        template_invalid_section_name = \
            Template("{% load content_tags %}{% snippet 'foo' %}")
        self.assertEqual(template_invalid_section_name.render(Context()), "")

        template_valid_section_name = \
            Template("{% load content_tags %}{% snippet 'foozle' %}")
        self.assertEqual(template_valid_section_name.render(Context()), "")

        template_valid_section_name_default = \
            Template("{% load content_tags %}{% snippet 'foozle' 'default' %}")
        self.assertEqual(
            template_valid_section_name_default.render(Context()),
            "default"
        )

        Snippet.objects.create(
            section=self.section,
            content="foo"
        )

        self.assertEqual(template_valid_section_name.render(Context()), "foo")

    @override_settings(DEBUG=True)
    def test_snippet_with_debug(self):

        self.assertEqual(Section.objects.filter(name="foo").count(), 0)

        with self.assertRaises(TemplateSyntaxError):
            template_missing_section_name = \
                Template("{% load content_tags %}{% snippet %}")
            template_missing_section_name.render(Context())

        with self.assertRaises(Section.DoesNotExist):
            template_invalid_section_name = \
                Template("{% load content_tags %}{% snippet 'foo' %}")
            template_invalid_section_name.render(Context())

        template_valid_section_name = \
            Template("{% load content_tags %}{% snippet 'foozle' %}")
        self.assertEqual(template_valid_section_name.render(Context()), "")

        template_valid_section_name_default = \
            Template("{% load content_tags %}{% snippet 'foozle' 'default' %}")
        self.assertEqual(
            template_valid_section_name_default.render(Context()),
            "default"
        )

        Snippet.objects.create(
            section=self.section,
            content="foo"
        )

        self.assertEqual(template_valid_section_name.render(Context()), "foo")

    def test_publish_soon_snippet(self):

        template = Template("{% load content_tags %}{% snippet 'foozle' %}")

        Snippet.objects.create(
            section=self.section,
            content="foo1"
        )
        Snippet.objects.create(
            section=self.section,
            publish=timezone.now() + datetime.timedelta(hours=1),
            content="foo2"
        )

        self.assertEqual(template.render(Context()), "foo1")

    def test_published_snippet(self):

        template = Template("{% load content_tags %}{% snippet 'foozle' %}")

        Snippet.objects.create(
            section=self.section,
            content="foo1"
        )
        Snippet.objects.create(
            section=self.section,
            publish=timezone.now() - datetime.timedelta(hours=1),
            content="foo2"
        )
        Snippet.objects.create(
            section=self.section,
            publish=timezone.now() - datetime.timedelta(hours=2),
            content="foo3"
        )

        self.assertEqual(template.render(Context()), "foo2")

    def test_expire_soon_snippet(self):

        template = Template("{% load content_tags %}{% snippet 'foozle' %}")

        Snippet.objects.create(
            section=self.section,
            content="foo1"
        )
        Snippet.objects.create(
            section=self.section,
            expire=timezone.now() + datetime.timedelta(hours=1),
            content="foo2"
        )
        Snippet.objects.create(
            section=self.section,
            expire=timezone.now() + datetime.timedelta(hours=2),
            content="foo3"
        )
        # also takes precedence over publish time
        Snippet.objects.create(
            section=self.section,
            publish=timezone.now() - datetime.timedelta(hours=2),
            content="foo4"
        )

        self.assertEqual(template.render(Context()), "foo2")

    def test_expired_snippet(self):

        template = Template("{% load content_tags %}{% snippet 'foozle' %}")

        Snippet.objects.create(
            section=self.section,
            content="foo1"
        )
        Snippet.objects.create(
            section=self.section,
            expire=timezone.now() - datetime.timedelta(hours=1),
            content="foo2"
        )

        self.assertEqual(template.render(Context()), "foo1")
