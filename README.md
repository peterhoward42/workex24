# Insructions for me to make download and build repeatable

### Obtain and build the code

```
mkdir parent
cd parent
python3 -m venv project
cd project
source bin/activate
python -m pip install --upgrade pip

git clone git@github.com:peterhoward42/accounts.git
pip install -r accounts/requirements.txt
```

### Run the service (with the FastAPI CLI)

```
cd accounts/api
fastapi dev main.py
```

###  Try out the service

The service is at `http://127.0.0.1:8000`

The Swagger UI is at `http://127.0.0.1:8000/docs`

The reference CSV input file is at `./reference_tests/data.csv`