#!/usr/bin/env bash
set -e
BASE_URL="${BASE_URL:-http://127.0.0.1:8000}"

echo "Checking health endpoint..."
curl --fail --silent "$BASE_URL/health"
echo
echo "Sending prediction request..."
curl --fail --silent -X POST "$BASE_URL/predict" \
  -H "Content-Type: application/json" \
  -d '{"sepal_length":5.1,"sepal_width":3.5,"petal_length":1.4,"petal_width":0.2}'
echo
echo "API smoke test completed."
