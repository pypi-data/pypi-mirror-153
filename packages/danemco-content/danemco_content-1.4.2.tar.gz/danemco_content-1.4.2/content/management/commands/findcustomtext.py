from django.conf import settings
from django.core.management.base import BaseCommand
from django.template.base import Template
from django.template.context import Context
import os
import pkgutil
import re


class Command(BaseCommand):

    def search_dir(self, path):
        if os.path.exists(path):
            for dirpath, dirnames, filenames in os.walk(path):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    content = open(filepath, "r").read()
                    if "customizable" in content:
                        print("----")
                        for result in re.findall(r"""\{% *customizable *(?:request *)?["']([a-z0-9\-_]+)["'] *%\}""", content):
                            print(result)
                        idx = content.index("{% customizable")
                        idx2 = content.index("{% endcustomizable %}", idx)
                        print(Template("{% load content_tags %}" + content[idx:idx2 + len("{% endcustomizable %}")]).render(Context(dict(request=None))))

    def handle(self, *args, **options):
        for app in settings.INSTALLED_APPS:
            path = os.path.join(pkgutil.find_loader(app).filename, "templates")
            self.search_dir(path)

        for path in settings.TEMPLATE_DIRS:
            self.search_dir(path)
