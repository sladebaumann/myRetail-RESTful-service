from setuptools import find_packages, setup

setup(
    name='myretail-restful-service',
    version='1.0.0',
    description='An end-to-end Proof-of-Concept for a products API',
    long_description='An end-to-end Proof-of-Concept for a products API',
    author='Slade Baumann',
    author_email='sladebaumann@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'myretail-restful-service=myretail_restful_service.wsgi:app.api'
        ],
    },
    install_requires=['falcon', 'mock', 'redis'],
    classifiers=[],
)