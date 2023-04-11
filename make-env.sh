#!/bin/bash

cat > ./wc_testing/.env <<EOF

HOST=http://127.0.0.1
PORT=8000

DB_NAME=test1
DB_USER=postgres
DB_PASSWORD=3141592653589
DB_HOST=localhost

JWT_KEY = 78hdls&02kihal9ehchwGH8skAHhr0KSHdv'kq19316&@9dcd9&)@
JWT_REFRESH_KEY = hdfk(!8dhcsdfk-e+sfle;vdf9kdjdfhlaey%@138fhDGA;s90

EOF
