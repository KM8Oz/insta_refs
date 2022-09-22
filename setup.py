import setuptools
from instagram_referrer.version import Version
setuptools.setup(name='rambler_google_activator',
                 version=Version('0.1.2').number,
                 description='Instagram referrer (for traffic)',
                 long_description_content_type="text/markdown",
                 long_description=open('README.md').read().strip(),
                 author='@KM8Oz (kmoz000)',
                 author_email='<kimo@oldi.dev>',
                 url='https://github.com/KM8Oz/Instagram-referrer.git',
                 py_modules=['instagram_referrer'],
                 install_requires=[],
                 license='MIT License',
                 keywords=['Traffic', 'SEO', 'Instagram', 'referral', 'links'],
                 classifiers=['Development Status :: 3 - Alpha', 'License :: OSI Approved :: MIT License', 'Topic :: Communications :: Email'])
