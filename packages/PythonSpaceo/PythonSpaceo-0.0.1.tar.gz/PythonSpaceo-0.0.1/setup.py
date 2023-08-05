import os
from setuptools import setup



here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()


lib_folder = os.path.dirname(os.path.realpath(__file__))
requirement_path = lib_folder + '/requirements.txt'
install_requires = [] # Here we'll get: ["gunicorn", "docutils>=0.3", "lxml==0.5a7"]
if os.path.isfile(requirement_path):
    with open(requirement_path) as f:
        install_requires = f.read().splitlines()
setup(
    name='PythonSpaceo',
    version='0.0.1',
    packages=['authentication','Custom','BaseCode','CMS'],
    description='python basecode package(api,admin panel)',
        # long_description="""# Markdown supported!\n\n* Cheer\n* Celebrate\n""",
    long_description=README,
    long_description_content_type='text/markdown',
    author='deepak',
    author_email='deepak@example.com',
    license='MIT',
    include_package_data=True,
    install_requires=[
        'facebook-sdk==3.1.0',
        'django-debug-toolbar==3.2.4',
        'django-jazzmin==2.5.0',
        'django-phonenumber-field==6.1.0',
        'django-tinymce==3.4.0',
        'djangorestframework==3.13.1',
        'djangorestframework-simplejwt==5.1.0',
        'drf-spectacular==0.22.1',
        'uritemplate==4.1.1',
        'urllib3==1.26.9',
    ]

)