from setuptools import setup, find_packages

version = __import__('content').get_version()

setup(
    name="danemco_content",
    version=version,
    author="Danemco",
    author_email="dev@velocitywebworks.com",
    url='https://gitlab.com/virgodev/lib/danemco-content.git',
    license='BSD License',
    packages=find_packages(),
    install_requires=(
        'django-wysiwyg', 'six'
    ),
    scripts=[],
    include_package_data=True,
    zip_safe=False,
)
