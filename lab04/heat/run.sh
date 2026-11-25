#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

results=../results
mkdir -p "$results/heat-100" "$results/heat-1000"
boundary_csv=$(mktemp)
trap 'rm -f "$boundary_csv"' EXIT

"${MPICC:-mpicc}" -O2 -std=c11 -Wall -Wextra -Werror -pedantic heat.c -o heat
{
  "${MPIRUN:-mpirun}" -n 4 ./heat 100 "$results/heat-100/Output.csv"
  "${MPIRUN:-mpirun}" -n 4 ./heat 1000 "$results/heat-1000/Output.csv"
  "${MPIRUN:-mpirun}" -n 4 ./heat 1 "$boundary_csv" --boundary-check
  python3 verify_plot.py "$results" "$boundary_csv"
} 2>&1 | tee "$results/heat.log"
