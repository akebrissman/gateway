# Project Title

Gateway-service, a reference project for REST APIs


## Getting Started


### Installing
Create a Python 3.8 virtual environment and install the packages:
    
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    pip install -e .
 
```
Run
./app.py
```


### Project information
- 


### Contributing
Really? Very welcome. Do the usual fork-and-submit-PR thingy.

Running the tests:

    cp .env.test .env 
    python setup.py test
 
Running the test with coverage

    coverage run --source gateway setup.py test
    coverage report -m
