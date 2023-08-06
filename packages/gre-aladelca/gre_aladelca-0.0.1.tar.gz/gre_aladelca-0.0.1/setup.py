from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: POSIX',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]


setup(
    name = 'gre_aladelca',
    version = '0.0.1',
    description = 'ES: Principales cálculos para GRE, EN: Main calculations for GRE Exam',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url = 'https://linktr.ee/aladelca',
    author = 'Carlos Adrian Alarcon',
    author_email='alarcon.adrianc@gmail.com',
    license = 'MIT',
    classifiers= classifiers,
    keywords = 'gre, calculations',
    packages = find_packages(),
    install_requires = ['']
    )
