#!/usr/bin/env bash
# Run each mutant from a clean source and restore it even when a command fails.
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.."

suite="${1:-main}"
case "$suite" in
  main) maven_args=(); result_dir=results ;;
  ai) maven_args=(-Dtest=CourseRegistrationServiceAiComparison); result_dir=results/ai-comparison ;;
  *) printf 'Usage: bash scripts/run-mutations.sh [main|ai]\n' >&2; exit 2 ;;
esac

service=src/main/java/mn/edu/must/sqat/CourseRegistrationService.java
backup=$(mktemp)
cp -- "$service" "$backup"
restore() { cp -- "$backup" "$service"; rm -f -- "$backup"; }
trap restore EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
mkdir -p -- "$result_dir"

run_suite() {
  local output=$1 expected=$2
  local -a statuses
  set +e
  mvn -B --no-transfer-progress "${maven_args[@]}" clean test 2>&1 | tee "$output"
  statuses=("${PIPESTATUS[@]}")
  set -e
  if (( statuses[1] != 0 )); then
    printf 'Cannot write evidence: %s\n' "$output" >&2
    return 1
  fi
  if [[ "$expected" == green ]]; then
    (( statuses[0] == 0 ))
    grep -q 'BUILD SUCCESS' "$output"
    if [[ "$suite" == main ]]; then
      grep -q 'Tests run: 10, Failures: 0, Errors: 0, Skipped: 0' "$output"
    fi
  else
    (( statuses[0] != 0 ))
    grep -q 'BUILD FAILURE' "$output"
    # A compilation failure alone does not count as killing a mutant.
    grep -Eq 'Tests run: [0-9]+, Failures: [1-9][0-9]*|Tests run: [0-9]+, Failures: [0-9]+, Errors: [1-9][0-9]*' "$output"
  fi
}

# Always record a passing baseline before changing the source.
run_suite "$result_dir/mvn-test.txt" green
for mutant in 1 2 3; do
  cp -- "$backup" "$service"
  case "$mutant" in
    1) sed -i '/if (!student.active()) return "ERROR_INACTIVE_STUDENT";/d' "$service" ;;
    2) sed -i '/repository.saveRegistration(studentId, courseId);/d' "$service" ;;
    3) sed -i 's/studentId == null || courseId == null/studentId == null/' "$service" ;;
  esac
  if cmp -s -- "$backup" "$service"; then
    printf 'Mutation %s did not change the source\n' "$mutant" >&2
    exit 1
  fi
  run_suite "$result_dir/mvn-test-mutant-$mutant.txt" red
  cp -- "$backup" "$service"
done
cmp -- "$backup" "$service"
run_suite "$result_dir/mvn-test.txt" green
printf 'All three mutants detected; source restored (%s suite).\n' "$suite"
