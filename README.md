# Context
This code is a partially finished REST API that helps someone to upload a CSV file that lists some expenses and some incomes, and then offers another endpoint that produced a net
income summary from the stored transactions.

The objective was to iterate from a rudimentary MVP and then provide notes and a commentary on assumptions you made, and what steps would be needed to make it production ready.

Those notes come towards the end of this README.

The code is centred around the FastAPI framework.


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

# Assumptions Made
- That each POST of a set of transactions is intended to overwrite any set that might be already stored. (If not it raises questions about: keying them perhaps to one tax year, managing accidental duplication, and how the report would need to be changed)
- That the format of dates in the uploaded CSV data is only expected be that shown in the example.
- That the required behaviour for a validation error any one of the input CSV lines should return an error response and not store any transactions.
- It is ok to change fields in the reports response that have a hypen (gross-revenue) to (gross_revenue). (I abandoned trying to make the ORM do the mapping)

# What is missing from the base requirements
- Persistent storage. (It does have ephemeral storage)

# Some requirements ambiguity I have not tackled
- What if the uploaded CSV data contains duplicates?
    -  Ostensibly the code could remove duplicates.
    -  But the time granularity is one day, so it is just conceivable that two genuine
       transactions could occur on the same day with the same party for the same amount.
    -  For production quality that cannot be ignored
        - Maybe a warning in the response - but that could be easily be missed by a client.
        - I'd go for parameterising the /report input to include a (mandatory) field to govern the treatment of duplicates as either an error or legitimate.

# What changes would be needed for Production
- To complete the persistent storage requirement.
    -  I envisaged using a SQL database
    -  Via a FastAPI/SQLAlchemy ORM
    -  Reading database connection configuration details from environment variables, but in their absence defaulting to a built-in local SQLite database (for conveient development).
    -  I have this nearly working on a git branch, but have got bogged down in some session lifecycle exceptions being raised.
- Serving on HTTPS and the associated certificate management
- Middleware for things like Authentication and OpenTelemetry
- A health end point to support external scaling orchestration
- The isolation of database migration tooling so that it can be orchestrated properly in the context of horizontally scaled API services. 
- Make the validation of the Expense vs Income field case insensitive
- A more robust and machine-readable contract for error responses.

