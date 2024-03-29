from setuptools import setup

setup(
    name='gateway',
    version='1.0.0',
    packages=['gateway'],
    url='https://github.com/akebrissman/gateway/',
    license='MIT',
    author='Åke Brissman',
    author_email='ake.brissman@gmail.com',
    description='Reference project for making a RESTful application',
    setup_requires=[
        'pytest-runner'
    ],
    install_requires=[
        'Flask',
        'Flask-RESTful',
        'Flask-SQLAlchemy',
        'pydantic',
        'python-dotenv',
        'python-jose'
    ],
    tests_require=[
         'pytest',
         'coverage'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Quality Assurance'
    ],
    python_requires='>=3.8'
)
