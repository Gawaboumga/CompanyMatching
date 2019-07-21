from setuptools import setup, find_packages


def readme():
    with open('README.rst', 'r', encoding='utf-8') as f:
        return f.read()


def get_version():
    return 0, 0, 1


def get_install_requirements():
    return ['setuptools']


setup(
    name='company-matching',
    version=get_version(),
    description='Fuzzy matching for company\'s names',
    long_description=readme(),
    license='MIT',
    author='Youri Hubaut',
    packages=find_packages(),
    package_data={'company-matching': ['companymatching/elf/elf_company.csv']},
    url='https://github.com/Gawaboumga/CompanyMatching',
    keywords='fuzzy matching company',
    install_requires=get_install_requirements(),
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: Stackless',
    ]
)