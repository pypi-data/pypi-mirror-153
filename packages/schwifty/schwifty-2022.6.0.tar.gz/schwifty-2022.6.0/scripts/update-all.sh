#!/usr/bin/env bash
set -o errexit

main() {
  local -r root=$(dirname "${BASH_SOURCE[0]}")

  for country in "at" "be" "cz" "de" "es" "fi" "hr" "lv" "nl" "pl" "si" "sk"; do
    echo "---> Updating bank registry for: ${country}"
    python "${root}/get_bank_registry_${country}.py"
  done
}

main
