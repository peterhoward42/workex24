echo

curl -X 'POST' \
  'http://0.0.0.0:8000/transactions' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'data=@data.csv;type=text/csv'

echo
echo
echo

curl -X 'GET'  'http://0.0.0.0:8000/report' -H 'accept: application/json'

echo

