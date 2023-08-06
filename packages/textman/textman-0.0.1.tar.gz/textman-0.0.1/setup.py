from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='textman',
    version='0.0.1',
    description='some methods of number theory',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Rahul Golder',
    author_email='rahulgolder0202@gmail.com',
    maintainer = "Rahul Golder",
    maintaier_email = "rahulgolder0202@gmail.com",
    license='MIT',
    classifiers=classifiers,
    keywords='text',
    packages=find_packages(),
    install_requires=[
        'setuptools >= 60.2.0',
        'textblob >= 0.17.1',
        'gramformer >= 1.0',
        'styleformer >= 0.1',
        'cleantext >= 1.1.4',
        'googletrans >= 3.0.0',
        'PyDictionary >= 2.0.1'
    ]
)