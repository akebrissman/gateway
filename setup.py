from setuptools import setup

setup(
    name='gateway',
    version='0.1',
    packages=['models', 'resources'],
    url='https://github.com/akebrissman/gateway/',
    license='MIT',
    author='Åke Brissman',
    author_email='ake.brissman@gmail.com',
    description='Referense project for making a RESTful application',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Quality Assurance'
    ],

    python_requires='>=3.6'
)
