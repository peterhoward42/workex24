# Context
This code implements a REST API that helps you to upload a CSV file that lists some expenses and some incomes, and then offers another endpoint that produces a net
income summary from the stored transactions.

The objective was to iterate, starting with a rudimentary MVP and then provide notes and a commentary on assumptions you made, and what steps would be needed to make it production ready.

Those notes come towards the end of this README.

The code is centred around the FastAPI framework.


# Create the development environment

The code has been developed and tested on Python 3.13.0.

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

The development environment does not set the DATABASE_URL environment variable,
so the tests will create amd use an SQLite file-based database at ./database.db

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

Point your browser to the API docs URL (a SwaggerUI) to try out the API.

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

# Configuring the API to use an external database.

You specify the database connection URL in the DATABASE_URL environment variable.

For example:

```export DATABASE_URL="postgresql+psycopg2://user:password@hostname/database_name'"```

# Assumptions Made
- That each POST of a set of transactions is intended to overwrite any previously saved transactions. (If not it raises questions about: keying them perhaps to one tax year, managing accidental duplication, and how the report would need to be changed)
- That the format of dates in the uploaded CSV data is the format shown in the example.
- That none of the transactions should be stored if there is any validation error of the input file.
- It is ok to replace hyphens in the expected fields of the /report response to underscores. I.e. gross-revenue -> gross_revenue. (I abandoned trying to make the ORM do the mapping)

# Requirements ambiguity (duplicate transactions)
It is unclear how to handle duplicate transactions in the uploaded CSV data. The subtlety is that they might be intentional, given that the date field only specifies the day, not the time.

The choices are:
- Treat it as an error
- Include a warning in the reponse(s)
- Accept duplicates silently
- Add a mandatory parameter to the /transactions request to choose the behaviour.

The API developer should not make this decision - it is a product / client question.

# TODOs
- Make the validation of the Expense vs Income field case insensitive
- A more robust and machine-readable contract for error responses

# What changes would be needed for Production
- Serving on HTTPS and the associated certificate management
- Middleware for things like Authentication and OpenTelemetry, etc.
- A health end point to support external scaling orchestration like Kubernetes
- freeze versions of dependencies
- observability tooling
- Scaling and security infrastructure
    - likely Dockerised
    - likely Kubernetes or serverless
    - orchestration of database migration in combination with service lifecycle management
    - in the case of Kubernetes it would often use Nginx as:
        - reverse proxy
        - TLS/SSL termination
        - cache
        - load balancer

