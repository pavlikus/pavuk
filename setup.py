from setuptools import find_packages, setup


setup(
    name='pavuk',
    version='0.0.9',
    packages=find_packages(),
    py_modules=['formater', 'pavuk', 'scraper'],
    include_package_data=True,
    license='GNU General Public License v3.0',
    description="Web Scraper",
    author='Pavlik',
    author_email='readystores.ru@gmail.com',
    install_requires=[
        "beautifulsoup4==4.9.1",
        "requests==2.23.0",
        "selenium==3.141.0",
        "lxml==4.5.0"
    ],
    entry_points={
        'console_scripts': [
            'pavuk = pavuk:main',
        ]
    },
)
