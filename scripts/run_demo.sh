#!/usr/bin/env bash
set -euo pipefail

API_URL="${API_URL:-http://localhost:8000/api/v1}"

curl -sS -X POST "$API_URL/demo/run" -H 'Content-Type: application/json' | jq .

REPORT=$(curl -sS -X POST "$API_URL/reports/generate" -H 'Content-Type: application/json')
echo "$REPORT" | jq '{report_id, title, summary}'
