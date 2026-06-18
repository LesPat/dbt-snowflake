#!/usr/bin/env bash
# Syncs the GitHub "About" description and topics from .github/description.
# Requires: gh auth login (account with repo admin access)
set -euo pipefail

REPO="${1:-LesPat/dbt-snowflake}"
DESC="$(tr -d '\n' < "$(dirname "$0")/description")"

gh repo edit "$REPO" \
  --description "$DESC" \
  --add-topic airflow \
  --add-topic covid-19 \
  --add-topic data-engineering \
  --add-topic dbt \
  --add-topic snowflake \
  --add-topic elt

echo "About section updated for https://github.com/$REPO"
