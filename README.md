# Create the development environment

```
mkdir foo
cd foo
git clone  git@github.com:peterhoward42/workex24.git
cd workex24
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt

```

# Run the automated tests

```
make test
```

# Launching the service locally and interacting with it

```
fastapi dev main.py
```

The fastAPI CLI output will include something like this:

```
Serving at: http://127.0.0.1:8000
API docs: http://127.0.0.1:8000/docs
```

Point your browser to the API docs URL to try out the API.

You'll find a sample CSV file at `./reference_tests/data.csv`

Note,

While the service is running you can also run the "official" reference 
tests.

Note, the `test.sh` script assumes the API is being served on port 8000. If it is not please edit the script accordingly.

```
cd reference_tests
./test.sh
```

You should see the set of transactions loaded by a POST request 
to `/transactions`, and then a net income summary from the GET request
to `/report`.