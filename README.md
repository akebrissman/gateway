[![Build Status](https://travis-ci.org/akebrissman/gateway.svg?branch=master)](https://travis-ci.org/akebrissman/gateway)

[![Build Status](https://travis-ci.org/akebrissman/gateway.svg?branch=develop)](https://travis-ci.org/akebrissman/gateway)
   
[![Build Status](https://travis-ci.org/akebrissman/gateway.svg?branch=embed-build-status-image)](https://travis-ci.org/akebrissman/gateway)


# Project Title

Gateway for Firebase notifications


## Getting Started


### Installing
Create a Python 3.6 virtual environment and install the packages:
    
    pip install virtualenv
    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt
    pip install -e .
 
```
Run
./app.py
```




Contributing
------------

Really? Very welcome. Do the usual fork-and-submit-PR thingy.

Running the tests:

    python setup.py test
 
Running the test with coverage

    coverage run --source gateway setup.py test
    coverage report -m